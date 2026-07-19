from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st


ROOT = Path(__file__).resolve().parent
CANDIDATE_DIR = ROOT / "output" / "candidates"
APPROVED_DIR = ROOT / "output" / "approved"
REVIEW_DIR = ROOT / "output" / "reviews"
REPORT_DIR = ROOT / "output" / "review-reports"

for folder in (CANDIDATE_DIR, APPROVED_DIR, REVIEW_DIR, REPORT_DIR):
    folder.mkdir(parents=True, exist_ok=True)


REAL_BRAND_TERMS = {
    "iphone", "apple", "whatsapp", "facebook", "instagram", "twitter",
    "tiktok", "amazon", "google", "microsoft", "samsung", "tesla",
    "paypal", "netflix", "spotify", "youtube", "reddit", "discord",
    "telegram", "snapchat", "uber", "deliveroo",
}

PLACEHOLDER_TERMS = {
    "targetname", "portalname", "fictionaluser", "example hospital",
    "example company", "john doe", "jane doe",
}

URL_RE = re.compile(
    r"\b(?:https?://|www\.|bit\.ly/|tinyurl\.com/|t\.co/)\S+",
    re.IGNORECASE,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def find_candidate_files() -> list[Path]:
    return sorted(
        CANDIDATE_DIR.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def warning_flags(post: dict[str, Any]) -> list[str]:
    combined = " ".join(
        str(post.get(key, ""))
        for key in ("author", "text", "scenario", "explanation", "location", "platform")
    ).casefold()

    warnings: list[str] = []

    found_brands = sorted(term for term in REAL_BRAND_TERMS if term in combined)
    if found_brands:
        warnings.append("Possible real brand/platform: " + ", ".join(found_brands))

    found_placeholders = sorted(
        term for term in PLACEHOLDER_TERMS if term in combined
    )
    if found_placeholders:
        warnings.append(
            "Placeholder or generic identity: " + ", ".join(found_placeholders)
        )

    if URL_RE.search(combined):
        warnings.append("Live-looking URL detected; prefer [link removed].")

    if post.get("correctAction") == "Escalate" and not post.get(
        "correctEscalationReason"
    ):
        warnings.append("Escalated post has no escalation reason.")

    if post.get("correctAction") != "Escalate" and post.get(
        "correctEscalationReason"
    ):
        warnings.append("Non-escalated post contains an escalation reason.")

    return warnings


def review_file_for(candidate: Path) -> Path:
    return REVIEW_DIR / f"{candidate.stem}-review.json"


def load_saved_review(candidate: Path) -> dict[str, Any]:
    review_path = review_file_for(candidate)
    if review_path.exists():
        return load_json(review_path)
    return {"candidate": candidate.name, "items": {}}


def build_review_payload(
    candidate: Path,
    posts: list[dict[str, Any]],
) -> dict[str, Any]:
    items: dict[str, Any] = {}
    for post in posts:
        post_id = str(post.get("id", ""))
        items[post_id] = {
            "decision": st.session_state.get(f"{post_id}-decision", "Pending"),
            "reviewNotes": st.session_state.get(f"{post_id}-notes", ""),
            "post": {
                **post,
                "author": st.session_state.get(
                    f"{post_id}-author", post.get("author", "")
                ),
                "text": st.session_state.get(
                    f"{post_id}-text", post.get("text", "")
                ),
                "category": st.session_state.get(
                    f"{post_id}-category", post.get("category", "")
                ),
                "correctAction": st.session_state.get(
                    f"{post_id}-action", post.get("correctAction", "")
                ),
                "difficulty": st.session_state.get(
                    f"{post_id}-difficulty", post.get("difficulty", "")
                ),
                "explanation": st.session_state.get(
                    f"{post_id}-explanation", post.get("explanation", "")
                ),
                "day": int(
                    st.session_state.get(f"{post_id}-day", post.get("day", 1))
                ),
                "correctEscalationReason": st.session_state.get(
                    f"{post_id}-reason",
                    post.get("correctEscalationReason", ""),
                ),
                "scenario": st.session_state.get(
                    f"{post_id}-scenario", post.get("scenario", "")
                ),
            },
        }

    return {
        "candidate": candidate.name,
        "savedAt": datetime.now().isoformat(timespec="seconds"),
        "items": items,
    }


def initialise_session(
    posts: list[dict[str, Any]],
    saved: dict[str, Any],
) -> None:
    saved_items = saved.get("items", {})
    for post in posts:
        post_id = str(post.get("id", ""))
        existing = saved_items.get(post_id, {})
        edited = existing.get("post", post)

        defaults = {
            f"{post_id}-decision": existing.get("decision", "Pending"),
            f"{post_id}-notes": existing.get("reviewNotes", ""),
            f"{post_id}-author": edited.get("author", post.get("author", "")),
            f"{post_id}-text": edited.get("text", post.get("text", "")),
            f"{post_id}-category": edited.get(
                "category", post.get("category", "")
            ),
            f"{post_id}-action": edited.get(
                "correctAction", post.get("correctAction", "")
            ),
            f"{post_id}-difficulty": edited.get(
                "difficulty", post.get("difficulty", "")
            ),
            f"{post_id}-explanation": edited.get(
                "explanation", post.get("explanation", "")
            ),
            f"{post_id}-day": int(edited.get("day", post.get("day", 1))),
            f"{post_id}-reason": edited.get(
                "correctEscalationReason",
                post.get("correctEscalationReason", ""),
            ),
            f"{post_id}-scenario": edited.get(
                "scenario", post.get("scenario", "")
            ),
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value


def markdown_report(
    candidate: Path,
    review_payload: dict[str, Any],
) -> str:
    items = review_payload["items"]
    counts = {
        decision: sum(
            1 for item in items.values() if item["decision"] == decision
        )
        for decision in ("Approve", "Edit", "Reject", "Pending")
    }

    lines = [
        f"# Review Report — {candidate.name}",
        "",
        f"Saved: {review_payload['savedAt']}",
        "",
        "## Summary",
        "",
        f"- Approve: {counts['Approve']}",
        f"- Edit: {counts['Edit']}",
        f"- Reject: {counts['Reject']}",
        f"- Pending: {counts['Pending']}",
        "",
        "| ID | Decision | Action | Difficulty | Notes |",
        "|---|---|---|---|---|",
    ]

    for post_id, item in items.items():
        post = item["post"]
        notes = str(item.get("reviewNotes", "")).replace("|", "\\|")
        lines.append(
            f"| {post_id} | {item['decision']} | "
            f"{post.get('correctAction', '')} | "
            f"{post.get('difficulty', '')} | {notes} |"
        )

    return "\n".join(lines) + "\n"


st.set_page_config(
    page_title="Moderation Game Content Review",
    page_icon="🧾",
    layout="wide",
)

st.title("Moderation Game — Candidate Review")
st.caption(
    "Review AI-generated filler posts. The source candidate remains unchanged."
)

candidate_files = find_candidate_files()
if not candidate_files:
    st.error(
        "No candidate JSON files found in output/candidates. "
        "Generate or copy a candidate batch there first."
    )
    st.stop()

candidate_names = [path.name for path in candidate_files]
selected_name = st.sidebar.selectbox("Candidate batch", candidate_names)
candidate_path = CANDIDATE_DIR / selected_name

payload = load_json(candidate_path)
posts = payload.get("posts", [])
if not isinstance(posts, list) or not posts:
    st.error("Candidate file must contain a non-empty posts array.")
    st.stop()

candidate_key = f"active-candidate::{candidate_path.name}"
if st.session_state.get("loaded-candidate") != candidate_key:
    for key in list(st.session_state):
        if key != "loaded-candidate":
            del st.session_state[key]
    st.session_state["loaded-candidate"] = candidate_key

saved_review = load_saved_review(candidate_path)
initialise_session(posts, saved_review)

decisions = [
    st.session_state.get(f"{post['id']}-decision", "Pending")
    for post in posts
]
summary_cols = st.columns(4)
for col, decision in zip(
    summary_cols, ("Approve", "Edit", "Reject", "Pending")
):
    col.metric(decision, decisions.count(decision))

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Decision meanings**\n\n"
    "- **Approve:** usable without a content change\n"
    "- **Edit:** usable after the edits shown here\n"
    "- **Reject:** exclude from approved export\n"
)

for index, post in enumerate(posts, start=1):
    post_id = str(post.get("id", f"POST-{index}"))
    current_post = {
        **post,
        "author": st.session_state[f"{post_id}-author"],
        "text": st.session_state[f"{post_id}-text"],
        "category": st.session_state[f"{post_id}-category"],
        "correctAction": st.session_state[f"{post_id}-action"],
        "difficulty": st.session_state[f"{post_id}-difficulty"],
        "explanation": st.session_state[f"{post_id}-explanation"],
        "day": st.session_state[f"{post_id}-day"],
        "correctEscalationReason": st.session_state[f"{post_id}-reason"],
        "scenario": st.session_state[f"{post_id}-scenario"],
    }

    warnings = warning_flags(current_post)
    title = (
        f"{index}. {post_id} — "
        f"{current_post.get('correctAction', '')} / "
        f"{current_post.get('category', '')} / "
        f"{current_post.get('difficulty', '')}"
    )

    with st.expander(title, expanded=index == 1):
        if warnings:
            for warning in warnings:
                st.warning(warning)

        top = st.columns([1, 1, 2])
        top[0].selectbox(
            "Decision",
            ("Pending", "Approve", "Edit", "Reject"),
            key=f"{post_id}-decision",
        )
        top[1].number_input(
            "Earliest eligible day",
            min_value=0,
            max_value=99,
            step=1,
            key=f"{post_id}-day",
        )
        top[2].text_input("Author", key=f"{post_id}-author")

        st.text_area(
            "Post text",
            height=120,
            key=f"{post_id}-text",
        )

        meta = st.columns(4)
        meta[0].text_input("Category", key=f"{post_id}-category")
        meta[1].selectbox(
            "Correct action",
            ("Approve", "Remove", "Escalate"),
            key=f"{post_id}-action",
        )
        meta[2].selectbox(
            "Difficulty",
            ("Easy", "Medium", "Hard"),
            key=f"{post_id}-difficulty",
        )
        meta[3].text_input(
            "Escalation reason",
            key=f"{post_id}-reason",
            help="Leave blank unless the correct action is Escalate.",
        )

        st.text_area(
            "Scenario/context",
            height=90,
            key=f"{post_id}-scenario",
        )
        st.text_area(
            "Explanation",
            height=110,
            key=f"{post_id}-explanation",
        )
        st.text_area(
            "Reviewer notes",
            height=80,
            key=f"{post_id}-notes",
        )

st.markdown("---")
review_payload = build_review_payload(candidate_path, posts)

action_cols = st.columns(3)

if action_cols[0].button("Save review progress", type="primary"):
    review_path = review_file_for(candidate_path)
    write_json(review_path, review_payload)
    st.success(f"Saved review progress to {review_path.relative_to(ROOT)}")

approved_posts = [
    item["post"]
    for item in review_payload["items"].values()
    if item["decision"] in {"Approve", "Edit"}
]
pending_count = sum(
    1
    for item in review_payload["items"].values()
    if item["decision"] == "Pending"
)

if action_cols[1].button("Export approved JSON"):
    if pending_count:
        st.error(
            f"{pending_count} post(s) are still Pending. "
            "Review every post before exporting."
        )
    elif not approved_posts:
        st.error("Nothing is approved for export.")
    else:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        approved_path = APPROVED_DIR / (
            f"{candidate_path.stem}-approved-{timestamp}.json"
        )
        report_path = REPORT_DIR / (
            f"{candidate_path.stem}-review-{timestamp}.md"
        )
        write_json(approved_path, {"posts": approved_posts})
        report_path.write_text(
            markdown_report(candidate_path, review_payload),
            encoding="utf-8",
        )
        write_json(review_file_for(candidate_path), review_payload)
        st.success(
            f"Exported {len(approved_posts)} post(s) to "
            f"{approved_path.relative_to(ROOT)}"
        )
        st.info(f"Review report: {report_path.relative_to(ROOT)}")

approved_json = json.dumps(
    {"posts": approved_posts},
    ensure_ascii=False,
    indent=2,
).encode("utf-8")

action_cols[2].download_button(
    "Download current approved JSON",
    data=approved_json,
    file_name=f"{candidate_path.stem}-approved.json",
    mime="application/json",
    disabled=not approved_posts,
)

st.caption(
    "The reviewer never changes input/posts.json or the original candidate file."
)

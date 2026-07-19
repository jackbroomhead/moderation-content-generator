from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from scripts.tag_rules import (
    CONTROLLED_SENSITIVITY_TAGS,
    canonicalise_tags,
    suggested_sensitivity_tags,
)


ROOT = Path(__file__).resolve().parent
CANDIDATE_DIR = ROOT / "output" / "candidates"
APPROVED_DIR = ROOT / "output" / "approved"
REVIEW_DIR = ROOT / "output" / "reviews"
REPORT_DIR = ROOT / "output" / "review-reports"

for folder in (CANDIDATE_DIR, APPROVED_DIR, REVIEW_DIR, REPORT_DIR):
    folder.mkdir(parents=True, exist_ok=True)

SENSITIVITY_TAGS = list(CONTROLLED_SENSITIVITY_TAGS)

SPECIALIST_REASONS = [
    "",
    "HealthMedical",
    "CivicElection",
    "PublicSafetyEmergency",
    "FinancialEconomic",
    "SyntheticManipulatedMedia",
]

PARENT_ESCALATION_REASONS = [
    "ThreatViolence",
    "SelfHarmCrisis",
    "HarassmentAbuse",
    "FraudScam",
    "PrivacySensitiveInfo",
    "MisinformationPublicHarm",
]

METADATA_FIELDS = [
    "accountAgeDays",
    "followerCount",
    "followingCount",
    "verifiedStatus",
    "postCount",
    "bio",
    "previousFlags",
    "location",
    "platform",
]

NUMERIC_METADATA_FIELDS = {
    "accountAgeDays",
    "followerCount",
    "followingCount",
    "postCount",
    "previousFlags",
}

CATEGORY_OPTIONS = [
    "Normal",
    "Lifestyle",
    "Public Information",
    "News / Public Event",
    "Spam",
    "Fraud",
    "Harassment",
    "Privacy",
    "Threat",
    "Misinformation",
    "Self-Harm",
]

APPROVED_FICTIONAL_LOCATIONS = [
    "",
    "Unknown",
    "Westbridge",
    "Oakhaven",
    "Northbridge",
    "Greyford",
    "Bellmere",
    "Moorvale",
    "Dunmere",
    "East Westbridge",
    "Near Westbridge",
    "Near Oakhaven",
    "Near Northbridge",
    "Near Greyford",
    "Near Bellmere",
    "Near Moorvale",
    "Near Dunmere",
]

APPROVED_FICTIONAL_PLATFORMS = [
    "",
    "PhotoBoard",
    "CommonThread",
    "TownSquare",
    "EchoBoard",
    "QuickPost",
    "CommunityFeed",
    "MarketBoard",
    "StoryGrid",
    "PublicSquare",
    "ClipLoop",
]

BLOCKED_REAL_PLACE_TERMS = {
    "london", "manchester", "birmingham", "leeds", "liverpool", "bristol",
    "sheffield", "nottingham", "derby", "brighton", "luton", "york",
    "yorkshire", "north yorkshire", "glasgow", "edinburgh", "cardiff",
    "belfast", "oxford", "cambridge", "newcastle", "leicester", "coventry",
    "southampton", "portsmouth", "plymouth", "swansea",
    "aberdeen", "dundee", "piccadilly",
}

PLATFORM_TOKEN_RE = re.compile(
    r"(?i)\b(?:"
    + "|".join(
        re.escape(item)
        for item in APPROVED_FICTIONAL_PLATFORMS
        if item
    )
    + r")\b"
)


REAL_BRAND_TERMS = {
    "iphone", "apple", "whatsapp", "facebook", "instagram", "twitter",
    "tiktok", "amazon", "google", "microsoft", "samsung", "tesla",
    "paypal", "netflix", "spotify", "youtube", "reddit", "discord",
    "telegram", "snapchat", "uber", "deliveroo",
}

PLACEHOLDER_TERMS = {
    "targetname", "targetuser", "realplayername", "realusername",
    "portalname", "fictionaluser", "sampleuser", "dummyuser",
    "example hospital", "example company", "john doe", "jane doe",
}

PLACEHOLDER_HANDLE_RE = re.compile(
    r"(?i)(?:@)?(?:target(?:user|name)?|realplayername|realusername|"
    r"sampleuser|dummyuser|testuser|user\d{4,})\b"
)

URL_RE = re.compile(
    r"\b(?:https?://|www\.|bit\.ly/|tinyurl\.com/|t\.co/)\S+",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d ()-]{6,}\d)(?!\w)")
LONG_NUMBER_RE = re.compile(r"\b\d{8,19}\b")
SORT_CODE_RE = re.compile(r"\b\d{2}[- ]\d{2}[- ]\d{2}\b")
HASHTAG_RE = re.compile(r"(?<!\w)#[A-Za-z0-9_]+")
DIGIT_SUFFIX_RE = re.compile(r"\d{2,}$")


# Conservative policy-quality heuristics for reviewer triage. They are warnings,
# not automatic moderation decisions.
FRAUD_REQUEST_RE = re.compile(
    r"(?i)\b(?:reply|send|provide|enter|share|message|pay|transfer|deposit|"
    r"verify|confirm)\b.{0,120}\b(?:password|login details?|login credentials?|"
    r"2fa|security code|card number|expiry date|bank details?|gift cards?|crypto|"
    r"deposit|payment handle|identity documents?|home address|phone number|"
    r"daily routine)\b"
)
DANGEROUS_CHALLENGE_RE = re.compile(
    r"(?i)\b(?:challenge|dare|prove (?:you'?re|you are) brave|no safety gear|"
    r"moving train|outside of a train|jump(?:ing)? from|jump(?:ing)? off|"
    r"quarry|freezing water|run(?:ning)? into traffic|break your own bones?|"
    r"ledge|cliff|stunt)\b"
)
HEALTH_HARM_RE = re.compile(
    r"(?i)\b(?:skip (?:the )?(?:vaccine|injection|doctor|hospital|treatment)|"
    r"stop prescribed treatment|stop treatment|avoid emergency care|false cure|"
    r"miracle cure|cures? all cancers?|bleach|detox (?:instead|cure|protocol)|"
    r"replace (?:prescribed|medical|hospital)|doctors? (?:are )?hiding)\b"
)
THREAT_LANGUAGE_RE = re.compile(
    r"(?i)\b(?:i will|i'll|we will|we'll|going to|planning to|bring(?:ing)? a|"
    r"weapon|knife|gun|hammer|attack|hurt|smash|smashing|burn|set fire|kill|shoot|stab|bomb|poison bait|cull the stray|locking .* in the shed|confrontation|settle the score|deal' with anyone|"
    r"target|outside .{0,40} at \d|tonight|tomorrow)\b"
)
HARASSMENT_ESCALATION_RE = re.compile(
    r"(?i)\b(?:coordinated|brigad(?:e|ing)|mass report|report every|repeatedly|"
    r"keeps messaging|asked (?:him|her|them|you) to stop|after i blocked|"
    r"new accounts?|stalking|following me|won't leave me alone|flood(?:ed)?"
    r" (?:my )?(?:dms|messages))\b"
)
FIRST_PERSON_CRISIS_RE = re.compile(
    r"(?i)\b(?:i (?:do not|don't) think i am safe|i have taken|i took|"
    r"i(?:'|â€™)m going to hurt myself|hurt myself|make myself disappear|"
    r"end my life|goodbye messages?|won't be here|not be here in the morning|"
    r"can't go on|cannot go on|overdose)\b"
)
PRIVACY_SIGNAL_RE = re.compile(
    r"(?i)\b(?:home address|phone number|daily routine|medical records?|"
    r"diagnosis|hospital results?|identity document|passport|driving licence|"
    r"private address|where (?:they|she|he) live|leaves work)\b"
)


def coerce_int(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    try:
        text = str(value).strip()
        return int(float(text)) if text else 0
    except (TypeError, ValueError):
        return 0


def coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().casefold() in {"true", "1", "yes", "y", "on"}


def normalise_review_post(post: dict[str, Any]) -> dict[str, Any]:
    result = dict(post)
    result["day"] = coerce_int(result.get("day", 1))
    for field in NUMERIC_METADATA_FIELDS:
        result[field] = coerce_int(result.get(field, 0))
    result["verifiedStatus"] = coerce_bool(result.get("verifiedStatus", False))
    result["isStoryPost"] = coerce_bool(result.get("isStoryPost", False))
    result["allowNeedsReviewEscalation"] = coerce_bool(
        result.get("allowNeedsReviewEscalation", False)
    )
    result["tags"] = canonicalise_tags(result.get("tags", []) or [])
    result["acceptableEscalationReasons"] = list(
        result.get("acceptableEscalationReasons", []) or []
    )
    result["acceptableSpecialistReasons"] = list(
        result.get("acceptableSpecialistReasons", []) or []
    )
    result.setdefault("correctSpecialistReason", "")

    action = str(result.get("correctAction", ""))
    if action != "Escalate":
        result["correctEscalationReason"] = ""
        result["acceptableEscalationReasons"] = []
        result["allowNeedsReviewEscalation"] = False
        result["correctSpecialistReason"] = ""
        result["acceptableSpecialistReasons"] = []
    elif str(result.get("correctEscalationReason", "")) != "MisinformationPublicHarm":
        result["correctSpecialistReason"] = ""
        result["acceptableSpecialistReasons"] = []

    return result


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
    author = str(post.get("author", ""))
    text = str(post.get("text", ""))
    explanation = str(post.get("explanation", ""))
    combined = " ".join(
        str(post.get(key, ""))
        for key in (
            "author", "text", "scenario", "explanation", "location", "platform"
        )
    ).casefold()

    warnings: list[str] = []

    visible_world_text = " ".join(
        str(post.get(key, ""))
        for key in ("author", "text", "bio", "location")
    ).casefold()
    found_real_places = sorted(
        term for term in BLOCKED_REAL_PLACE_TERMS
        if re.search(rf"\b{re.escape(term)}\b", visible_world_text)
    )
    if found_real_places:
        warnings.append(
            "Real-world place name detected: " + ", ".join(found_real_places)
        )

    if PLATFORM_TOKEN_RE.search(author):
        warnings.append("Username contains a platform name.")

    if PLATFORM_TOKEN_RE.search(text):
        warnings.append(
            "Visible text names a platform; normally use 'the app' or 'the platform'."
        )

    location_value = str(post.get("location", "")).strip()
    if location_value not in APPROVED_FICTIONAL_LOCATIONS:
        warnings.append("Location is outside the approved fictional-world list.")

    platform_value = str(post.get("platform", "")).strip()
    if platform_value not in APPROVED_FICTIONAL_PLATFORMS:
        warnings.append("Platform is outside the approved fictional platform list.")

    if not str(post.get("category", "")).strip():
        warnings.append("Category is blank.")

    found_brands = sorted(term for term in REAL_BRAND_TERMS if term in combined)
    if found_brands:
        warnings.append("Possible real brand/platform: " + ", ".join(found_brands))

    found_placeholders = sorted(
        term for term in PLACEHOLDER_TERMS if term in combined
    )
    if found_placeholders or PLACEHOLDER_HANDLE_RE.search(combined):
        rendered = ", ".join(found_placeholders) or "generic handle pattern"
        warnings.append("Placeholder or generic identity: " + rendered)

    if URL_RE.search(combined):
        warnings.append("Live-looking URL detected; prefer [link removed].")

    if EMAIL_RE.search(text):
        warnings.append("Email address detected; remove usable contact details.")

    if PHONE_RE.search(text):
        warnings.append("Phone-number-like sequence detected.")

    if LONG_NUMBER_RE.search(text) or SORT_CODE_RE.search(text):
        warnings.append("Usable-looking account, bank, card or routing number detected.")

    action = str(post.get("correctAction", ""))
    day = int(post.get("day", 1))
    reason = str(post.get("correctEscalationReason", ""))
    specialist = str(post.get("correctSpecialistReason", ""))
    acceptable = {str(item) for item in post.get("acceptableEscalationReasons", []) or []}

    if not str(post.get("explanation", "")).strip():
        warnings.append("Explanation is blank.")

    if day >= 3 and action == "Escalate" and not reason:
        warnings.append("Day 3+ escalated post has no escalation reason.")

    if day >= 10 and action == "Escalate" and reason == "MisinformationPublicHarm" and not specialist:
        warnings.append("Day 10+ misinformation escalation has no specialist reason.")

    if specialist and day < 10:
        warnings.append("Specialist reason is set before Day 10 unlock.")

    if action != "Escalate" and reason:
        warnings.append("Non-escalated post contains an escalation reason.")

    if day >= 3 and FRAUD_REQUEST_RE.search(combined) and (action == "Remove" or reason != "FraudScam"):
        if not any(phrase in combined for phrase in ("do not reply", "don't reply", "scam alert", "warning about", "asking whether")):
            warnings.append("Policy heuristic: scam/payment/private-data signals may need Escalate -> FraudScam.")

    if day >= 3 and DANGEROUS_CHALLENGE_RE.search(combined) and (action == "Remove" or reason == "ThreatViolence"):
        if not any(phrase in combined for phrase in ("do not attempt", "do not try", "warns viewers not to", "not to attempt")):
            warnings.append("Policy heuristic: dangerous challenge may need Escalate -> MisinformationPublicHarm/PublicSafety.")

    if day >= 3 and HEALTH_HARM_RE.search(combined) and (action == "Remove" or reason != "MisinformationPublicHarm"):
        warnings.append("Policy heuristic: harmful health misinformation may need Escalate -> MisinformationPublicHarm.")

    if reason == "ThreatViolence" and not THREAT_LANGUAGE_RE.search(combined):
        warnings.append("Policy heuristic: ThreatViolence lacks clear threat/planning/incitement language.")

    if day >= 3 and HARASSMENT_ESCALATION_RE.search(combined) and action in {"Approve", "Remove"}:
        warnings.append("Policy heuristic: persistent harassment/brigading may need Escalate -> HarassmentAbuse.")

    if day >= 3 and FIRST_PERSON_CRISIS_RE.search(combined) and action == "Remove":
        warnings.append("Policy heuristic: first-person crisis language may need Escalate -> SelfHarmCrisis.")

    if day >= 3 and PRIVACY_SIGNAL_RE.search(combined):
        has_privacy = reason == "PrivacySensitiveInfo" or "PrivacySensitiveInfo" in acceptable
        has_fraud_privacy = reason == "FraudScam" and "PrivacySensitiveInfo" in acceptable
        if action == "Escalate" and not (has_privacy or has_fraud_privacy):
            warnings.append("Policy heuristic: privacy signals should include PrivacySensitiveInfo as primary or acceptable.")

    if action == "Approve" and "[link removed]" in text.casefold():
        warnings.append("Approved post contains [link removed]; it is probably unnecessary.")

    explanation_lower = explanation.casefold()
    if action == "Approve" and any(
        phrase in explanation_lower
        for phrase in ("violates", "should be removed", "requires removal", "requires escalation")
    ):
        warnings.append("Action/explanation mismatch: explanation describes a violation.")

    if action == "Remove" and "should be approved" in explanation_lower:
        warnings.append("Action/explanation mismatch: explanation says approve.")

    if action == "Escalate" and "should be removed" in explanation_lower:
        warnings.append("Action/explanation mismatch: explanation says remove.")

    text_lower = text.casefold()
    if (
        post.get("category") == "Misinformation"
        and action == "Remove"
        and any(
            phrase in text_lower
            for phrase in (
                "do not try this", "dangerous misinformation",
                "the claim is false", "fact-check", "fact check",
                "has been debunked", "warning: a viral video claims",
            )
        )
    ):
        warnings.append(
            "Possible debunking post: the text may warn about misinformation rather than spread it."
        )

    if (
        post.get("category") == "Self-Harm"
        and action == "Escalate"
        and re.search(
            r"(?i)\b(?:heart attack|chest pain|can't breathe|ambulance|stroke|seizure)\b",
            text,
        )
        and not re.search(
            r"(?i)\b(?:suicid|self[- ]?harm|hurt myself|end my life|goodbye|"
            r"won't be here|not safe on my own|can't go on|starv|purging|overdose)\b",
            text,
        )
    ):
        warnings.append("Likely general medical emergency rather than Self-Harm / Crisis.")

    if (
        re.search(r"(?i)\b(?:dog|cat|animal|pet|horse|rabbit|bird)\b", text)
        and re.search(
            r"(?i)\b(?:burn alive|set .* on fire|matches|solvent|inside .* cage|watch .* suffer)\b",
            text,
        )
    ):
        warnings.append("Animal-cruelty wording may be too graphic or method-specific.")

    tags = {str(tag) for tag in post.get("tags", [])}

    if re.search(
        r"(?i)\b(?:cancer|chemo(?:therapy)?|radiotherapy|tumou?r|oncology)\b",
        text,
    ) and "Cancer" not in tags:
        warnings.append(
            "Cancer-related content is visible but the Cancer tag is missing."
        )

    if re.search(
        r"(?i)\b(?:fertility|infertility|conceiv|pregnant|get pregnant)\b",
        text,
    ) and "Fertility" not in tags:
        warnings.append(
            "Fertility content is visible but the Fertility tag is missing."
        )

    if re.search(r"(?i)\bmenopaus", text) and "Menopause" not in tags:
        warnings.append(
            "Menopause content is visible but the Menopause tag is missing."
        )

    if post.get("category") == "Self-Harm" and re.search(
        r"(?i)\b(?:suicid|end my life|ending it all|won't be here|"
        r"not going to be here|goodbye)\b",
        text,
    ):
        if "SelfHarm" not in tags:
            warnings.append(
                "Self-harm content is visible but the SelfHarm tag is missing."
            )
        if "Suicide" not in tags:
            warnings.append(
                "Suicide-related content is visible but the Suicide tag is missing."
            )

    if re.search(
        r"(?i)\b(?:eating disorder|starv|purging|binge|body image|"
        r"restrictive eating)\b",
        text,
    ) and "EatingDisorders" not in tags:
        warnings.append(
            "Eating-disorder content may require the EatingDisorders tag."
        )

    if re.search(
        r"(?i)\b(?:animal cruelty|cruelty|cull the stray|poison bait|"
        r"neglecting the animal)\b",
        text,
    ) and "AnimalCruelty" not in tags:
        warnings.append(
            "Animal-cruelty content is visible but the AnimalCruelty tag is missing."
        )

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
        edited_post = {
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
            "day": st.session_state.get(
                f"{post_id}-day", post.get("day", 1)
            ),
            "correctEscalationReason": st.session_state.get(
                f"{post_id}-reason",
                post.get("correctEscalationReason", ""),
            ),
            "allowNeedsReviewEscalation": st.session_state.get(
                f"{post_id}-allow-needs-review",
                post.get("allowNeedsReviewEscalation", False),
            ),
            "scenario": st.session_state.get(
                f"{post_id}-scenario", post.get("scenario", "")
            ),
            "tags": list(
                st.session_state.get(
                    f"{post_id}-tags",
                    post.get("tags", []),
                )
            ),
            "correctSpecialistReason": st.session_state.get(
                f"{post_id}-specialist",
                post.get("correctSpecialistReason", ""),
            ),
            "acceptableSpecialistReasons": list(
                st.session_state.get(
                    f"{post_id}-acceptable-specialists",
                    post.get("acceptableSpecialistReasons", []),
                )
            ),
            "acceptableEscalationReasons": list(
                st.session_state.get(
                    f"{post_id}-acceptable-parents",
                    post.get("acceptableEscalationReasons", []),
                )
            ),
            **{
                field: st.session_state.get(
                    f"{post_id}-metadata-{field}",
                    post.get(field, ""),
                )
                for field in METADATA_FIELDS
            },
        }
        edited_post = normalise_review_post(edited_post)
        items[post_id] = {
            "decision": st.session_state.get(f"{post_id}-decision", "Pending"),
            "reviewNotes": st.session_state.get(f"{post_id}-notes", ""),
            "post": edited_post,
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
            f"{post_id}-allow-needs-review": coerce_bool(
                edited.get(
                    "allowNeedsReviewEscalation",
                    post.get("allowNeedsReviewEscalation", False),
                )
            ),
            f"{post_id}-scenario": edited.get(
                "scenario", post.get("scenario", "")
            ),
            f"{post_id}-tags": canonicalise_tags(
                edited.get("tags", post.get("tags", [])) or []
            ),
            f"{post_id}-specialist": edited.get(
                "correctSpecialistReason",
                post.get("correctSpecialistReason", ""),
            ),
            f"{post_id}-acceptable-specialists": list(
                edited.get(
                    "acceptableSpecialistReasons",
                    post.get("acceptableSpecialistReasons", []),
                ) or []
            ),
            f"{post_id}-acceptable-parents": list(
                edited.get(
                    "acceptableEscalationReasons",
                    post.get("acceptableEscalationReasons", []),
                ) or []
            ),
            **{
                f"{post_id}-metadata-{field}": (
                    coerce_int(edited.get(field, post.get(field, 0)))
                    if field in NUMERIC_METADATA_FIELDS
                    else coerce_bool(
                        edited.get(field, post.get(field, False))
                    )
                    if field == "verifiedStatus"
                    else str(edited.get(field, post.get(field, "")))
                )
                for field in METADATA_FIELDS
            },
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
        f"# Review Report â€” {candidate.name}",
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
        "| ID | Decision | Action | Difficulty | Tags | Notes |",
        "|---|---|---|---|---|---|",
    ]

    for post_id, item in items.items():
        post = item["post"]
        notes = str(item.get("reviewNotes", "")).replace("|", "\\|")
        tags = ", ".join(str(tag) for tag in post.get("tags", []))
        tags = tags.replace("|", "\\|")
        lines.append(
            f"| {post_id} | {item['decision']} | "
            f"{post.get('correctAction', '')} | "
            f"{post.get('difficulty', '')} | {tags} | {notes} |"
        )

    return "\n".join(lines) + "\n"


st.set_page_config(
    page_title="Moderation Game Content Review",
    page_icon="ðŸ§¾",
    layout="wide",
)

st.title("Moderation Game â€” Candidate Review")
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

if st.sidebar.button("Auto-fill suggested sensitivity tags"):
    for post in posts:
        post_id = str(post.get("id", ""))
        current = {
            **post,
            "text": st.session_state.get(f"{post_id}-text", post.get("text", "")),
            "scenario": st.session_state.get(
                f"{post_id}-scenario", post.get("scenario", "")
            ),
            "tags": st.session_state.get(f"{post_id}-tags", post.get("tags", [])),
        }
        st.session_state[f"{post_id}-tags"] = suggested_sensitivity_tags(current)
    st.rerun()

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
        "allowNeedsReviewEscalation": st.session_state[
            f"{post_id}-allow-needs-review"
        ],
        "scenario": st.session_state[f"{post_id}-scenario"],
        "tags": list(st.session_state[f"{post_id}-tags"]),
        "correctSpecialistReason": st.session_state[
            f"{post_id}-specialist"
        ],
        "acceptableSpecialistReasons": list(
            st.session_state[f"{post_id}-acceptable-specialists"]
        ),
        "acceptableEscalationReasons": list(
            st.session_state[f"{post_id}-acceptable-parents"]
        ),
        **{
            field: st.session_state[f"{post_id}-metadata-{field}"]
            for field in METADATA_FIELDS
        },
    }

    warnings = warning_flags(current_post)
    title = (
        f"{index}. {post_id} â€” "
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
        current_category = str(
            st.session_state.get(f"{post_id}-category", "")
        )
        category_options = list(CATEGORY_OPTIONS)
        if current_category and current_category not in category_options:
            category_options.append(current_category)
        meta[0].selectbox(
            "Category",
            options=category_options,
            key=f"{post_id}-category",
        )
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

        existing_tags = list(st.session_state.get(f"{post_id}-tags", []))
        tag_options = sorted(set(SENSITIVITY_TAGS) | set(existing_tags))
        st.multiselect(
            "Sensitivity tags",
            options=tag_options,
            key=f"{post_id}-tags",
            help=(
                "Tag what the player is exposed to, including content that is "
                "reported, questioned or debunked."
            ),
        )

        specialist_cols = st.columns(3)
        specialist_cols[0].selectbox(
            "Correct specialist reason (Day 10+)",
            options=SPECIALIST_REASONS,
            key=f"{post_id}-specialist",
        )
        specialist_cols[1].multiselect(
            "Other acceptable specialist reasons",
            options=SPECIALIST_REASONS[1:],
            key=f"{post_id}-acceptable-specialists",
        )
        specialist_cols[2].checkbox(
            "Allow Needs Review",
            key=f"{post_id}-allow-needs-review",
        )

        st.multiselect(
            "Other acceptable parent escalation reasons",
            options=PARENT_ESCALATION_REASONS,
            key=f"{post_id}-acceptable-parents",
        )

        with st.expander("Account metadata (Day 6+)", expanded=False):
            metadata_cols = st.columns(3)
            labels = {
                "accountAgeDays": "Account age (days)",
                "followerCount": "Followers",
                "followingCount": "Following",
                "verifiedStatus": "Verified status",
                "postCount": "Post count",
                "bio": "Biography",
                "previousFlags": "Previous flags",
                "location": "Location",
                "platform": "Platform",
            }
            for metadata_index, field in enumerate(METADATA_FIELDS):
                column = metadata_cols[metadata_index % 3]
                if field in NUMERIC_METADATA_FIELDS:
                    column.number_input(
                        labels[field],
                        min_value=0,
                        step=1,
                        key=f"{post_id}-metadata-{field}",
                    )
                elif field == "verifiedStatus":
                    column.checkbox(
                        labels[field],
                        key=f"{post_id}-metadata-{field}",
                    )
                elif field == "location":
                    current_location = str(
                        st.session_state.get(
                            f"{post_id}-metadata-{field}", ""
                        )
                    )
                    options = list(APPROVED_FICTIONAL_LOCATIONS)
                    if current_location and current_location not in options:
                        options.append(current_location)
                    column.selectbox(
                        labels[field],
                        options=options,
                        key=f"{post_id}-metadata-{field}",
                    )
                elif field == "platform":
                    current_platform = str(
                        st.session_state.get(
                            f"{post_id}-metadata-{field}", ""
                        )
                    )
                    options = list(APPROVED_FICTIONAL_PLATFORMS)
                    if current_platform and current_platform not in options:
                        options.append(current_platform)
                    column.selectbox(
                        labels[field],
                        options=options,
                        key=f"{post_id}-metadata-{field}",
                    )
                else:
                    column.text_input(
                        labels[field],
                        key=f"{post_id}-metadata-{field}",
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
        blocking_warnings: list[str] = []
        for approved_post in approved_posts:
            post_id = str(approved_post.get("id", "Unknown"))
            for warning in warning_flags(approved_post):
                if warning.startswith(
                    (
                        "Real-world place name detected:",
                        "Username contains a platform name.",
                        "Location is outside",
                        "Platform is outside",
                        "Category is blank.",
                    )
                ):
                    blocking_warnings.append(f"{post_id}: {warning}")
        if blocking_warnings:
            st.error(
                "Export blocked by fictional-world/schema checks:\n\n- "
                + "\n- ".join(blocking_warnings)
            )
            st.stop()

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


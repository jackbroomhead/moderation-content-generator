from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

META_FIELDS = {"id", "why", "notesToAppend", "minimumUnlockDay", "removeTags", "requiresSpecialistReason"}
LIST_FIELDS = {"tags", "acceptableEscalationReasons", "acceptableSpecialistReasons"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_note(existing: str, addition: str) -> str:
    existing = (existing or "").strip()
    addition = (addition or "").strip()
    if not addition:
        return existing
    if addition in existing:
        return existing
    return addition if not existing else existing + "\n" + addition


def normalise_overrides_payload(payload: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(payload, dict):
        return {}
    posts = payload.get("posts", payload)
    if not isinstance(posts, dict):
        return {}
    return {str(k): dict(v) for k, v in posts.items() if isinstance(v, dict)}


def load_current_posts(path: Path) -> dict[str, dict[str, Any]]:
    payload = load_json(path)
    posts = payload.get("posts", []) if isinstance(payload, dict) else []
    if not isinstance(posts, list):
        raise ValueError(f"{path} does not contain a posts array")
    by_id: dict[str, dict[str, Any]] = {}
    duplicate_ids: list[str] = []
    for post in posts:
        if not isinstance(post, dict):
            continue
        post_id = str(post.get("id", ""))
        if not post_id:
            continue
        if post_id in by_id:
            duplicate_ids.append(post_id)
        by_id[post_id] = post
    if duplicate_ids:
        raise ValueError("Duplicate post IDs in current approved library: " + ", ".join(sorted(set(duplicate_ids))))
    return by_id


def effective_post(current: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(current)
    merged.update(override)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply policy quality correction set to v4 override file.")
    parser.add_argument("--corrections", default="content-corrections/v4/policy-quality-backfill-v1.json")
    parser.add_argument("--current-library", default="content-library/v4/approved/all-approved-posts-v4.json")
    parser.add_argument("--overrides", default="config/v4_overrides.json")
    args = parser.parse_args()

    root = Path.cwd()
    corrections_path = (root / args.corrections).resolve()
    current_library_path = (root / args.current_library).resolve()
    overrides_path = (root / args.overrides).resolve()

    correction_payload = load_json(corrections_path)
    corrections = correction_payload.get("corrections", [])
    if not isinstance(corrections, list):
        raise ValueError("Correction set must contain a corrections array")

    current_by_id = load_current_posts(current_library_path)
    overrides_payload = load_json(overrides_path) if overrides_path.exists() else {"posts": {}}
    overrides = normalise_overrides_payload(overrides_payload)

    correction_ids = set()
    changed_posts: list[str] = []
    missing_ids: list[str] = []
    report_lines: list[str] = [f"Correction set: {correction_payload.get('correctionSetId', corrections_path.stem)}"]

    for correction in corrections:
        if not isinstance(correction, dict):
            raise ValueError("Each correction must be an object")
        post_id = str(correction.get("id", "")).strip()
        if not post_id:
            raise ValueError("Correction with missing id")
        if post_id in correction_ids:
            raise ValueError(f"Duplicate correction id: {post_id}")
        correction_ids.add(post_id)
        if post_id not in current_by_id:
            missing_ids.append(post_id)
            continue

        existing_override = dict(overrides.get(post_id, {}))
        before = effective_post(current_by_id[post_id], existing_override)
        updated = dict(existing_override)

        if "minimumUnlockDay" in correction:
            updated["day"] = int(correction["minimumUnlockDay"])

        for key, value in correction.items():
            if key in META_FIELDS:
                continue
            updated[key] = list(value) if key in LIST_FIELDS and isinstance(value, list) else value

        if "removeTags" in correction:
            remove = {str(tag) for tag in correction.get("removeTags", [])}
            tags = list(before.get("tags", [])) if isinstance(before.get("tags", []), list) else []
            updated["tags"] = [tag for tag in tags if str(tag) not in remove]

        if "notesToAppend" in correction:
            updated["notes"] = append_note(str(before.get("notes", "")), str(correction.get("notesToAppend", "")))

        after = effective_post(current_by_id[post_id], updated)
        diffs: list[str] = []
        for key in sorted(set(before) | set(after)):
            if before.get(key) != after.get(key):
                diffs.append(f"{key}: {before.get(key)!r} -> {after.get(key)!r}")

        if diffs:
            overrides[post_id] = updated
            changed_posts.append(post_id)
            report_lines.append(post_id)
            report_lines.extend("  " + diff for diff in diffs)
        else:
            report_lines.append(f"{post_id}: no effective change")

    if missing_ids:
        print("Correction IDs not found: " + ", ".join(missing_ids), file=sys.stderr)
        return 1

    for post_id, override in overrides.items():
        base = current_by_id.get(post_id)
        if not base:
            continue
        post = effective_post(base, override)
        action = str(post.get("correctAction", ""))
        day = int(post.get("day", 0) or 0)
        if action not in {"Approve", "Remove", "Escalate"}:
            raise ValueError(f"{post_id}: invalid correctAction {action!r}")
        if action == "Escalate" and day >= 3 and not str(post.get("correctEscalationReason", "")).strip():
            raise ValueError(f"{post_id}: Day 3+ Escalate post still has no correctEscalationReason")

    output_payload = {"posts": {key: overrides[key] for key in sorted(overrides)}}
    write_json(overrides_path, output_payload)

    report_path = corrections_path.with_name(corrections_path.stem + "-application-report.txt")
    report_lines.append("")
    report_lines.append(f"Changed posts: {len(changed_posts)}")
    report_lines.append("Changed IDs: " + (", ".join(changed_posts) if changed_posts else "None"))
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    write_json(corrections_path.with_name(corrections_path.stem + "-application-report.json"), {
        "changedPosts": changed_posts,
        "missingIds": missing_ids,
    })

    print(f"Applied {len(changed_posts)} corrected posts to {overrides_path}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

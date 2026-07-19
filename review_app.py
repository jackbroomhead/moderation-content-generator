from __future__ import annotations

import json
import re
from datetime import datetime
from dataclasses import dataclass
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
AUTOMATION_LOG_DIR = ROOT / "output" / "automation-logs"
APPROVED_DIR = ROOT / "output" / "approved"
REVIEW_DIR = ROOT / "output" / "reviews"
REVIEW_STATE_DIR = ROOT / "output" / "review-state"
REVIEW_EXPORT_DIR = ROOT / "output" / "review-exports"
REPORT_DIR = ROOT / "output" / "review-reports"

for folder in (
    CANDIDATE_DIR,
    APPROVED_DIR,
    REVIEW_DIR,
    REVIEW_STATE_DIR,
    REVIEW_EXPORT_DIR,
    REPORT_DIR,
):
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
CANDIDATE_NAME_RE = re.compile(
    r"^day(?P<day>\d+)-(?P<label>.+)-(?P<timestamp>\d{8}-\d{6})\.json$"
)
GENERATION_MANIFEST_RE = re.compile(
    r"^generation-(?P<run_id>\d{8}-\d{6})-manifest\.json$"
)


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
    r"weapon|knife|gun|hammer|attack|hurt|smash|smashing|burn|set fire|kill|shoot|stab|bomb|poison baits?|cull the stray|locking .* in the shed|confrontation|settle the score|deal' with anyone|"
    r"target|outside .{0,40} at \d|tonight|tomorrow)\b"
)
HARASSMENT_ESCALATION_RE = re.compile(
    r"(?i)\b(?:coordinated (?:harassment|abuse|attack|campaign|brigad(?:e|ing))|brigad(?:e|ing)|mass report|report every|repeatedly|"
    r"keeps messaging|asked (?:him|her|them|you) to stop|after i blocked|"
    r"new accounts?|stalking|following me|won't leave me alone|flood(?:ed)?"
    r" (?:my )?(?:dms|messages))\b"
)
FIRST_PERSON_CRISIS_RE = re.compile(
    r"(?i)\b(?:i (?:do not|don't) think i am safe|i have taken|i took|"
    r"i(?:'|\u2019)m going to hurt myself|hurt myself|make myself disappear|"
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


@dataclass(frozen=True)
class ReviewPost:
    post: dict[str, Any]
    source_file: Path
    review_key: str


@dataclass(frozen=True)
class GenerationRun:
    run_id: str
    label: str
    candidate_files: list[Path]
    source: str
    started_at: str = ""


def candidate_metadata(path: Path) -> dict[str, Any]:
    match = CANDIDATE_NAME_RE.match(path.name)
    if not match:
        return {
            "day": 0,
            "label": "candidate",
            "timestamp": "",
            "datetime": datetime.fromtimestamp(path.stat().st_mtime),
        }

    timestamp = match.group("timestamp")
    parsed = datetime.strptime(timestamp, "%Y%m%d-%H%M%S")
    return {
        "day": int(match.group("day")),
        "label": match.group("label"),
        "timestamp": timestamp,
        "datetime": parsed,
    }


def load_posts_from_candidate(path: Path) -> list[dict[str, Any]]:
    payload = load_json(path)
    posts = payload.get("posts", [])
    if not isinstance(posts, list):
        return []
    return posts


def count_posts(candidate_files: list[Path]) -> int:
    total = 0
    for candidate in candidate_files:
        try:
            total += len(load_posts_from_candidate(candidate))
        except (OSError, json.JSONDecodeError):
            pass
    return total


def review_key_for(source_file: Path, post: dict[str, Any]) -> str:
    return f"{source_file.name}::{post.get('id', '')}"


def load_run_from_manifest(manifest_path: Path) -> GenerationRun | None:
    match = GENERATION_MANIFEST_RE.match(manifest_path.name)
    if not match:
        return None

    try:
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError):
        return None

    candidates: list[Path] = []
    profiles: list[str] = []
    for result in manifest.get("results", []) or []:
        candidate_text = result.get("candidate")
        if not candidate_text:
            continue
        candidate = Path(candidate_text)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        if candidate.exists() and candidate.parent == CANDIDATE_DIR:
            candidates.append(candidate)
        profile = str(result.get("profile") or "").strip()
        if profile:
            profiles.append(profile)

    if not candidates:
        return None

    unique_candidates = sorted(
        set(candidates),
        key=lambda path: (
            candidate_metadata(path)["day"],
            candidate_metadata(path)["timestamp"],
            path.name,
        ),
    )
    friendly = "smoke test" if any("smoke" in item.casefold() for item in profiles) else "generation"
    run_id = match.group("run_id")
    return GenerationRun(
        run_id=run_id,
        label=f"{run_id} {friendly}",
        candidate_files=unique_candidates,
        source="manifest",
        started_at=run_id,
    )


def discover_generation_runs(candidate_files: list[Path]) -> list[GenerationRun]:
    runs: list[GenerationRun] = []
    assigned: set[Path] = set()

    for manifest_path in sorted(
        AUTOMATION_LOG_DIR.glob("generation-*-manifest.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    ):
        run = load_run_from_manifest(manifest_path)
        if not run:
            continue
        runs.append(run)
        assigned.update(run.candidate_files)

    orphan_files = [
        path for path in candidate_files
        if path not in assigned and CANDIDATE_NAME_RE.match(path.name)
    ]
    orphan_files.sort(key=lambda path: candidate_metadata(path)["datetime"])

    group: list[Path] = []
    group_label = ""
    group_start: datetime | None = None
    previous_time: datetime | None = None

    def flush_group() -> None:
        nonlocal group, group_label, group_start, previous_time
        if not group or group_start is None:
            return
        run_id = group_start.strftime("%Y%m%d-%H%M%S")
        runs.append(
            GenerationRun(
                run_id=f"nearby-{run_id}",
                label=f"{run_id} {group_label} nearby files",
                candidate_files=sorted(
                    group,
                    key=lambda path: (
                        candidate_metadata(path)["day"],
                        candidate_metadata(path)["timestamp"],
                        path.name,
                    ),
                ),
                source="nearby timestamp",
                started_at=run_id,
            )
        )
        group = []
        group_label = ""
        group_start = None
        previous_time = None

    for candidate in orphan_files:
        metadata = candidate_metadata(candidate)
        current_time = metadata["datetime"]
        current_label = str(metadata["label"])
        same_group = (
            group
            and current_label == group_label
            and previous_time is not None
            and (current_time - previous_time).total_seconds() <= 600
        )
        if not group:
            group = [candidate]
            group_label = current_label
            group_start = current_time
            previous_time = current_time
        elif same_group:
            group.append(candidate)
            previous_time = current_time
        else:
            flush_group()
            group = [candidate]
            group_label = current_label
            group_start = current_time
            previous_time = current_time
    flush_group()

    unmatched = [
        path for path in candidate_files
        if path not in assigned
        and not any(path in run.candidate_files for run in runs)
    ]
    for candidate in unmatched:
        metadata = candidate_metadata(candidate)
        run_id = metadata["timestamp"] or candidate.stem
        runs.append(
            GenerationRun(
                run_id=f"single-{run_id}",
                label=f"{run_id} single file",
                candidate_files=[candidate],
                source="single file fallback",
                started_at=run_id,
            )
        )

    return sorted(
        runs,
        key=lambda run: max(path.stat().st_mtime for path in run.candidate_files),
        reverse=True,
    )


def build_review_posts(candidate_files: list[Path], keyed_by_source: bool) -> list[ReviewPost]:
    review_posts: list[ReviewPost] = []
    for candidate in candidate_files:
        for index, post in enumerate(load_posts_from_candidate(candidate), start=1):
            post_id = str(post.get("id", f"POST-{index}"))
            key = review_key_for(candidate, post) if keyed_by_source else post_id
            review_posts.append(
                ReviewPost(
                    post={**post, "id": post_id},
                    source_file=candidate,
                    review_key=key,
                )
            )
    return review_posts


def day_label(day: int) -> str:
    return f"Day {day}" if day else "Unknown day"


def warning_flags(post: dict[str, Any]) -> list[str]:
    author = str(post.get("author") or "")
    text = str(post.get("text") or "")
    text_lower = text.casefold()
    explanation = str(post.get("explanation") or "")
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

    boundary_setting = any(phrase in text_lower for phrase in ("leave me alone", "back off", "stop following me", "keep harassing me", "keeps harassing me"))
    if day >= 3 and HARASSMENT_ESCALATION_RE.search(text) and action in {"Approve", "Remove"} and not boundary_setting:
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


def review_state_file_for(run: GenerationRun) -> Path:
    safe_id = re.sub(r"[^A-Za-z0-9_.-]+", "-", run.run_id).strip("-")
    return REVIEW_STATE_DIR / f"review-run-{safe_id}.json"


def load_saved_run_review(run: GenerationRun) -> dict[str, Any]:
    review_path = review_state_file_for(run)
    if review_path.exists():
        return load_json(review_path)
    return {
        "runId": run.run_id,
        "candidates": [path.name for path in run.candidate_files],
        "items": {},
    }


def build_review_payload(
    candidate: Path,
    review_posts: list[ReviewPost],
    include_source_metadata: bool = False,
) -> dict[str, Any]:
    items: dict[str, Any] = {}
    for review_post in review_posts:
        post = review_post.post
        post_id = str(post.get("id", ""))
        key = review_post.review_key
        edited_post = {
            **post,
            "author": st.session_state.get(
                f"{key}-author", post.get("author", "")
            ),
            "text": st.session_state.get(
                f"{key}-text", post.get("text", "")
            ),
            "category": st.session_state.get(
                f"{key}-category", post.get("category", "")
            ),
            "correctAction": st.session_state.get(
                f"{key}-action", post.get("correctAction", "")
            ),
            "difficulty": st.session_state.get(
                f"{key}-difficulty", post.get("difficulty", "")
            ),
            "explanation": st.session_state.get(
                f"{key}-explanation", post.get("explanation", "")
            ),
            "day": st.session_state.get(
                f"{key}-day", post.get("day", 1)
            ),
            "correctEscalationReason": st.session_state.get(
                f"{key}-reason",
                post.get("correctEscalationReason", ""),
            ),
            "allowNeedsReviewEscalation": st.session_state.get(
                f"{key}-allow-needs-review",
                post.get("allowNeedsReviewEscalation", False),
            ),
            "scenario": st.session_state.get(
                f"{key}-scenario", post.get("scenario", "")
            ),
            "tags": list(
                st.session_state.get(
                    f"{key}-tags",
                    post.get("tags", []),
                )
            ),
            "correctSpecialistReason": st.session_state.get(
                f"{key}-specialist",
                post.get("correctSpecialistReason", ""),
            ),
            "acceptableSpecialistReasons": list(
                st.session_state.get(
                    f"{key}-acceptable-specialists",
                    post.get("acceptableSpecialistReasons", []),
                )
            ),
            "acceptableEscalationReasons": list(
                st.session_state.get(
                    f"{key}-acceptable-parents",
                    post.get("acceptableEscalationReasons", []),
                )
            ),
            **{
                field: st.session_state.get(
                    f"{key}-metadata-{field}",
                    post.get(field, ""),
                )
                for field in METADATA_FIELDS
            },
        }
        edited_post = normalise_review_post(edited_post)
        item_payload = {
            "decision": st.session_state.get(f"{key}-decision", "Pending"),
            "reviewNotes": st.session_state.get(f"{key}-notes", ""),
            "post": edited_post,
        }
        if include_source_metadata:
            item_payload["sourceFile"] = review_post.source_file.name
            item_payload["postId"] = post_id
        items[key] = item_payload

    return {
        "candidate": candidate.name,
        "savedAt": datetime.now().isoformat(timespec="seconds"),
        "items": items,
    }


def build_run_review_payload(
    run: GenerationRun,
    review_posts: list[ReviewPost],
) -> dict[str, Any]:
    payload = build_review_payload(
        run.candidate_files[0],
        review_posts,
        include_source_metadata=True,
    )
    payload.pop("candidate", None)
    payload["runId"] = run.run_id
    payload["runLabel"] = run.label
    payload["runSource"] = run.source
    payload["candidates"] = [path.name for path in run.candidate_files]
    return payload


def initialise_session(
    review_posts: list[ReviewPost],
    saved: dict[str, Any],
) -> None:
    saved_items = saved.get("items", {})
    for review_post in review_posts:
        post = review_post.post
        post_id = str(post.get("id", ""))
        key = review_post.review_key
        existing = saved_items.get(key, {})
        edited = existing.get("post", post)

        defaults = {
            f"{key}-decision": existing.get("decision", "Pending"),
            f"{key}-notes": existing.get("reviewNotes", ""),
            f"{key}-author": edited.get("author", post.get("author", "")),
            f"{key}-text": edited.get("text", post.get("text", "")),
            f"{key}-category": edited.get(
                "category", post.get("category", "")
            ),
            f"{key}-action": edited.get(
                "correctAction", post.get("correctAction", "")
            ),
            f"{key}-difficulty": edited.get(
                "difficulty", post.get("difficulty", "")
            ),
            f"{key}-explanation": edited.get(
                "explanation", post.get("explanation", "")
            ),
            f"{key}-day": int(edited.get("day", post.get("day", 1))),
            f"{key}-reason": edited.get(
                "correctEscalationReason",
                post.get("correctEscalationReason", ""),
            ),
            f"{key}-allow-needs-review": coerce_bool(
                edited.get(
                    "allowNeedsReviewEscalation",
                    post.get("allowNeedsReviewEscalation", False),
                )
            ),
            f"{key}-scenario": edited.get(
                "scenario", post.get("scenario", "")
            ),
            f"{key}-tags": canonicalise_tags(
                edited.get("tags", post.get("tags", [])) or []
            ),
            f"{key}-specialist": edited.get(
                "correctSpecialistReason",
                post.get("correctSpecialistReason", ""),
            ),
            f"{key}-acceptable-specialists": list(
                edited.get(
                    "acceptableSpecialistReasons",
                    post.get("acceptableSpecialistReasons", []),
                ) or []
            ),
            f"{key}-acceptable-parents": list(
                edited.get(
                    "acceptableEscalationReasons",
                    post.get("acceptableEscalationReasons", []),
                ) or []
            ),
            **{
                f"{key}-metadata-{field}": (
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


def approved_posts_from(review_payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item["post"]
        for item in review_payload["items"].values()
        if item["decision"] in {"Approve", "Edit"}
    ]


def pending_count_from(review_payload: dict[str, Any]) -> int:
    return sum(
        1
        for item in review_payload["items"].values()
        if item["decision"] == "Pending"
    )


def blocking_export_warnings(approved_posts: list[dict[str, Any]]) -> list[str]:
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
    return blocking_warnings


def source_label(review_post: ReviewPost) -> str:
    metadata = candidate_metadata(review_post.source_file)
    day = metadata["day"] or coerce_int(review_post.post.get("day", 0))
    return f"{review_post.source_file.name} / {day_label(day)}"


def current_post_from_session(review_post: ReviewPost) -> dict[str, Any]:
    post = review_post.post
    key = review_post.review_key
    return {
        **post,
        "author": st.session_state[f"{key}-author"],
        "text": st.session_state[f"{key}-text"],
        "category": st.session_state[f"{key}-category"],
        "correctAction": st.session_state[f"{key}-action"],
        "difficulty": st.session_state[f"{key}-difficulty"],
        "explanation": st.session_state[f"{key}-explanation"],
        "day": st.session_state[f"{key}-day"],
        "correctEscalationReason": st.session_state[f"{key}-reason"],
        "allowNeedsReviewEscalation": st.session_state[
            f"{key}-allow-needs-review"
        ],
        "scenario": st.session_state[f"{key}-scenario"],
        "tags": list(st.session_state[f"{key}-tags"]),
        "correctSpecialistReason": st.session_state[
            f"{key}-specialist"
        ],
        "acceptableSpecialistReasons": list(
            st.session_state[f"{key}-acceptable-specialists"]
        ),
        "acceptableEscalationReasons": list(
            st.session_state[f"{key}-acceptable-parents"]
        ),
        **{
            field: st.session_state[f"{key}-metadata-{field}"]
            for field in METADATA_FIELDS
        },
    }


def render_post_editor(
    review_posts: list[ReviewPost],
    warning_cache: dict[str, list[str]] | None = None,
    show_source: bool = False,
) -> None:
    for index, review_post in enumerate(review_posts, start=1):
        post = review_post.post
        post_id = str(post.get("id", f"POST-{index}"))
        key = review_post.review_key
        current_post = current_post_from_session(review_post)

        warnings = warning_cache.get(key) if warning_cache else warning_flags(current_post)
        source = f" - {source_label(review_post)}" if show_source else ""
        title = (
            f"{index}. {post_id}{source} - "
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
                key=f"{key}-decision",
            )
            top[1].number_input(
                "Earliest eligible day",
                min_value=0,
                max_value=99,
                step=1,
                key=f"{key}-day",
            )
            top[2].text_input("Author", key=f"{key}-author")

            st.text_area(
                "Post text",
                height=120,
                key=f"{key}-text",
            )

            meta = st.columns(4)
            current_category = str(
                st.session_state.get(f"{key}-category", "")
            )
            category_options = list(CATEGORY_OPTIONS)
            if current_category and current_category not in category_options:
                category_options.append(current_category)
            meta[0].selectbox(
                "Category",
                options=category_options,
                key=f"{key}-category",
            )
            meta[1].selectbox(
                "Correct action",
                ("Approve", "Remove", "Escalate"),
                key=f"{key}-action",
            )
            meta[2].selectbox(
                "Difficulty",
                ("Easy", "Medium", "Hard"),
                key=f"{key}-difficulty",
            )
            meta[3].text_input(
                "Escalation reason",
                key=f"{key}-reason",
                help="Leave blank unless the correct action is Escalate.",
            )

            existing_tags = list(st.session_state.get(f"{key}-tags", []))
            tag_options = sorted(set(SENSITIVITY_TAGS) | set(existing_tags))
            st.multiselect(
                "Sensitivity tags",
                options=tag_options,
                key=f"{key}-tags",
                help=(
                    "Tag what the player is exposed to, including content that is "
                    "reported, questioned or debunked."
                ),
            )

            specialist_active = (
                st.session_state.get(f"{key}-reason")
                == "MisinformationPublicHarm"
            )
            if not specialist_active:
                st.caption(
                    "Specialist misinformation reason fields are only active for "
                    "MisinformationPublicHarm escalations."
                )
            specialist_cols = st.columns(3)
            specialist_cols[0].selectbox(
                "Specialist misinformation reason",
                options=SPECIALIST_REASONS,
                key=f"{key}-specialist",
                disabled=not specialist_active,
                help=(
                    "Only required for MisinformationPublicHarm escalations from "
                    "Day 10 onward."
                ),
            )
            specialist_cols[1].multiselect(
                "Other acceptable specialist reasons",
                options=SPECIALIST_REASONS[1:],
                key=f"{key}-acceptable-specialists",
                disabled=not specialist_active,
                help=(
                    "Only required for MisinformationPublicHarm escalations from "
                    "Day 10 onward."
                ),
            )
            specialist_cols[2].checkbox(
                "Allow Needs Review",
                key=f"{key}-allow-needs-review",
            )

            st.multiselect(
                "Other acceptable parent escalation reasons",
                options=PARENT_ESCALATION_REASONS,
                key=f"{key}-acceptable-parents",
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
                            key=f"{key}-metadata-{field}",
                        )
                    elif field == "verifiedStatus":
                        column.checkbox(
                            labels[field],
                            key=f"{key}-metadata-{field}",
                        )
                    elif field == "location":
                        current_location = str(
                            st.session_state.get(
                                f"{key}-metadata-{field}", ""
                            )
                        )
                        options = list(APPROVED_FICTIONAL_LOCATIONS)
                        if current_location and current_location not in options:
                            options.append(current_location)
                        column.selectbox(
                            labels[field],
                            options=options,
                            key=f"{key}-metadata-{field}",
                        )
                    elif field == "platform":
                        current_platform = str(
                            st.session_state.get(
                                f"{key}-metadata-{field}", ""
                            )
                        )
                        options = list(APPROVED_FICTIONAL_PLATFORMS)
                        if current_platform and current_platform not in options:
                            options.append(current_platform)
                        column.selectbox(
                            labels[field],
                            options=options,
                            key=f"{key}-metadata-{field}",
                        )
                    else:
                        column.text_input(
                            labels[field],
                            key=f"{key}-metadata-{field}",
                        )

            st.text_area(
                "Scenario/context",
                height=90,
                key=f"{key}-scenario",
            )
            st.text_area(
                "Explanation",
                height=110,
                key=f"{key}-explanation",
            )
            st.text_area(
                "Reviewer notes",
                height=80,
                key=f"{key}-notes",
            )


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
        f"# Review Report - {candidate.name}",
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
    page_icon="R",
    layout="wide",
)

st.title("Moderation Game - Candidate Review")
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

review_mode = st.sidebar.radio(
    "Review mode",
    ("Generation run", "Single candidate file"),
    horizontal=False,
)

run: GenerationRun | None = None
candidate_path: Path | None = None

if review_mode == "Generation run":
    generation_runs = discover_generation_runs(candidate_files)
    if not generation_runs:
        st.warning("No generation runs were found. Falling back to single-file review.")
        review_mode = "Single candidate file"
    else:
        run_labels = {
            (
                f"{item.label} - {count_posts(item.candidate_files)} posts "
                f"({len(item.candidate_files)} files, {item.source})"
            ): item
            for item in generation_runs
        }
        selected_run_label = st.sidebar.selectbox(
            "Generation run",
            list(run_labels),
        )
        run = run_labels[selected_run_label]
        review_posts = build_review_posts(run.candidate_files, keyed_by_source=True)
        active_key = f"active-run::{run.run_id}"
        saved_review = load_saved_run_review(run)

if review_mode == "Single candidate file":
    candidate_names = [path.name for path in candidate_files]
    selected_name = st.sidebar.selectbox("Candidate batch", candidate_names)
    candidate_path = CANDIDATE_DIR / selected_name
    review_posts = build_review_posts([candidate_path], keyed_by_source=False)
    active_key = f"active-candidate::{candidate_path.name}"
    saved_review = load_saved_review(candidate_path)

if not review_posts:
    st.error("Selected candidate input must contain a non-empty posts array.")
    st.stop()

if st.session_state.get("loaded-candidate") != active_key:
    for key in list(st.session_state):
        if key != "loaded-candidate":
            del st.session_state[key]
    st.session_state["loaded-candidate"] = active_key

initialise_session(review_posts, saved_review)

warning_cache = {
    item.review_key: warning_flags(current_post_from_session(item))
    for item in review_posts
}

day_options = sorted(
    {
        coerce_int(current_post_from_session(item).get("day", 0))
        for item in review_posts
    }
)
decision_filter = st.sidebar.selectbox(
    "Decision filter",
    ("All", "Pending", "Approved", "Edited", "Rejected"),
)
day_filter_label = st.sidebar.selectbox(
    "Day filter",
    ["All days"] + [day_label(day) for day in day_options],
)
warnings_only = st.sidebar.checkbox("Warnings only")

decision_map = {
    "Approved": "Approve",
    "Edited": "Edit",
    "Rejected": "Reject",
}
selected_decision = decision_map.get(decision_filter, decision_filter)
selected_day = (
    int(day_filter_label.replace("Day ", ""))
    if day_filter_label.startswith("Day ")
    else None
)

filtered_posts: list[ReviewPost] = []
for item in review_posts:
    key = item.review_key
    current = current_post_from_session(item)
    if selected_day is not None and coerce_int(current.get("day", 0)) != selected_day:
        continue
    if selected_decision != "All" and st.session_state.get(f"{key}-decision") != selected_decision:
        continue
    if warnings_only and not warning_cache[key]:
        continue
    filtered_posts.append(item)

decisions = [
    st.session_state.get(f"{item.review_key}-decision", "Pending")
    for item in review_posts
]
summary_cols = st.columns(6)
summary_cols[0].metric("Total", len(review_posts))
for col, decision in zip(
    summary_cols[1:5], ("Approve", "Edit", "Reject", "Pending")
):
    col.metric(decision, decisions.count(decision))
summary_cols[5].metric(
    "Warnings",
    sum(1 for warnings in warning_cache.values() if warnings),
)

if review_mode == "Generation run" and run:
    day_counts: dict[int, int] = {}
    action_counts: dict[str, int] = {}
    for item in review_posts:
        current = current_post_from_session(item)
        day = coerce_int(current.get("day", 0))
        action = str(current.get("correctAction", "") or "Blank")
        day_counts[day] = day_counts.get(day, 0) + 1
        action_counts[action] = action_counts.get(action, 0) + 1
    st.caption(
        "By day: "
        + ", ".join(f"{day_label(day)} = {count}" for day, count in sorted(day_counts.items()))
        + " | By action: "
        + ", ".join(f"{action} = {count}" for action, count in sorted(action_counts.items()))
    )
    st.caption(
        "Source files: "
        + ", ".join(path.name for path in run.candidate_files)
    )

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Decision meanings**\n\n"
    "- **Approve:** usable without a content change\n"
    "- **Edit:** usable after the edits shown here\n"
    "- **Reject:** exclude from approved export\n"
)

if st.sidebar.button("Auto-fill suggested sensitivity tags"):
    for item in filtered_posts:
        key = item.review_key
        current = {
            **item.post,
            "text": st.session_state.get(f"{key}-text", item.post.get("text", "")),
            "scenario": st.session_state.get(
                f"{key}-scenario", item.post.get("scenario", "")
            ),
            "tags": st.session_state.get(f"{key}-tags", item.post.get("tags", [])),
        }
        st.session_state[f"{key}-tags"] = suggested_sensitivity_tags(current)
    st.rerun()

st.caption(f"Showing {len(filtered_posts)} of {len(review_posts)} posts.")
render_post_editor(
    filtered_posts,
    warning_cache=warning_cache,
    show_source=review_mode == "Generation run",
)

st.markdown("---")

if review_mode == "Generation run" and run:
    review_payload = build_run_review_payload(run, review_posts)
    state_path = review_state_file_for(run)
    export_id = re.sub(r"[^A-Za-z0-9_.-]+", "-", run.run_id).strip("-")
else:
    assert candidate_path is not None
    review_payload = build_review_payload(candidate_path, review_posts)
    state_path = review_file_for(candidate_path)
    export_id = candidate_path.stem

action_cols = st.columns(3)

if action_cols[0].button("Save review progress", type="primary"):
    write_json(state_path, review_payload)
    st.success(f"Saved review progress to {state_path.relative_to(ROOT)}")

approved_posts = approved_posts_from(review_payload)
pending_count = pending_count_from(review_payload)

if action_cols[1].button("Export approved JSON"):
    if pending_count:
        st.error(
            f"{pending_count} post(s) are still Pending. "
            "Review every post before exporting."
        )
    elif not approved_posts:
        st.error("Nothing is approved for export.")
    else:
        blocking_warnings = blocking_export_warnings(approved_posts)
        if blocking_warnings:
            st.error(
                "Export blocked by fictional-world/schema checks:\n\n- "
                + "\n- ".join(blocking_warnings)
            )
            st.stop()

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        if review_mode == "Generation run":
            approved_path = REVIEW_EXPORT_DIR / (
                f"approved-review-run-{export_id}-{timestamp}.json"
            )
            write_json(approved_path, {"posts": approved_posts})
            write_json(state_path, review_payload)
            st.success(
                f"Exported {len(approved_posts)} post(s) to "
                f"{approved_path.relative_to(ROOT)}"
            )
            st.info(
                "This export is a review convenience file only; it is not "
                "merged into the official approved v4 library or published to Unity."
            )
        else:
            assert candidate_path is not None
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
            write_json(state_path, review_payload)
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
    file_name=f"{export_id}-approved.json",
    mime="application/json",
    disabled=not approved_posts,
)

st.caption(
    "The reviewer never changes input/posts.json, original candidate files, "
    "the official approved library, or Unity published content."
)


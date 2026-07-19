from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


NUMERIC_FIELDS = {
    "accountAgeDays",
    "followerCount",
    "followingCount",
    "postCount",
    "previousFlags",
}

BOOLEAN_FIELDS = {
    "verifiedStatus",
    "allowNeedsReviewEscalation",
    "isStoryPost",
}

LIST_FIELDS = {
    "tags",
    "acceptableEscalationReasons",
    "acceptableSpecialistReasons",
}

CONTROLLED_TAGS = {
    "Cancer",
    "Fertility",
    "Pregnancy",
    "Miscarriage",
    "Menopause",
    "EatingDisorders",
    "BodyImage",
    "SelfHarm",
    "Suicide",
    "AnimalCruelty",
    "GraphicViolence",
    "DomesticAbuse",
    "SexualViolence",
    "SubstanceMisuse",
}

APPROVED_LOCATIONS = {
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
}

PLATFORMS = [
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

PLACE_REPLACEMENTS = [
    ("East London", "East Westbridge"),
    ("North Yorkshire", "Moorvale"),
    ("Yorkshire", "Moorvale"),
    ("Pagenham", "Oakhaven East"),
    ("Kent", "Moorvale"),
    ("London", "Westbridge"),
    ("Manchester", "Greyford"),
    ("Birmingham", "Northbridge"),
    ("Leeds", "Oakhaven"),
    ("Liverpool", "Bellmere"),
    ("Bristol", "Bellmere"),
    ("Sheffield", "Greyford"),
    ("Nottingham", "Greyford"),
    ("Derby", "Dunmere"),
    ("Brighton", "Bellmere"),
    ("Luton", "Oakhaven"),
    ("Piccadilly", "Westbridge Central"),
    ("Riverdale", "Oakhaven"),
    ("Ashworth", "Greyford"),
    ("Clifton", "Oakhaven"),
    ("M25", "Oakhaven bypass"),
]

BLOCKED_REAL_PLACES = {
    "london", "manchester", "birmingham", "leeds", "liverpool", "bristol",
    "sheffield", "nottingham", "derby", "brighton", "luton", "york",
    "yorkshire", "north yorkshire", "glasgow", "edinburgh", "cardiff",
    "belfast", "oxford", "cambridge", "newcastle", "leicester", "coventry",
    "southampton", "portsmouth", "plymouth", "swansea",
    "aberdeen", "dundee", "piccadilly", "pagenham", "kent",
}

LOCATION_TOKENS = {
    item.casefold()
    for item in APPROVED_LOCATIONS
    if item and not item.startswith("Near ")
} | BLOCKED_REAL_PLACES | {
    "riverdale", "ashworth", "clifton", "uk"
}

PLATFORM_TOKEN_RE = re.compile(
    r"(?i)\b(?:" + "|".join(re.escape(item) for item in PLATFORMS) + r")\b"
)

CANCER_RE = re.compile(
    r"(?i)\b(?:cancer|chemo(?:therapy)?|radiotherapy|radiation treatment|oncology|tumou?r)\b"
)
FERTILITY_RE = re.compile(r"(?i)\b(?:fertility|infertility|conceiv|pregnan|get pregnant)\b")
PREGNANCY_RE = re.compile(r"(?i)\b(?:pregnan|postpartum|prenatal|miscarriage)\b")
MENOPAUSE_RE = re.compile(r"(?i)\bmenopaus")
EATING_RE = re.compile(r"(?i)\b(?:eating disorder|starv|purging|binge|restrictive eating)\b")
BODY_IMAGE_RE = re.compile(r"(?i)\b(?:body image|weight loss|lose weight|thin|fat)\b")
SELF_HARM_RE = re.compile(
    r"(?i)\b(?:self[- ]?harm|hurt myself|end my life|ending it all|can't go on|"
    r"not safe on my own|goodbye message|overdose|starv|purging)\b"
)
SUICIDE_RE = re.compile(
    r"(?i)\b(?:suicid|end my life|ending it all|won't be here|not going to be here|"
    r"before the sun rises|goodbye to everyone)\b"
)
ANIMAL_CRUELTY_RE = re.compile(
    r"(?i)\b(?:animal cruelty|cruelty|cull the stray|poison bait|wildlife rescue|"
    r"locking .* in the shed|harm the animal|hurt the animal)\b"
)


VALID_PARENT_REASONS = {
    "ThreatViolence",
    "SelfHarmCrisis",
    "HarassmentAbuse",
    "FraudScam",
    "PrivacySensitiveInfo",
    "MisinformationPublicHarm",
}

VALID_SPECIALIST_REASONS = {
    "HealthMedical",
    "CivicElection",
    "PublicSafetyEmergency",
    "FinancialEconomic",
    "SyntheticManipulatedMedia",
}

# Conservative policy-quality heuristics for review triage. They are designed
# to catch common label mistakes, not to replace human policy judgement.
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
PUBLIC_HARM_MISINFO_RE = re.compile(
    r"(?i)\b(?:evacuation order|gas leak|chemical spill|water supply|toxic|"
    r"bridge collapse|emergency shelter|polling station|election (?:cancelled|"
    r"canceled)|ballots?|bank freeze|savings account|withdraw everything|"
    r"emergency tax|transaction(?:s)? .*blocked|public transport .*shut)\b"
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
SPEC_HINT_REASONS = {
    "HealthMedical": re.compile(r"(?i)\b(?:vaccine|doctor|medical|health|clinic|cancer|fertility|treatment|hospital|cure)\b"),
    "CivicElection": re.compile(r"(?i)\b(?:election|polling|ballot|vote|voter)\b"),
    "PublicSafetyEmergency": re.compile(r"(?i)\b(?:evacuation|gas leak|chemical spill|water supply|toxic|bridge collapse|emergency shelter|traffic|quarry|cliff|moving train)\b"),
    "FinancialEconomic": re.compile(r"(?i)\b(?:bank|savings|withdraw|tax|transaction|market|funds|account freeze)\b"),
    "SyntheticManipulatedMedia": re.compile(r"(?i)\b(?:deepfake|synthetic|manipulated|edited video|fake audio|doctored image|viral clip)\b"),
}
REAL_WORLD_REFERENCE_RE = re.compile(
    r"(?i)\b(?:london|leeds|parliament square|southwark)\b|@LondonWatch|@LeedsWatch|#LeedsNews"
)

FIELDS_TO_CLEAN = (
    "author",
    "text",
    "explanation",
    "bio",
    "location",
    "scenario",
    "notes",
)

STANDARD_FIELDS = [
    "id",
    "author",
    "profileImage",
    "text",
    "postImage",
    "category",
    "correctAction",
    "difficulty",
    "explanation",
    "day",
    "tags",
    "scenario",
    "notes",
    "accountAgeDays",
    "followerCount",
    "followingCount",
    "verifiedStatus",
    "postCount",
    "bio",
    "previousFlags",
    "location",
    "platform",
    "correctEscalationReason",
    "acceptableEscalationReasons",
    "allowNeedsReviewEscalation",
    "correctSpecialistReason",
    "acceptableSpecialistReasons",
    "isStoryPost",
]

PERSONAL_HANDLES = [
    "MaraVance",
    "TheoWrites",
    "NinaMakes",
    "RowanField",
    "EliSketches",
    "JulesHarper",
    "SamReads",
    "AshaNotes",
    "MiloCooks",
    "TessaGardens",
    "KieranVale",
    "LenaHart",
    "IvyRowan",
    "JonahReed",
    "MaeveStone",
    "RoryQuill",
    "NoraWren",
    "CallumPike",
    "FreyaMoss",
    "DylanCove",
]

ORG_HANDLES = {
    "Public Information": [
        "CivicNoticeDesk",
        "TransitUpdates",
        "LibraryBulletin",
        "ServiceNotice",
    ],
    "News / Public Event": [
        "LanternEvents",
        "CultureDesk",
        "MarketWeekend",
        "CommunityStage",
    ],
    "Fraud": [
        "SecureAccountDesk",
        "CommunityHopeFund",
        "MarketplaceHelp",
        "ReliefNetwork",
    ],
    "Misinformation": [
        "CivicLens",
        "EvidenceDesk",
        "MediaCheck",
        "PublicClaimWatch",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and validate the frozen v4 approved content library."
    )
    parser.add_argument(
        "--inputs",
        nargs="*",
        default=[],
        help="Approved JSON files. If omitted, output/approved/**/*.json is scanned.",
    )
    parser.add_argument(
        "--approved-dir",
        default="output/approved",
        help="Directory scanned when --inputs is omitted.",
    )
    parser.add_argument(
        "--output-dir",
        default="content-library/v4",
        help="Destination directory for the v4 library.",
    )
    parser.add_argument(
        "--overrides",
        default="config/v4_overrides.json",
        help="Optional targeted override JSON.",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
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


def replace_case_insensitive(text: str, old: str, new: str) -> str:
    return re.sub(rf"\b{re.escape(old)}\b", new, text, flags=re.IGNORECASE)


def clean_world_text(value: Any) -> str:
    text = str(value or "")
    for old, new in PLACE_REPLACEMENTS:
        text = replace_case_insensitive(text, old, new)
    text = text.replace("22:00 BST", "22:00 local time")
    text = text.replace("19:00 BST", "19:00 local time")
    text = re.sub(
        r"(?i)@PublicSquareUser\d+",
        "@RowanVale89",
        text,
    )
    text = re.sub(
        r"(?i)@(?:" + "|".join(re.escape(item) for item in PLATFORMS) + r")\b",
        "the platform",
        text,
    )
    text = PLATFORM_TOKEN_RE.sub("the platform", text)
    text = re.sub(r"\bthe platformUser\d+\b", "@RowanVale89", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def author_is_unsafe(author: str) -> bool:
    lowered = author.casefold()
    if PLATFORM_TOKEN_RE.search(author):
        return True
    if "_uk" in lowered or lowered.endswith("uk"):
        return True
    if re.search(r"(?i)\buser\d+\b", author):
        return True
    return any(
        re.search(rf"\b{re.escape(token)}\b", lowered)
        or token in lowered.replace("_", "").replace("-", "")
        for token in LOCATION_TOKENS
        if len(token) >= 4
    )


def choose_handle(post: dict[str, Any], used: set[str]) -> str:
    category = str(post.get("category", ""))
    candidates = ORG_HANDLES.get(category, PERSONAL_HANDLES)
    digest = int(
        hashlib.sha256(str(post.get("id", "")).encode("utf-8")).hexdigest(),
        16,
    )
    base = candidates[digest % len(candidates)]
    candidate = base
    attempt = 0
    while candidate.casefold() in used:
        attempt += 1
        candidate = f"{base}{17 + ((digest + attempt * 11) % 71)}"
    used.add(candidate.casefold())
    return candidate


def sanitise_author(post: dict[str, Any], used: set[str]) -> str:
    author = str(post.get("author", "")).strip()
    if not author or author_is_unsafe(author) or author.casefold() in used:
        return choose_handle(post, used)
    used.add(author.casefold())
    return author


def clean_tags(post: dict[str, Any]) -> list[str]:
    existing = {
        str(tag)
        for tag in post.get("tags", []) or []
        if str(tag) in CONTROLLED_TAGS
    }
    text = " ".join(
        str(post.get(field, ""))
        for field in ("text", "scenario", "explanation")
    )
    if CANCER_RE.search(text):
        existing.add("Cancer")
    else:
        existing.discard("Cancer")
    if FERTILITY_RE.search(text):
        existing.add("Fertility")
    else:
        existing.discard("Fertility")
    if PREGNANCY_RE.search(text):
        existing.add("Pregnancy")
    elif "Pregnancy" in existing and not FERTILITY_RE.search(text):
        existing.discard("Pregnancy")
    if MENOPAUSE_RE.search(text):
        existing.add("Menopause")
    else:
        existing.discard("Menopause")
    if EATING_RE.search(text):
        existing.add("EatingDisorders")
    else:
        existing.discard("EatingDisorders")
    if BODY_IMAGE_RE.search(text):
        existing.add("BodyImage")
    else:
        existing.discard("BodyImage")
    if SELF_HARM_RE.search(text) or str(post.get("category")) == "Self-Harm":
        existing.add("SelfHarm")
    elif "SelfHarm" in existing:
        existing.discard("SelfHarm")
    if SUICIDE_RE.search(text):
        existing.add("Suicide")
    else:
        existing.discard("Suicide")
    if ANIMAL_CRUELTY_RE.search(text):
        existing.add("AnimalCruelty")
    elif "AnimalCruelty" in existing:
        existing.discard("AnimalCruelty")
    return sorted(existing)


def normalise_post(
    source_post: dict[str, Any],
    override: dict[str, Any],
    used_authors: set[str],
) -> tuple[dict[str, Any], list[str]]:
    post = dict(source_post)
    changes: list[str] = []
    for key, value in override.items():
        if post.get(key) != value:
            post[key] = value
            changes.append(f"override:{key}")

    for field in FIELDS_TO_CLEAN:
        if field in post:
            cleaned = clean_world_text(post.get(field, ""))
            if cleaned != str(post.get(field, "")):
                changes.append(f"world:{field}")
            post[field] = cleaned

    original_author = str(post.get("author", ""))
    post["author"] = sanitise_author(post, used_authors)
    if post["author"] != original_author:
        changes.append("author:sanitised")

    post["day"] = coerce_int(post.get("day", 0))
    for field in NUMERIC_FIELDS:
        post[field] = coerce_int(post.get(field, 0))
    for field in BOOLEAN_FIELDS:
        post[field] = coerce_bool(post.get(field, False))
    for field in LIST_FIELDS:
        value = post.get(field, [])
        post[field] = list(value) if isinstance(value, (list, tuple, set)) else []

    post.setdefault("profileImage", "")
    post.setdefault("postImage", "")
    post.setdefault("scenario", "")
    post.setdefault("notes", "")
    post.setdefault("bio", "")
    post.setdefault("location", "")
    post.setdefault("platform", "")
    post.setdefault("correctEscalationReason", "")
    post.setdefault("correctSpecialistReason", "")
    post.setdefault("acceptableEscalationReasons", [])
    post.setdefault("acceptableSpecialistReasons", [])
    post.setdefault("allowNeedsReviewEscalation", False)
    post.setdefault("isStoryPost", False)

    action = str(post.get("correctAction", "")).strip()
    if action != "Escalate":
        for field, empty in (
            ("correctEscalationReason", ""),
            ("acceptableEscalationReasons", []),
            ("correctSpecialistReason", ""),
            ("acceptableSpecialistReasons", []),
            ("allowNeedsReviewEscalation", False),
        ):
            if post.get(field) != empty:
                changes.append(f"action-clear:{field}")
            post[field] = empty
    elif str(post.get("correctEscalationReason", "")) != "MisinformationPublicHarm":
        post["correctSpecialistReason"] = ""
        post["acceptableSpecialistReasons"] = []

    post["tags"] = clean_tags(post)

    # Keep all schema fields in a stable order while preserving any future extras.
    ordered = {field: post.get(field, "" if field not in LIST_FIELDS else []) for field in STANDARD_FIELDS}
    for key, value in post.items():
        if key not in ordered and not key.startswith("_"):
            ordered[key] = value
    return ordered, changes


def discover_inputs(args: argparse.Namespace, root: Path) -> list[Path]:
    if args.inputs:
        return [Path(item).resolve() for item in args.inputs]
    approved_dir = (root / args.approved_dir).resolve()
    return sorted(
        approved_dir.rglob("*.json"),
        key=lambda path: path.stat().st_mtime,
    )


def load_overrides(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    payload = load_json(path)
    return payload.get("posts", payload)


def rebalance_platforms(posts: list[dict[str, Any]]) -> list[str]:
    changes: list[str] = []
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for post in posts:
        if int(post.get("day", 0)) >= 6:
            grouped[int(post.get("day", 0))].append(post)

    for day, day_posts in grouped.items():
        day_posts.sort(key=lambda item: str(item.get("id", "")))
        for chunk_start in range(0, len(day_posts), 25):
            chunk = day_posts[chunk_start:chunk_start + 25]
            offset = (day + chunk_start // 25) % len(PLATFORMS)
            for index, post in enumerate(chunk):
                desired = PLATFORMS[(offset + index) % len(PLATFORMS)]
                if post.get("platform") != desired:
                    post["platform"] = desired
                    changes.append(f"{post.get('id')}: platform->{desired}")
    return changes



def policy_quality_warnings(post: dict[str, Any]) -> list[str]:
    post_id = str(post.get("id", ""))
    day = int(post.get("day", 0) or 0)
    action = str(post.get("correctAction", ""))
    reason = str(post.get("correctEscalationReason", ""))
    specialist = str(post.get("correctSpecialistReason", ""))
    acceptable = {str(item) for item in post.get("acceptableEscalationReasons", []) or []}
    haystack = " ".join(
        str(post.get(field, ""))
        for field in ("author", "text", "scenario", "explanation", "notes", "location", "platform")
    )
    lower = haystack.casefold()
    warnings: list[str] = []

    if FRAUD_REQUEST_RE.search(haystack) and (action == "Remove" or reason != "FraudScam"):
        if not any(phrase in lower for phrase in ("do not reply", "don't reply", "scam alert", "warning about", "asking whether")):
            warnings.append(f"{post_id}: policy heuristic: fraud/scam signals but not Escalate/FraudScam.")
    if DANGEROUS_CHALLENGE_RE.search(haystack) and (action == "Remove" or reason == "ThreatViolence"):
        if not any(phrase in lower for phrase in ("do not attempt", "do not try", "warns viewers not to", "not to attempt")):
            warnings.append(f"{post_id}: policy heuristic: dangerous challenge may need MisinformationPublicHarm/PublicSafety routing.")
    if HEALTH_HARM_RE.search(haystack) and (action == "Remove" or reason != "MisinformationPublicHarm"):
        warnings.append(f"{post_id}: policy heuristic: harmful health misinformation may need MisinformationPublicHarm.")
    if PUBLIC_HARM_MISINFO_RE.search(haystack) and action == "Escalate" and reason == "MisinformationPublicHarm" and day >= 10 and not specialist:
        warnings.append(f"{post_id}: policy heuristic: Day 10+ public-harm misinformation may need a specialist reason.")
    if reason == "ThreatViolence" and not THREAT_LANGUAGE_RE.search(haystack):
        warnings.append(f"{post_id}: policy heuristic: ThreatViolence lacks clear threat/planning/incitement language.")
    if HARASSMENT_ESCALATION_RE.search(haystack) and action in {"Approve", "Remove"}:
        warnings.append(f"{post_id}: policy heuristic: sustained harassment/brigading signals but not Escalate/HarassmentAbuse.")
    if FIRST_PERSON_CRISIS_RE.search(haystack) and action == "Remove":
        warnings.append(f"{post_id}: policy heuristic: first-person crisis signals but action is Remove.")
    if PRIVACY_SIGNAL_RE.search(haystack):
        has_privacy = reason == "PrivacySensitiveInfo" or "PrivacySensitiveInfo" in acceptable
        has_fraud_privacy = reason == "FraudScam" and "PrivacySensitiveInfo" in acceptable
        if action == "Escalate" and not (has_privacy or has_fraud_privacy):
            warnings.append(f"{post_id}: policy heuristic: privacy signals should include PrivacySensitiveInfo as primary or acceptable.")
    if REAL_WORLD_REFERENCE_RE.search(haystack):
        warnings.append(f"{post_id}: policy heuristic: possible real-world reference in runtime text or notes.")
    if str(post.get("category", "")) == "Fraud" and action == "Remove" and FRAUD_REQUEST_RE.search(haystack):
        warnings.append(f"{post_id}: policy heuristic: Fraud category with theft signals is still Remove.")
    if str(post.get("category", "")) == "Threat" and DANGEROUS_CHALLENGE_RE.search(haystack) and not THREAT_LANGUAGE_RE.search(haystack):
        warnings.append(f"{post_id}: policy heuristic: Threat category on dangerous challenge without actual threat.")
    if str(post.get("category", "")) == "Misinformation" and action == "Escalate" and reason == "MisinformationPublicHarm" and day >= 10 and not specialist:
        warnings.append(f"{post_id}: policy heuristic: Day 10+ misinformation escalation has no specialist reason.")

    return warnings

def validate(posts: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    ids: set[str] = set()
    author_counts = Counter()

    for post in posts:
        post_id = str(post.get("id", ""))
        if not post_id:
            errors.append("Post with missing id.")
            continue
        if post_id in ids:
            errors.append(f"{post_id}: duplicate id.")
        ids.add(post_id)

        if not str(post.get("category", "")).strip():
            errors.append(f"{post_id}: blank category.")
        if post.get("correctAction") not in {"Approve", "Remove", "Escalate"}:
            errors.append(f"{post_id}: invalid correctAction.")
        if not isinstance(post.get("day"), int):
            errors.append(f"{post_id}: day is not an integer.")
        for field in NUMERIC_FIELDS:
            if not isinstance(post.get(field), int):
                errors.append(f"{post_id}: {field} is not an integer.")
        for field in BOOLEAN_FIELDS:
            if not isinstance(post.get(field), bool):
                errors.append(f"{post_id}: {field} is not boolean.")

        action = post.get("correctAction")
        day = int(post.get("day", 0) or 0)
        reason = str(post.get("correctEscalationReason", ""))
        specialist = str(post.get("correctSpecialistReason", ""))
        acceptable_reasons = list(post.get("acceptableEscalationReasons", []) or [])
        acceptable_specialists = list(post.get("acceptableSpecialistReasons", []) or [])

        if not str(post.get("explanation", "")).strip():
            errors.append(f"{post_id}: blank explanation.")

        if action != "Escalate" and (
            post.get("correctEscalationReason")
            or post.get("acceptableEscalationReasons")
            or post.get("correctSpecialistReason")
            or post.get("acceptableSpecialistReasons")
            or post.get("allowNeedsReviewEscalation")
        ):
            errors.append(f"{post_id}: stale escalation fields on {action} post.")

        if action == "Escalate":
            if day >= 3 and not reason:
                errors.append(f"{post_id}: Day 3+ Escalate post has blank correctEscalationReason.")
            if reason and reason not in VALID_PARENT_REASONS:
                errors.append(f"{post_id}: invalid correctEscalationReason {reason!r}.")
            invalid_reasons = sorted(
                str(item) for item in acceptable_reasons
                if str(item) not in VALID_PARENT_REASONS
            )
            if invalid_reasons:
                errors.append(
                    f"{post_id}: invalid acceptableEscalationReasons: "
                    + ", ".join(invalid_reasons)
                    + "."
                )
            if day < 3 and reason:
                errors.append(f"{post_id}: escalation reason appears before Day 3 unlock.")
            if specialist:
                if specialist not in VALID_SPECIALIST_REASONS:
                    errors.append(f"{post_id}: invalid correctSpecialistReason {specialist!r}.")
                if day < 10:
                    warnings.append(f"{post_id}: specialist reason appears before Day 10 unlock.")
                if reason != "MisinformationPublicHarm":
                    errors.append(f"{post_id}: specialist reason requires MisinformationPublicHarm.")
            invalid_specialists = sorted(
                str(item) for item in acceptable_specialists
                if str(item) not in VALID_SPECIALIST_REASONS
            )
            if invalid_specialists:
                errors.append(
                    f"{post_id}: invalid acceptableSpecialistReasons: "
                    + ", ".join(invalid_specialists)
                    + "."
                )
            if day >= 10 and reason == "MisinformationPublicHarm" and not specialist:
                if any(pattern.search(" ".join(str(post.get(field, "")) for field in ("text", "scenario", "explanation", "notes"))) for pattern in SPEC_HINT_REASONS.values()):
                    errors.append(f"{post_id}: Day 10+ MisinformationPublicHarm post is missing correctSpecialistReason.")

        warnings.extend(policy_quality_warnings(post))

        if int(post.get("day", 0)) >= 6:
            if post.get("location") not in APPROVED_LOCATIONS:
                errors.append(
                    f"{post_id}: location {post.get('location')!r} is outside the fictional list."
                )
            if post.get("platform") not in PLATFORMS:
                errors.append(
                    f"{post_id}: platform {post.get('platform')!r} is outside the fictional list."
                )

        visible = " ".join(
            str(post.get(field, ""))
            for field in ("author", "text", "bio", "location")
        ).casefold()
        found = sorted(
            place for place in BLOCKED_REAL_PLACES
            if re.search(rf"\b{re.escape(place)}\b", visible)
        )
        if found:
            errors.append(f"{post_id}: residual real place(s): {', '.join(found)}.")

        if PLATFORM_TOKEN_RE.search(str(post.get("author", ""))):
            errors.append(f"{post_id}: platform name in author.")
        if PLATFORM_TOKEN_RE.search(str(post.get("text", ""))):
            errors.append(f"{post_id}: platform name in visible text.")

        author_counts[str(post.get("author", "")).casefold()] += 1

    for author, count in author_counts.items():
        if author and count > 1:
            warnings.append(f"Author {author!r} appears {count} times.")

    by_day = defaultdict(list)
    for post in posts:
        by_day[int(post.get("day", 0))].append(post)

    for day, items in sorted(by_day.items()):
        counts = Counter(str(item.get("correctAction", "")) for item in items)
        warnings.append(
            f"Day {day}: {len(items)} posts | "
            f"Approve={counts['Approve']} Remove={counts['Remove']} "
            f"Escalate={counts['Escalate']}"
        )
        misinfo = sum(1 for item in items if item.get("category") == "Misinformation")
        cancer = sum(
            1
            for item in items
            if CANCER_RE.search(
                " ".join(
                    str(item.get(field, ""))
                    for field in ("text", "scenario", "explanation", "tags")
                )
            )
        )
        warnings.append(
            f"Day {day}: misinformation={misinfo}, cancer-related={cancer}."
        )

        sorted_items = sorted(items, key=lambda item: str(item.get("id", "")))
        for start in range(0, len(sorted_items), 25):
            chunk = sorted_items[start:start + 25]
            platform_counts = Counter(
                str(item.get("platform", ""))
                for item in chunk
                if int(item.get("day", 0)) >= 6
            )
            for platform, count in platform_counts.items():
                if count > 3:
                    errors.append(
                        f"Day {day} chunk {start // 25 + 1}: "
                        f"{platform} appears {count} times."
                    )

    rolling_cancer = [
        item
        for item in posts
        if CANCER_RE.search(
            " ".join(
                str(item.get(field, ""))
                for field in ("text", "scenario", "explanation", "tags")
            )
        )
    ]
    if len(rolling_cancer) > max(1, (len(posts) + 74) // 75):
        warnings.append(
            f"Library contains {len(rolling_cancer)} cancer-related posts across "
            f"{len(posts)} total; production selection must enforce the rolling cap."
        )

    return errors, warnings


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    input_paths = discover_inputs(args, root)
    if not input_paths:
        print("No approved JSON files found.", file=sys.stderr)
        return 2

    override_path = (root / args.overrides).resolve()
    overrides = load_overrides(override_path)
    output_dir = (root / args.output_dir).resolve()

    # Newest source wins for duplicate IDs.
    latest_by_id: dict[str, tuple[dict[str, Any], Path, float]] = {}
    for path in input_paths:
        payload = load_json(path)
        raw_posts = payload.get("posts", []) if isinstance(payload, dict) else []
        if not isinstance(raw_posts, list):
            continue
        mtime = path.stat().st_mtime
        for post in raw_posts:
            if not isinstance(post, dict) or not post.get("id"):
                continue
            post_id = str(post["id"])
            current = latest_by_id.get(post_id)
            if current is None or mtime >= current[2]:
                latest_by_id[post_id] = (post, path, mtime)

    used_authors: set[str] = set()
    cleaned: list[dict[str, Any]] = []
    change_log: list[str] = []
    source_manifest: dict[str, str] = {}
    for post_id in sorted(latest_by_id):
        raw_post, source_path, _ = latest_by_id[post_id]
        post, changes = normalise_post(
            raw_post,
            overrides.get(post_id, {}),
            used_authors,
        )
        cleaned.append(post)
        source_manifest[post_id] = str(source_path)
        if changes:
            change_log.append(f"{post_id}: " + ", ".join(changes))

    change_log.extend(rebalance_platforms(cleaned))
    cleaned.sort(key=lambda item: (int(item.get("day", 0)), str(item.get("id", ""))))

    errors, warnings = validate(cleaned)

    approved_dir = output_dir / "approved"
    write_json(approved_dir / "all-approved-posts-v4.json", {"posts": cleaned})

    by_day = defaultdict(list)
    for post in cleaned:
        by_day[int(post.get("day", 0))].append(post)
    for day, items in sorted(by_day.items()):
        write_json(approved_dir / f"day-{day:02d}-approved-v4.json", {"posts": items})

    manifest = {
        "version": 4,
        "postCount": len(cleaned),
        "sourceFiles": [str(path) for path in input_paths],
        "sourceByPostId": source_manifest,
        "outputFiles": [
            str(approved_dir / "all-approved-posts-v4.json"),
            *[
                str(approved_dir / f"day-{day:02d}-approved-v4.json")
                for day in sorted(by_day)
            ],
        ],
        "errors": errors,
        "warnings": warnings,
    }
    write_json(output_dir / "manifest.json", manifest)

    report_lines = [
        "CONTENT LIBRARY V4 VALIDATION",
        f"Posts: {len(cleaned)}",
        f"Sources: {len(input_paths)}",
        f"Blocking errors: {len(errors)}",
        "",
        "ERRORS",
        *(errors or ["None."]),
        "",
        "SUMMARY / WARNINGS",
        *(warnings or ["None."]),
        "",
        "CHANGES",
        *(change_log or ["None."]),
        "",
        "The source approved files were not modified.",
    ]
    (output_dir / "validation-report.txt").write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print(f"Built {len(cleaned)} posts in {output_dir}")
    print(f"Blocking errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())


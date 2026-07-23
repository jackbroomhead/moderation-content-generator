from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import sys
import time
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import requests
from jsonschema import Draft202012Validator
from json_repair import repair_json

from tag_rules import assign_sensitivity_tags, sensitivity_tag_errors


REFERENCE_FILES = [
    "11 - Runtime Generation Rules.md",
]

DAY_0_TO_2_CATEGORIES = {
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
}

SPECIALIST_CATEGORIES = {
    "Synthetic Media",
    "Graphic Violence",
    "Hate",
    "Extremism",
    "Platform Manipulation",
    "Sexual Exploitation",
}

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

METADATA_FIELDS = (
    "accountAgeDays",
    "followerCount",
    "followingCount",
    "verifiedStatus",
    "postCount",
    "bio",
    "previousFlags",
    "location",
    "platform",
)

APPROVED_FICTIONAL_LOCATIONS = {
    "Westbridge",
    "Oakhaven",
    "Northbridge",
    "Greyford",
    "Bellmere",
    "Moorvale",
    "Dunmere",
    "East Westbridge",
    "Unknown",
}

APPROVED_FICTIONAL_PLATFORMS = {
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
}

BLOCKED_REAL_PLACE_TERMS = {
    "london", "manchester", "birmingham", "leeds", "liverpool", "bristol",
    "sheffield", "nottingham", "derby", "brighton", "luton", "york",
    "yorkshire", "north yorkshire", "glasgow", "edinburgh", "cardiff",
    "belfast", "oxford", "cambridge", "newcastle", "leicester", "coventry",
    "southampton", "portsmouth", "plymouth", "swansea",
    "aberdeen", "dundee", "piccadilly",
}

PLATFORM_TOKEN_PATTERN = re.compile(
    r"(?i)\b(?:"
    + "|".join(re.escape(name) for name in sorted(APPROVED_FICTIONAL_PLATFORMS))
    + r")\b"
)

CANCER_CONTENT_PATTERN = re.compile(
    r"(?i)\b(?:cancer|chemotherapy|chemo|radiotherapy|radiation treatment|oncology)\b"
)

MEDICAL_MISINFORMATION_PATTERN = re.compile(
    r"(?i)\b(?:cancer|chemotherapy|chemo|radiotherapy|fertility|menopause|"
    r"pregnan|postpartum|supplement|detox|medication|medical treatment|"
    r"hormone|clinic|doctor|patient)\b"
)

NUMERIC_HANDLE_SUFFIX_PATTERN = re.compile(r"(\d{2,})$")

PROTECTED_STORY_IDENTITIES = {
    "supervisor",
    "victoria",
    "theo",
    "fennec",
    "date counterpart",
}

PROHIBITED_BRAND_TERMS = {
    "iphone", "ipad", "macbook", "playstation", "xbox", "whatsapp",
    "facebook", "instagram", "tiktok", "twitter", "paypal", "amazon",
    "netflix", "spotify", "youtube", "reddit", "discord", "telegram",
    "snapchat", "samsung", "tesla", "uber", "deliveroo",
    "tinder", "ticketmaster",
}

PLACEHOLDER_TERMS = {
    "fictionaluser", "targetname", "targetuser", "realplayername",
    "realusername", "portalname", "sampleuser", "dummyuser",
    "example street", "example lane", "example road", "example mews",
    "test hospital", "test user", "cityhospitalportal",
}

PLACEHOLDER_HANDLE_PATTERN = re.compile(
    r"(?i)(?:@)?(?:target(?:user|name)?|realplayername|realusername|"
    r"sampleuser|dummyuser|testuser|user\d{4,})\b"
)

LIVE_URL_PATTERN = re.compile(
    r"\b(?:https?://|www\.|bit\.ly/|tinyurl\.com/|t\.co/)\S+",
    re.IGNORECASE,
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)

PHONE_PATTERN = re.compile(
    r"(?<!\w)(?:\+?\d[\d ()-]{6,}\d)(?!\w)"
)

LONG_NUMBER_PATTERN = re.compile(r"\b\d{8,19}\b")
SORT_CODE_PATTERN = re.compile(r"\b\d{2}[- ]\d{2}[- ]\d{2}\b")
HASHTAG_PATTERN = re.compile(r"(?<!\w)#[A-Za-z0-9_]+")
JSON_FRAGMENT_PATTERN = re.compile(
    r'(?i)"(?:posts|category|correctAction|difficulty|explanation|day|text)"\s*:'
)
JSON_OBJECT_FRAGMENT_PATTERN = re.compile(
    r'(?is)(?:\{\s*"posts"\s*:|\{\s*"id"\s*:|\[\s*\{\s*"id"\s*:)'
)
REPEATED_OPENING_PATTERN = re.compile(
    r"(?i)^\s*(?:finally got|finally finished|just managed|just wanted to|"
    r"honestly tired|just finished|spent the afternoon|spent all afternoon|"
    r"managed to finish|finished making)\b"
)
REPEATED_HOBBY_THEME_PATTERN = re.compile(
    r"(?i)\b(?:sourdough|pottery|ceramic|kiln|candles?|vinyl|gardening|"
    r"seedlings?|planters?|knitting|crochet|sketching|watercolou?r|"
    r"crafts?|guitar)\b"
)
REPEATED_PUBLIC_NOTICE_PATTERN = re.compile(
    r"(?i)\b(?:library|community centre|town hall|festival|maintenance|"
    r"opening hours|closing early|drop-in session|annual fair|market day)\b"
)
REPEATED_CREDENTIAL_SCAM_PATTERN = re.compile(
    r"(?i)\b(?:verify (?:your )?(?:account|identity)|account recovery|"
    r"support team|security check|password|2fa|two[- ]factor|login details?|"
    r"security code|card details?)\b"
)
PROMO_URGENT_PATTERN = re.compile(
    r"(?i)\b(?:promoking|urgent|last chance|limited (?:time|offer|stock)|"
    r"click now|act fast|deal of the day|90% off|shopnow)\b"
)
BANK_FREEZE_PATTERN = re.compile(
    r"(?i)\b(?:bellmerewatcher|market freeze|bank freeze|"
    r"savings withdrawals?|withdraw everything|check your balances?)\b"
)
DAY13_EASY_FILLER_PATTERN = re.compile(
    r"(?i)\b(?:gaming achievement|achievement unlocked|high score|puzzle app|"
    r"sourdough|pottery|ceramic|kiln|candles?|vinyl|gardening|crafts?|guitar)\b"
)

SELF_LABEL_PHRASES = {
    "this is a real threat",
    "this is dangerous misinformation",
    "this is a scam",
    "this violates policy",
    "the correct action is",
    "must be removed",
    "must be escalated",
}

DEBUNKING_PHRASES = {
    "do not try this",
    "this is dangerous misinformation",
    "the claim is false",
    "fact-check",
    "fact check",
    "has been debunked",
    "warning: a viral video claims",
}

OBVIOUS_CREDENTIAL_REQUEST_PATTERN = re.compile(
    r"(?i)\b(?:reply|send|provide|enter|share)\b.{0,80}\b(?:password|"
    r"login credentials?|seed phrase|card number|credit card|security code|"
    r"bank details?|bank account|routing number|sort code)\b"
)

SELF_HARM_SIGNAL_PATTERN = re.compile(
    r"(?i)\b(?:suicid|self[- ]?harm|hurt myself|end my life|goodbye messages?|"
    r"won't be here|not safe on my own|can't go on|starv|purging|overdose)\b"
)

MEDICAL_EMERGENCY_PATTERN = re.compile(
    r"(?i)\b(?:heart attack|chest pain|can't breathe|cannot breathe|ambulance|"
    r"cardiac|seizure|stroke|passed out|pass out)\b"
)

ANIMAL_PATTERN = re.compile(
    r"(?i)\b(?:dog|cat|animal|pet|horse|rabbit|bird)\b"
)

GRAPHIC_ANIMAL_HARM_PATTERN = re.compile(
    r"(?i)\b(?:burn alive|set (?:it|them|him|her) on fire|matches|solvent|"
    r"inside (?:a|the) cage|watch .* suffer|graphic)\b"
)

EXPLICIT_FIRST_PERSON_THREAT_PATTERN = re.compile(
    r"(?i)\b(?:i am|i'm|i will|i'll|we are|we're|we will|we'll)\b"
    r".{0,45}\b(?:burn down|set fire to|bomb|shoot|stab|kill|attack|"
    r"smash up|destroy)\b"
)

TIME_SIGNAL_PATTERN = re.compile(
    r"(?i)\b(?:today|tonight|tomorrow|monday|tuesday|wednesday|thursday|"
    r"friday|saturday|sunday|\d{1,2}(?::\d{2})?\s?(?:am|pm))\b"
)

ADDRESS_SIGNAL_PATTERN = re.compile(
    r"(?i)\b\d{1,4}\s+[A-Z][A-Za-z' -]{2,30}\s+"
    r"(?:road|street|close|drive|lane|avenue|crescent|mews|way)\b"
)

EXCLUDED_TOPIC_PHRASES = {
    "child sexual",
    "grooming a child",
    "grooming minors",
    "child exploitation",
    "child abuse",
}

DEFERRED_TOPIC_PHRASES = {
    "illegal drug sale",
    "illegal drugs sale",
    "weapon sale",
    "weapons sale",
    "regulated goods",
    "copyright infringement",
}


# Conservative policy-quality heuristics. These are not perfect policy
# adjudication; they catch common generation mistakes before review/publish.
FRAUD_SCAM_SIGNAL_PATTERN = re.compile(
    r"(?i)\b(?:password|login details?|login credentials?|2fa|two[- ]factor|"
    r"security code|card number|expiry date|bank details?|gift cards?|crypto|"
    r"deposit|off-platform payment|backup payment handle|payment handle|"
    r"verification link|verify your identity|account recovery|support team|"
    r"identity documents?|home address|phone number|daily routine)\b"
)
FRAUD_REQUEST_PATTERN = re.compile(
    r"(?i)\b(?:reply|send|provide|enter|share|message|pay|transfer|deposit|"
    r"verify|confirm)\b.{0,120}\b(?:password|login details?|login credentials?|"
    r"2fa|security code|card number|expiry date|bank details?|gift cards?|crypto|"
    r"deposit|payment handle|identity documents?|home address|phone number|"
    r"daily routine)\b"
)
DANGEROUS_CHALLENGE_PATTERN = re.compile(
    r"(?i)\b(?:challenge|dare|prove (?:you'?re|you are) brave|no safety gear|"
    r"moving train|outside of a train|jump(?:ing)? from|jump(?:ing)? off|"
    r"quarry|freezing water|run(?:ning)? into traffic|break your own bones?|"
    r"ledge|cliff|stunt)\b"
)
HEALTH_HARM_PATTERN = re.compile(
    r"(?i)\b(?:skip (?:the )?(?:vaccine|injection|doctor|hospital|treatment)|"
    r"stop prescribed treatment|stop treatment|avoid emergency care|false cure|"
    r"miracle cure|cures? all cancers?|bleach|detox (?:instead|cure|protocol)|"
    r"replace (?:prescribed|medical|hospital)|doctors? (?:are )?hiding)\b"
)
PUBLIC_HARM_MISINFO_PATTERN = re.compile(
    r"(?i)\b(?:evacuation order|gas leak|chemical spill|water supply|toxic|"
    r"bridge collapse|emergency shelter|polling station|election (?:cancelled|"
    r"canceled)|ballots?|bank freeze|savings account|withdraw everything|"
    r"emergency tax|transaction(?:s)? .*blocked|public transport .*shut)\b"
)
THREAT_LANGUAGE_PATTERN = re.compile(
    r"(?i)\b(?:i will|i'll|we will|we'll|going to|planning to|bring(?:ing)? a|"
    r"weapon|knife|gun|hammer|attack|hurt|smash|smashing|burn|set fire|kill|shoot|stab|bomb|poison baits?|cull the stray|locking .* in the shed|confrontation|settle the score|deal' with anyone|"
    r"target|outside .{0,40} at \d|tonight|tomorrow)\b"
)
HARASSMENT_ESCALATION_PATTERN = re.compile(
    r"(?i)\b(?:coordinated (?:harassment|abuse|attack|campaign|brigad(?:e|ing))|brigad(?:e|ing)|mass report|report every|repeatedly|"
    r"keeps messaging|asked (?:him|her|them|you) to stop|after i blocked|"
    r"new accounts?|stalking|following me|won't leave me alone|flood(?:ed)?"
    r" (?:my )?(?:dms|messages))\b"
)
FIRST_PERSON_CRISIS_PATTERN = re.compile(
    r"(?i)\b(?:i (?:do not|don't) think i am safe|i have taken|i took|"
    r"i(?:'|â€™)m going to hurt myself|hurt myself|make myself disappear|"
    r"end my life|goodbye messages?|won't be here|not be here in the morning|"
    r"can't go on|cannot go on|overdose)\b"
)
PRIVACY_SIGNAL_PATTERN = re.compile(
    r"(?i)\b(?:home address|phone number|daily routine|medical records?|"
    r"diagnosis|hospital results?|identity document|passport|driving licence|"
    r"private address|where (?:they|she|he) live|leaves work)\b"
)


# Gemma sometimes places these required flat fields inside a nested
# "metadata" object, despite the JSON Schema. The generator safely flattens
# recognised fields and supplies empty schema-compatible defaults where a
# non-essential field is omitted.
POST_DEFAULTS = {
    "profileImage": "",
    "postImage": "",
    "tags": [],
    "scenario": "",
    "notes": "",
    "accountAgeDays": "",
    "followerCount": "",
    "followingCount": "",
    "verifiedStatus": "",
    "postCount": "",
    "bio": "",
    "previousFlags": "",
    "location": "",
    "platform": "",
    "correctEscalationReason": "",
    "acceptableEscalationReasons": [],
    "allowNeedsReviewEscalation": False,
    "isStoryPost": False,
    "correctSpecialistReason": "",
    "acceptableSpecialistReasons": [],
}


class GenerationError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.json")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise GenerationError(f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def find_named_file(root: Path, filename: str) -> Path:
    direct = root / filename
    if direct.is_file():
        return direct

    matches = list(root.rglob(filename))
    if not matches:
        raise FileNotFoundError(f"Could not find '{filename}' under {root}")
    if len(matches) > 1:
        rendered = "\n".join(f"  {p}" for p in matches)
        raise GenerationError(
            f"Found multiple copies of '{filename}'. Keep one active copy:\n{rendered}"
        )
    return matches[0]


def load_existing_posts(root: Path) -> tuple[Path, list[dict[str, Any]]]:
    path = find_named_file(root / "input", "posts.json")
    payload = load_json(path)
    if isinstance(payload, list):
        return path, payload
    if isinstance(payload, dict) and isinstance(payload.get("posts"), list):
        return path, payload["posts"]
    raise GenerationError(
        f"{path} must be an array or an object containing a 'posts' array."
    )


def load_reference_text(root: Path) -> str:
    chunks = []
    for filename in REFERENCE_FILES:
        path = find_named_file(root / "reference", filename)
        chunks.append(
            f"\n===== {filename} =====\n"
            + path.read_text(encoding="utf-8-sig").strip()
        )
    return "\n".join(chunks)


def normalise_text(value: str) -> str:
    value = value.casefold()
    value = re.sub(r"https?://\S+", " ", value)
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def load_output_history(root: Path) -> list[dict[str, Any]]:
    posts: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for folder_name in ("candidates", "approved"):
        folder = root / "output" / folder_name
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.json")):
            try:
                payload = load_json(path)
            except GenerationError:
                continue
            items = payload.get("posts", []) if isinstance(payload, dict) else payload
            if not isinstance(items, list):
                continue
            for post in items:
                if not isinstance(post, dict):
                    continue
                post_id = str(post.get("id", ""))
                if not post_id or post_id in seen_ids:
                    continue
                seen_ids.add(post_id)
                posts.append(post)
    return posts


def reserve_ids(
    used_posts: list[dict[str, Any]], target_day: int, count: int
) -> list[str]:
    pattern = re.compile(rf"^DAY{target_day}-(\d+)$")
    numbers = []
    for post in used_posts:
        match = pattern.match(str(post.get("id", "")))
        if match:
            numbers.append(int(match.group(1)))
    start = max(numbers, default=0) + 1
    return [f"DAY{target_day}-{n:03d}" for n in range(start, start + count)]


def get_available_models(config: dict[str, Any]) -> list[str]:
    response = requests.get(
        f"{config['api_base'].rstrip('/')}/models",
        timeout=min(int(config["request_timeout_seconds"]), 30),
    )
    response.raise_for_status()
    return [
        str(item["id"])
        for item in response.json().get("data", [])
        if item.get("id")
    ]


def validate_chat_model(config: dict[str, Any]) -> None:
    try:
        models = get_available_models(config)
    except requests.RequestException as exc:
        raise GenerationError(
            "Could not reach LM Studio. Start its local server and check api_base.\n"
            f"{exc}"
        ) from exc

    if config["model"] not in models:
        visible = "\n".join(f"  - {m}" for m in models) or "  (none)"
        raise GenerationError(
            f"Configured model '{config['model']}' is unavailable.\n"
            f"Available model IDs:\n{visible}"
        )


def resolve_embedding_model(config: dict[str, Any]) -> str:
    configured = str(config.get("embedding_model", "auto")).strip()
    if configured and configured.casefold() != "auto":
        return configured

    api_base = config["api_base"].rstrip("/")
    server_root = re.sub(r"/v1$", "", api_base)
    candidates: list[str] = []

    try:
        response = requests.get(
            f"{server_root}/api/v1/models",
            timeout=min(int(config["request_timeout_seconds"]), 30),
        )
        response.raise_for_status()
        models = response.json().get("models", [])
        for model in models:
            if str(model.get("type", "")).casefold() == "embedding":
                key = model.get("key") or model.get("id")
                if key:
                    candidates.append(str(key))
    except (requests.RequestException, ValueError, TypeError):
        pass

    if not candidates:
        try:
            candidates = [
                model
                for model in get_available_models(config)
                if "embed" in model.casefold() or "nomic" in model.casefold()
            ]
        except requests.RequestException:
            candidates = []

    if not candidates:
        raise GenerationError(
            "Semantic duplicate detection is enabled, but no embedding model "
            "was found. Load Nomic Embed Text v1.5 in LM Studio or set "
            "embedding_model explicitly in config.json."
        )

    candidates.sort(key=lambda value: ("nomic" not in value.casefold(), value))
    return candidates[0]


def request_embeddings(
    config: dict[str, Any], model: str, texts: list[str]
) -> list[list[float]]:
    if not texts:
        return []
    response = requests.post(
        f"{config['api_base'].rstrip('/')}/embeddings",
        json={"model": model, "input": texts},
        timeout=int(config["request_timeout_seconds"]),
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise GenerationError(
            f"LM Studio embeddings returned HTTP {response.status_code}:\n"
            f"{response.text[:3000]}"
        ) from exc

    data = response.json().get("data", [])
    ordered = sorted(data, key=lambda item: int(item.get("index", 0)))
    vectors = [item.get("embedding") for item in ordered]
    if len(vectors) != len(texts) or any(not isinstance(v, list) for v in vectors):
        raise GenerationError("LM Studio returned an unexpected embeddings response.")
    return vectors


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def embedding_cache_key(model: str, posts: list[dict[str, Any]]) -> str:
    payload = {
        "model": model,
        "items": [
            [str(post.get("id", "")), str(post.get("text", ""))]
            for post in posts
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]


def get_history_embeddings(
    root: Path,
    config: dict[str, Any],
    model: str,
    posts: list[dict[str, Any]],
) -> list[list[float]]:
    cache_dir = root / "output" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = embedding_cache_key(model, posts)
    cache_path = cache_dir / f"history-embeddings-{key}.json"
    if cache_path.exists():
        payload = load_json(cache_path)
        vectors = payload.get("vectors", []) if isinstance(payload, dict) else []
        if len(vectors) == len(posts):
            return vectors

    texts = [str(post.get("text", "")) for post in posts]
    batch_size = int(config.get("embedding_batch_size", 32))
    vectors: list[list[float]] = []
    for offset in range(0, len(texts), batch_size):
        vectors.extend(
            request_embeddings(config, model, texts[offset : offset + batch_size])
        )
    write_json(
        cache_path,
        {
            "model": model,
            "postIds": [str(post.get("id", "")) for post in posts],
            "vectors": vectors,
        },
    )
    return vectors


def load_blueprint(
    root: Path, config: dict[str, Any]
) -> tuple[Path, dict[str, Any], list[dict[str, Any]]]:
    filename = str(config.get("blueprint_file", "")).strip()
    if not filename:
        raise GenerationError("config.json must define blueprint_file.")
    path = find_named_file(root / "reference", filename)
    blueprint = load_json(path)
    slots = blueprint.get("slots", []) if isinstance(blueprint, dict) else []
    if not isinstance(slots, list) or not slots:
        raise GenerationError(f"Blueprint {path} has no slots array.")

    target_day = int(config["target_day"])
    if int(blueprint.get("day", target_day)) != target_day:
        raise GenerationError(
            f"Blueprint day {blueprint.get('day')} does not match target_day {target_day}."
        )
    requested_count = int(config["count"])
    slot_start_index = int(config.get("slot_start_index", 0) or 0)
    if slot_start_index < 0:
        raise GenerationError("slot_start_index cannot be negative.")
    if requested_count < 1 or slot_start_index + requested_count > len(slots):
        raise GenerationError(
            f"Blueprint contains {len(slots)} slots but config requested "
            f"count={requested_count} from slot_start_index={slot_start_index}. "
            "The requested window must fit inside the blueprint."
        )
    slots = slots[slot_start_index : slot_start_index + requested_count]

    if (
        requested_count == 25
        and slot_start_index == 0
        and isinstance(blueprint.get("batchBalance"), dict)
    ):
        expected_balance = blueprint["batchBalance"]
        actual_balance = {
            action: sum(1 for slot in slots if slot.get("correctAction") == action)
            for action in ("Approve", "Remove", "Escalate")
        }
        for action in ("Approve", "Remove", "Escalate"):
            expected = int(expected_balance.get(action, actual_balance[action]))
            if actual_balance[action] != expected:
                raise GenerationError(
                    f"Blueprint balance error for {action}: "
                    f"expected {expected}, found {actual_balance[action]}."
                )

    required = {"category", "correctAction", "difficulty", "scenarioBrief"}
    for index, slot in enumerate(slots, start=1):
        missing = sorted(required - set(slot))
        if missing:
            raise GenerationError(
                f"Blueprint slot {index} is missing: {', '.join(missing)}"
            )
    return path, blueprint, slots


def build_single_post_schema(
    batch_schema: dict[str, Any],
) -> dict[str, Any]:
    """Build a compact schema for model generation.

    The model generates only content-bearing fields. The script then fills
    non-content metadata defaults and validates the expanded post against the
    full authoritative game schema.
    """
    full_post_schema = copy.deepcopy(
        batch_schema["properties"]["posts"]["items"]
    )

    generated_fields = [
        "id",
        "author",
        "text",
        "category",
        "correctAction",
        "difficulty",
        "explanation",
        "day",
        "correctEscalationReason",
        "acceptableEscalationReasons",
        "allowNeedsReviewEscalation",
        "isStoryPost",
        "accountAgeDays",
        "followerCount",
        "followingCount",
        "verifiedStatus",
        "postCount",
        "bio",
        "previousFlags",
        "location",
        "platform",
        "correctSpecialistReason",
        "acceptableSpecialistReasons",
    ]

    compact_properties = {
        key: full_post_schema["properties"][key]
        for key in generated_fields
    }

    compact_post_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": compact_properties,
        "required": generated_fields,
    }

    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "posts": {
                "type": "array",
                "minItems": 1,
                "maxItems": 1,
                "items": compact_post_schema,
            }
        },
        "required": ["posts"],
    }


def build_system_prompt(reference_text: str) -> str:
    return f"""You generate original filler social-media posts for a content-moderation game.

The policy below is authoritative. Return only JSON matching the supplied schema.

Rules:
- Filler content only; never create story events or recurring story characters.
- Never generate child-safety material.
- Follow the target-day mechanics exactly.
- Never invent actions, categories, fields, or unavailable reason codes.
- Day 0 is tutorial-only and lives in Unity Resources fallback; generated
  runtime filler should begin at Day 1 unless a blueprint explicitly says otherwise.
- Days 1-2 expose only Approve, Remove and generic Escalate. Escalation-reason
  fields must remain blank before Day 3 because the player cannot select them.
- From Day 3, every Escalate post must use one approved parent reason:
  ThreatViolence, SelfHarmCrisis, HarassmentAbuse, FraudScam,
  PrivacySensitiveInfo or MisinformationPublicHarm.
- From Day 6, output the exact coherent account metadata supplied by the
  blueprint. Do not invent different counts, status, history or location.
- From Day 10, MisinformationPublicHarm escalation posts must use the approved
  specialist reason supplied by the blueprint when the central misinformation
  issue is health, civic/election, public safety, financial/economic or
  synthetic/manipulated media.
- Needs Review is never a primary JSON escalation reason.
- Use natural, plausible names, handles and organisations. Do not use
  placeholder words such as FictionalUser, TargetName, PortalName, Example
  Street or Test Hospital.
- Routine filler must use only the approved fictional world locations:
  Westbridge, Oakhaven, Northbridge, Greyford, Bellmere, Moorvale and Dunmere.
  Never use a real city, county, region, street, venue or location-based handle.
- Account platform metadata must use only: PhotoBoard, CommonThread, TownSquare,
  EchoBoard, QuickPost, CommunityFeed, MarketBoard, StoryGrid, PublicSquare or
  ClipLoop. A platform name must never be used as a username or account handle.
- Do not repeatedly mention platform names in visible text. Say "the app" or
  "the platform" unless the name is genuinely necessary.
- Never use a real private address, identifiable private person,
  public-figure allegation, phone number, usable financial detail, medical
  record, or deliberately real organisation.
- Do not mention major real-world brands, social platforms or exact branded
  product models. Use generic terms such as smartphone, games console,
  messaging app, payment account, online retailer or parcel service.
- Never output a live-looking URL. Use [link removed].
- Political, anti-government and anti-AI opinions are allowed unless another
  concrete policy violation is present.
- Write visible post text like a genuine social-media user, not like a policy
  example. The post must never announce its own moderation category or outcome.
- Use hashtags naturally: many posts should have none, some one or two, and
  occasional promotional or trend-driven posts may use several.
- Never use hashtags merely to label the moderation category.
- Avoid repetitive username formulas such as every handle ending in 99, 92 or
  another two-digit suffix. Numeric suffixes are allowed occasionally,
  but ordinary word-based handles are preferred and the same suffix must not recur.
- Production pools must remain recognisable as ordinary social media:
  approximately 14 Approve, 6 Remove and 5 Escalate posts per 25.
- Keep misinformation to roughly 2-4 posts per 25. Health or medical
  misinformation is optional and capped at one per batch. Cancer-related
  content is rare: at most one item across a rolling 75-post window.
- Default to contemporary UK English and use Â£ when money is needed unless the
  blueprint explicitly requires another setting.
- Use [link removed] only when a link is necessary to understand the scenario.
  Approved posts should not contain it.
- Keep each post focused on one main moderation issue rather than stacking
  several unrelated violations to make the answer obvious.
- A misinformation-removal post must itself promote or assert the harmful
  falsehood. A post warning about, quoting to debunk, or correcting a false
  claim is not a misinformation violation.
- Simple spam is nuisance promotion, bot-like advertising, engagement bait,
  repetitive ads, suspicious low-risk offers or low-value junk: normally Remove.
- FraudScam is required once reasons are unlocked when a post asks for or steers
  users toward passwords, login details, 2FA/security codes, card numbers,
  expiry dates, bank details, gift cards, crypto, deposits, off-platform
  payments, backup payment handles, fake charity payment links, fake
  support/security/account verification, identity documents, or home
  address/phone/routine data as part of a fake verification flow.
- Dangerous challenge posts should not usually be simple Remove once reasons
  are unlocked. Challenges involving bridges, moving trains, quarry/freezing
  water, traffic, broken bones or no-safety-gear stunts should map to
  Escalate / MisinformationPublicHarm with allowNeedsReviewEscalation=true.
  From Day 10, use specialist PublicSafetyEmergency when applicable.
- Do not classify dangerous challenges as ThreatViolence unless there is an
  actual threat against a person or group.
- Health misinformation escalates to MisinformationPublicHarm when it
  discourages vaccines, prescribed treatment or emergency care, promotes false
  cures, or encourages dangerous substances. From Day 10, use HealthMedical.
- Civic, public-safety and financial misinformation escalates when it may cause
  voter suppression, panic, unsafe movement or financial harm. Use Day 10+
  specialist reasons CivicElection, PublicSafetyEmergency, FinancialEconomic
  or SyntheticManipulatedMedia as appropriate.
- ThreatViolence requires actual threat, incitement, praise, planning or intent
  of violence. Do not use it for civic frustration, public-safety rumours,
  dangerous challenges without a target, demolition/eviction safety claims or
  non-violent infrastructure risk.
- Self-Harm / Crisis escalation requires first-person crisis, imminent risk,
  method/means, goodbye language, active suicidal ideation, overdose/ingestion
  statements, or ambiguous but concerning first-person distress. General
  self-harm promotion without personal crisis is usually Remove.
- HarassmentAbuse escalation is for coordinated harassment, brigading, mass
  reporting, repeated unwanted contact, stalking-style behaviour or multi-account
  evasion after blocks. One-off targeted insults are usually Remove.
- PrivacySensitiveInfo escalation is for disclosed or solicited home addresses,
  phone numbers, exact routines, medical information, identity document
  fragments, private schedules or private addresses of someone else. Fake
  support soliciting private data may be FraudScam primary with Privacy as
  acceptable.
- Approve debunks, corrections, scam/stunt warnings and users asking whether
  something is suspicious when they are not spreading it as fact or soliciting
  harm/payment.
- Animal-cruelty cases must be text-only and non-graphic, without method detail.
  Under the current parent menu they may use ThreatViolence only when no better
  active parent reason exists; append a future AnimalCruelty/RealWorldHarm note
  when appropriate.
- Include enough evidence for a fair and defensible decision.
- Explanations must be non-empty, one or two concise sentences stating why the
  action and reason apply. Edge-case explanations should name common traps, such
  as why a public-safety claim is not ThreatViolence.
- Every generated post is filler, so isStoryPost must be false.
- Output exactly one post in the posts array.

AUTHORITATIVE REFERENCE:
{reference_text}
"""



def accepted_texts_for_avoidance(
    accepted_posts: list[dict[str, Any]], limit: int = 8
) -> str:
    """Render recent accepted post text for prompt-level repetition avoidance."""
    if not accepted_posts:
        return "- None yet."
    recent = accepted_posts[-limit:]
    return "\n".join(
        f"- {str(post.get('text', ''))[:220]}" for post in recent
    )


def resolve_slot_variant(
    slot: dict[str, Any],
    post_id: str,
    comparison_posts: list[dict[str, Any]] | None = None,
    accepted_posts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Choose deterministic scenario/metadata variants for this post ID.

    V4 supports scenarioVariants that may override specialist reasons, tags,
    policy hints and metadata. Cancer variants are skipped when cancer has
    appeared in the rolling 75-post history or already in the current batch.
    """
    resolved = copy.deepcopy(slot)
    comparison_posts = comparison_posts or []
    accepted_posts = accepted_posts or []

    variants = resolved.get("scenarioVariants", [])
    if isinstance(variants, list) and variants:
        match = re.search(r"(\d+)$", post_id)
        numeric_id = int(match.group(1)) if match else int(
            hashlib.sha256(post_id.encode("utf-8")).hexdigest(), 16
        )
        offset = int(resolved.get("variantOffset", 0))
        selected = copy.deepcopy(variants[(numeric_id + offset) % len(variants)])
        for key, value in selected.items():
            resolved[key] = value

    options = resolved.get("scenarioOptions", [])
    if isinstance(options, list) and options:
        recent_posts = (comparison_posts + accepted_posts)[-75:]
        recent_has_cancer = any(
            CANCER_CONTENT_PATTERN.search(
                " ".join(
                    str(post.get(field, ""))
                    for field in ("text", "scenario", "tags")
                )
            )
            for post in recent_posts
        )
        available = list(options)
        if recent_has_cancer:
            non_cancer = [
                option for option in available
                if not CANCER_CONTENT_PATTERN.search(str(option))
            ]
            if non_cancer:
                available = non_cancer

        digest = hashlib.sha256(post_id.encode("utf-8")).hexdigest()
        selected_option = available[int(digest, 16) % len(available)]
        resolved["scenarioBrief"] = str(selected_option)

    return resolved


def build_user_prompt(
    target_day: int,
    post_id: str,
    slot: dict[str, Any],
    accepted_posts: list[dict[str, Any]],
    previous_errors: list[str],
) -> str:
    retry = ""
    if previous_errors:
        retry = (
            "\nFix these previous validation issues:\n- "
            + "\n- ".join(previous_errors[:12])
            + "\n"
        )

    expected_reason = str(slot.get("correctEscalationReason", ""))
    expected_acceptable = list(slot.get("acceptableEscalationReasons", []))
    expected_needs_review = bool(
        slot.get("allowNeedsReviewEscalation", False)
    )
    expected_specialist = str(slot.get("correctSpecialistReason", ""))
    expected_acceptable_specialist = list(
        slot.get("acceptableSpecialistReasons", [])
    )
    metadata = {
        field: slot.get("metadata", {}).get(field, POST_DEFAULTS[field])
        for field in METADATA_FIELDS
    }
    policy_hint = str(slot.get("policyHint", "")).strip()
    hint_line = f"- Policy emphasis: {policy_hint}\n" if policy_hint else ""
    avoided = accepted_texts_for_avoidance(accepted_posts)

    return f"""Create exactly one fictional filler post for a moderation game.

Mandatory blueprint:
- id = {post_id}
- day = {target_day}
- category = {slot['category']}
- correctAction = {slot['correctAction']}
- difficulty = {slot['difficulty']}
- scenario = {slot['scenarioBrief']}
- correctEscalationReason = {expected_reason!r}
- acceptableEscalationReasons = {expected_acceptable!r}
- allowNeedsReviewEscalation = {str(expected_needs_review).lower()}
- correctSpecialistReason = {expected_specialist!r}
- acceptableSpecialistReasons = {expected_acceptable_specialist!r}
- account metadata = {metadata!r}
- isStoryPost = false
{hint_line}
Return only these fields:
- id
- author
- text
- category
- correctAction
- difficulty
- explanation
- day
- correctEscalationReason
- acceptableEscalationReasons
- allowNeedsReviewEscalation
- correctSpecialistReason
- acceptableSpecialistReasons
- accountAgeDays
- followerCount
- followingCount
- verifiedStatus
- postCount
- bio
- previousFlags
- location
- platform
- isStoryPost

Rules:
- author must be a unique, natural fictional username
- never put a platform name or real place name in the username
- do not use generic handles such as PublicSquareUser89, QuickPostUser or User1234
- vary handle structure; prefer natural word-based handles; numeric suffixes are
  allowed occasionally, but avoid relying on them too often
- use only the approved fictional locations: Westbridge, Oakhaven, Northbridge,
  Greyford, Bellmere, Moorvale and Dunmere
- do not mention the platform name in visible text unless essential; normally
  say "the app" or "the platform"
- visible text must sound like a real user, not a moderation training example
- do not let the post label itself as a threat, scam, misinformation or policy violation
- use hashtags naturally; occasional promotional or trend-driven posts may use several
- explanation must be one or two concise sentences explaining the policy result
- use contemporary UK English and Â£ by default
- use plausible names and places rather than visible placeholders
- do not output phone numbers, email addresses, account numbers, card details,
  routing numbers, sort codes or usable payment handles
- do not use major brands, named social platforms or branded product models
- use [link removed] instead of any URL, and only when a link is needed
- focus on one primary moderation issue rather than stacking unrelated violations
- return strict JSON only in exactly this outer shape: {{"posts":[{{...}}]}}
- do not return a single post object at the root
- no Markdown fences, commentary, or reasoning
- no nested metadata object
- no story characters, real allegations, excluded topics, or deferred topics
- the case must be self-contained
- metadata values must exactly match the blueprint and must matter to the case
  only when the scenario says they matter
- an explanation must not invent evidence absent from the visible post or
  supplied metadata
- the visible post itself must contain the evidence supporting the decision;
  do not merely say that another unseen post contained an address, threat,
  scam, rumour or private detail
- Threat/Escalate needs an actual threat, planned harm, target or credible
  report of planned harm; a normal event announcement is not a threat
- Privacy/Escalate must expose the sensitive detail itself, such as a fictional
  address, routine, workplace access point, live location or medical fact
- Fraud/Escalate needs a suspicious payment, impersonation, authentication,
  fundraiser or social-engineering signal
- Harassment/Escalate must show repetition, stalking, coordination, brigading
  or continued contact after blocks
- Self-Harm/Remove must explicitly promote or glorify self-harm or
  eating-disorder behaviour; vague language about discipline is insufficient
- do not use moderation labels as hashtags merely to make the answer obvious
- do not use a scenario or phrasing similar to an earlier generated post
{retry}
Posts already accepted in this batch; avoid their scenarios and wording:
{avoided}

Return the JSON immediately.
"""

def request_raw(
    config: dict[str, Any],
    schema: dict[str, Any],
    system_prompt: str,
    user_prompt: str,
) -> dict[str, Any]:
    """Call LM Studio's native REST chat endpoint.

    The native endpoint exposes an explicit reasoning='off' setting. We keep
    the authoritative schema validation in Python after generation.
    """
    prompt_suffix = str(config.get("writer_prompt_suffix", "")).strip()
    if prompt_suffix:
        user_prompt = user_prompt.rstrip() + "\n\n" + prompt_suffix

    payload = {
        "model": config["model"],
        "system_prompt": system_prompt,
        "input": user_prompt,
        "temperature": float(config.get("temperature", 0.7)),
        "top_p": float(config.get("top_p", 0.8)),
        "top_k": int(config.get("top_k", 20)),
        "max_output_tokens": int(config.get("max_tokens_per_post", 1200)),
        "reasoning": str(config.get("reasoning", "off")),
        "stream": False,
        "store": False,
    }

    response = requests.post(
        f"{config['native_api_base'].rstrip('/')}/chat",
        json=payload,
        timeout=int(config["request_timeout_seconds"]),
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise GenerationError(
            f"LM Studio native chat returned HTTP {response.status_code}:\n"
            f"{response.text[:4000]}"
        ) from exc
    return response.json()


def parse_content(
    raw: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    repairs: list[str] = []

    # LM Studio native REST API response.
    if isinstance(raw.get("output"), list):
        message_items = [
            item for item in raw["output"]
            if isinstance(item, dict) and item.get("type") == "message"
        ]
        content = (
            message_items[-1].get("content", "")
            if message_items
            else ""
        )
        if not str(content).strip():
            stats = raw.get("stats", {})
            raise GenerationError(
                "LM Studio native chat returned no final message. "
                f"stats={stats!r}. The raw response has been saved in output/reports."
            )
        text = str(content).strip()

    # Backward-compatible OpenAI response parsing.
    else:
        try:
            choice = raw["choices"][0]
            message = choice["message"]
        except (KeyError, IndexError, TypeError) as exc:
            raise GenerationError(
                "Unexpected LM Studio response shape:\n"
                + json.dumps(raw, ensure_ascii=False, indent=2)[:5000]
            ) from exc

        content = message.get("content")
        if isinstance(content, dict):
            parsed = content
            if "posts" not in parsed and any(
                key in parsed for key in ("id", "author", "text")
            ):
                parsed = {"posts": [parsed]}
                repairs.append(
                    "Wrapped a root-level post object in the required posts array."
                )
            return parsed, repairs

        text = "" if content is None else str(content).strip()
        if not text:
            finish_reason = choice.get("finish_reason")
            usage = raw.get("usage", {})
            reasoning = (
                message.get("reasoning")
                or message.get("reasoning_content")
                or ""
            )
            reasoning_note = (
                f"\nReasoning characters returned: {len(str(reasoning))}"
                if reasoning
                else ""
            )
            raise GenerationError(
                "LM Studio returned an empty final message. "
                f"finish_reason={finish_reason!r}; usage={usage!r}."
                f"{reasoning_note} "
                "The raw response has been saved in output/reports."
            )

    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as original_error:
        try:
            parsed = repair_json(text, return_objects=True)
        except Exception as repair_error:
            raise GenerationError(
                "Model output was not valid JSON and automatic syntax repair "
                f"failed.\nOriginal error: {original_error}\n"
                f"Repair error: {repair_error}\n{text[:4000]}"
            ) from repair_error

        if not isinstance(parsed, dict):
            raise GenerationError(
                "Automatic JSON syntax repair did not produce a JSON object.\n"
                f"Original error: {original_error}\n{text[:4000]}"
            )

        repairs.append(
            "Repaired malformed JSON syntax before schema validation "
            f"(original parser error: {original_error})."
        )

    # Qwen sometimes returns the single post directly rather than the requested
    # {"posts": [...]} wrapper. This is a harmless structural repair.
    if isinstance(parsed, dict) and "posts" not in parsed and any(
        key in parsed for key in ("id", "author", "text")
    ):
        parsed = {"posts": [parsed]}
        repairs.append(
            "Wrapped a root-level post object in the required posts array."
        )

    return parsed, repairs


def normalise_model_payload(
    payload: dict[str, Any],
) -> tuple[dict[str, Any], list[str], list[str], list[str]]:
    repairs: list[str] = []
    fallbacks: list[str] = []
    defaults: list[str] = []
    posts = payload.get("posts")
    if not isinstance(posts, list):
        return payload, repairs, fallbacks, defaults

    for index, post in enumerate(posts):
        if not isinstance(post, dict):
            continue

        metadata = post.pop("metadata", None)
        if isinstance(metadata, dict):
            moved = 0
            for key, value in metadata.items():
                if key in POST_DEFAULTS and key not in post:
                    post[key] = value
                    moved += 1
            repairs.append(
                f"posts[{index}]: flattened nested metadata ({moved} field(s) moved)."
            )

        if isinstance(post.get("tags"), str):
            tag = post["tags"].strip()
            post["tags"] = [tag] if tag else []
            repairs.append(f"posts[{index}].tags: converted string to array.")

        if isinstance(post.get("previousFlags"), list):
            values = post["previousFlags"]
            post["previousFlags"] = "" if not values else len(values)
            repairs.append(f"posts[{index}].previousFlags: converted array.")

        if not str(post.get("author", "")).strip():
            safe_id = re.sub(
                r"[^a-zA-Z0-9]+", "_", str(post.get("id", index))
            ).strip("_").lower()
            post["author"] = f"user_{safe_id}"
            fallbacks.append(
                f"posts[{index}].author: supplied deterministic fictional username."
            )

        if not str(post.get("explanation", "")).strip():
            action = str(post.get("correctAction", ""))
            category = str(post.get("category", "content"))
            reason = str(post.get("correctEscalationReason", ""))
            if action == "Approve":
                explanation = (
                    f"This is ordinary {category.lower()} content with no credible "
                    "policy or safety concern."
                )
            elif action == "Remove":
                explanation = (
                    f"This is a clear {category.lower()} policy violation that can "
                    "be removed without specialist review."
                )
            else:
                explanation = (
                    f"This presents a credible {category.lower()} concern requiring "
                    f"specialist review under {reason}."
                )
            post["explanation"] = explanation
            fallbacks.append(
                f"posts[{index}].explanation: supplied deterministic policy explanation."
            )

        for key, default in POST_DEFAULTS.items():
            if key not in post:
                post[key] = copy.deepcopy(default)
                defaults.append(f"posts[{index}].{key}")

    return payload, repairs, fallbacks, defaults


def schema_errors(payload: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    return [
        f"{'.'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
        for e in errors
    ]


def batch_quality_errors(posts: list[dict[str, Any]], target_day: int) -> list[str]:
    errors: list[str] = []
    opening_counts: dict[str, int] = {}
    promo_count = 0
    bank_freeze_count = 0

    for post in posts:
        post_id = str(post.get("id", "<unknown>"))
        author = str(post.get("author", ""))
        text = str(post.get("text", ""))
        combined = f"{author} {text}"

        if JSON_FRAGMENT_PATTERN.search(text) or JSON_OBJECT_FRAGMENT_PATTERN.search(text):
            errors.append(
                f"{post_id}: visible text contains JSON-like field/object fragments."
            )

        match = REPEATED_OPENING_PATTERN.search(text)
        if match:
            opening = match.group(0).strip().casefold()
            opening_counts[opening] = opening_counts.get(opening, 0) + 1

        if PROMO_URGENT_PATTERN.search(combined):
            promo_count += 1

        if BANK_FREEZE_PATTERN.search(combined):
            bank_freeze_count += 1

    repeated_openings = sorted(
        opening for opening, count in opening_counts.items() if count > 1
    )
    if repeated_openings:
        errors.append(
            "Repeated low-diversity opening phrase(s) in batch: "
            + ", ".join(repeated_openings)
            + "."
        )

    if promo_count > 1:
        errors.append(
            "Batch repeats PromoKing/urgent-deal spam more than once; vary remove cases."
        )

    if bank_freeze_count > 1:
        errors.append(
            "Batch repeats Bellmere bank/market freeze misinformation more than once."
        )

    if target_day >= 13:
        easy_filler_count = 0
        obvious_spam_count = 0
        hard_case_count = 0
        for post in posts:
            action = str(post.get("correctAction", ""))
            category = str(post.get("category", ""))
            difficulty = str(post.get("difficulty", ""))
            reason = str(post.get("correctEscalationReason", ""))
            needs_review = bool(post.get("allowNeedsReviewEscalation", False))
            text = str(post.get("text", ""))
            combined = f"{post.get('author', '')} {text}"
            explanation = str(post.get("explanation", ""))
            haystack = f"{combined} {explanation}".casefold()

            if action == "Approve" and DAY13_EASY_FILLER_PATTERN.search(text):
                easy_filler_count += 1
            if action == "Remove" and category == "Spam" and (
                difficulty == "Easy" or PROMO_URGENT_PATTERN.search(combined)
            ):
                obvious_spam_count += 1
            if action == "Escalate" and needs_review:
                hard_case_count += 1
            if action == "Escalate" and reason in {
                "HarassmentAbuse",
                "FraudScam",
                "PrivacySensitiveInfo",
                "MisinformationPublicHarm",
            }:
                hard_case_count += 1
            if (
                difficulty == "Hard"
                and action in {"Remove", "Escalate"}
                and category in {
                    "Harassment",
                    "Fraud",
                    "Privacy",
                    "Misinformation",
                    "Threat",
                    "Self-Harm",
                }
            ):
                hard_case_count += 1
            if any(
                phrase in haystack
                for phrase in (
                    "metadata",
                    "previous flag",
                    "repeat",
                    "coordinated",
                    "needs review",
                    "ambiguous",
                    "overlap",
                )
            ):
                hard_case_count += 1

        if easy_filler_count or obvious_spam_count:
            errors.append(
                "Day 13 batch contains simple approve filler or obvious promo spam; "
                "use hard overlaps, metadata relevance, Needs Review or specialist ambiguity."
            )
        if hard_case_count == 0:
            errors.append(
                "Day 13 batch lacks hard overlap, metadata-relevant, Needs Review "
                "or specialist ambiguity signals."
            )

    return errors


def sentence_count(text: str) -> int:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return len([part for part in parts if part.strip()])


def editorial_quality_errors(
    post: dict[str, Any],
    expected_action: str,
    expected_category: str,
) -> list[str]:
    errors: list[str] = []
    author = str(post.get("author", "")).strip()
    text = str(post.get("text", "")).strip()
    explanation = str(post.get("explanation", "")).strip()
    combined = f"{author} {text}"

    if PLACEHOLDER_HANDLE_PATTERN.search(combined):
        errors.append(
            "Uses an immersion-breaking placeholder handle or identity."
        )

    if EMAIL_PATTERN.search(text):
        errors.append("Contains an email address; use non-usable fictional context.")

    if PHONE_PATTERN.search(text):
        errors.append("Contains a phone-number-like sequence; remove it.")

    if LONG_NUMBER_PATTERN.search(text) or SORT_CODE_PATTERN.search(text):
        errors.append(
            "Contains a usable-looking financial or account number; remove it."
        )

    if JSON_FRAGMENT_PATTERN.search(text) or JSON_OBJECT_FRAGMENT_PATTERN.search(text):
        errors.append(
            "Post text contains JSON-like field/object fragments such as \"posts\" "
            "or \"category\":; "
            "visible post text must not include raw JSON."
        )

    if REPEATED_OPENING_PATTERN.search(text):
        errors.append(
            "Avoid repeated low-diversity openings such as 'Finally finished...' "
            "or hobby-completion templates."
        )

    if REPEATED_HOBBY_THEME_PATTERN.search(text):
        errors.append(
            "Avoid overused hobby/craft/baking/gardening themes in nightly output."
        )

    if REPEATED_PUBLIC_NOTICE_PATTERN.search(text):
        errors.append(
            "Avoid repeated public notice, library, maintenance or festival templates."
        )

    if REPEATED_CREDENTIAL_SCAM_PATTERN.search(text) and expected_category == "Fraud":
        errors.append(
            "Avoid repeated obvious credential-scam wording; use a fresher fraud or "
            "social-engineering pattern."
        )

    day = int(post.get("day", 0) or 0)
    difficulty = str(post.get("difficulty", "")).strip()
    if day >= 13:
        if expected_action == "Approve" and DAY13_EASY_FILLER_PATTERN.search(text):
            errors.append(
                "Day 13 nightly posts must not use simple gaming achievements, "
                "pure hobby filler or Easy approve filler as main cases."
            )
        if expected_action == "Remove" and expected_category == "Spam" and (
            difficulty == "Easy" or PROMO_URGENT_PATTERN.search(combined)
        ):
            errors.append(
                "Day 13 nightly posts must not use obvious urgent promo spam as "
                "a main case; use harder remove or overlap cases."
            )
    if (
        day >= 10
        and expected_action == "Escalate"
        and str(post.get("correctEscalationReason", "")) == "MisinformationPublicHarm"
        and BANK_FREEZE_PATTERN.search(combined)
    ):
        errors.append(
            "Day 10+ specialist misinformation should vary beyond bank freeze, "
            "market freeze or savings-withdrawal panic templates."
        )

    if expected_action == "Approve" and "[link removed]" in text.casefold():
        errors.append("Approved posts should not contain [link removed].")

    lowered = text.casefold()
    self_labels = sorted(
        phrase for phrase in SELF_LABEL_PHRASES if phrase in lowered
    )
    if self_labels:
        errors.append(
            "Post text labels its own policy outcome: "
            + ", ".join(self_labels)
            + "."
        )

    if len(explanation) > 420 or sentence_count(explanation) > 2:
        errors.append(
            "Explanation must be one or two concise sentences (maximum 420 characters)."
        )

    if (
        expected_category == "Misinformation"
        and expected_action == "Remove"
        and any(phrase in lowered for phrase in DEBUNKING_PHRASES)
    ):
        errors.append(
            "This appears to warn about or debunk misinformation rather than promote it."
        )

    if (
        expected_category == "Fraud"
        and expected_action == "Escalate"
        and OBVIOUS_CREDENTIAL_REQUEST_PATTERN.search(text)
    ):
        errors.append(
            "This is obvious credential theft and should normally be Remove, not Escalate."
        )

    if (
        expected_category == "Self-Harm"
        and expected_action == "Escalate"
        and MEDICAL_EMERGENCY_PATTERN.search(text)
        and not SELF_HARM_SIGNAL_PATTERN.search(text)
    ):
        errors.append(
            "This is a general medical emergency, not a Self-Harm / Crisis case."
        )

    if (
        ANIMAL_PATTERN.search(text)
        and GRAPHIC_ANIMAL_HARM_PATTERN.search(text)
    ):
        errors.append(
            "Animal-cruelty content is too graphic or method-specific; keep it non-graphic."
        )

    explanation_lower = explanation.casefold()

    if expected_action == "Approve" and any(
        phrase in explanation_lower
        for phrase in (
            "promotes harmful",
            "constitutes a violation",
            "violates policy",
            "must be removed",
            "requires specialist investigation",
            "requires specialist review",
        )
    ):
        errors.append(
            "Approve action conflicts with an explanation describing removal or escalation."
        )

    if expected_action == "Remove" and any(
        phrase in explanation_lower
        for phrase in (
            "permitted",
            "allowed content",
            "does not violate",
            "no policy violation",
            "requires specialist investigation",
        )
    ):
        errors.append(
            "Remove action conflicts with an explanation describing approval or escalation."
        )

    if expected_action == "Escalate" and any(
        phrase in explanation_lower
        for phrase in (
            "harmless",
            "permitted",
            "allowed content",
            "does not violate",
            "must be removed immediately",
        )
    ):
        errors.append(
            "Escalate action conflicts with the explanation."
        )

    if (
        expected_action == "Approve"
        and EXPLICIT_FIRST_PERSON_THREAT_PATTERN.search(text)
    ):
        errors.append(
            "Contains an explicit first-person threat and cannot be treated as ordinary satire."
        )

    if "specific time" in explanation_lower and not TIME_SIGNAL_PATTERN.search(text):
        errors.append(
            "Explanation claims a specific time, but no time evidence appears in the post."
        )

    if (
        "residential address" in explanation_lower
        and not ADDRESS_SIGNAL_PATTERN.search(text)
    ):
        errors.append(
            "Explanation claims a residential address, but no address appears in the post."
        )

    return errors



def apply_blueprint_contract(
    payload: dict[str, Any],
    slot: dict[str, Any],
    expected_id: str,
    expected_day: int,
) -> list[str]:
    """Force structural fields from the authoritative blueprint.

    The language model is responsible for author, visible text and explanation.
    IDs, day, actions, reasons and metadata are deterministic game data and
    should never consume retries merely because the model emitted "13" instead
    of 13 or returned a stale escalation value.
    """
    repairs: list[str] = []
    posts = payload.get("posts")
    if not isinstance(posts, list) or len(posts) != 1:
        return repairs
    post = posts[0]
    if not isinstance(post, dict):
        return repairs

    expected_metadata = {
        field: slot.get("metadata", {}).get(field, POST_DEFAULTS[field])
        for field in METADATA_FIELDS
    }
    expected = {
        "id": expected_id,
        "day": int(expected_day),
        "category": str(slot["category"]),
        "correctAction": str(slot["correctAction"]),
        "difficulty": str(slot["difficulty"]),
        "correctEscalationReason": str(
            slot.get("correctEscalationReason", "")
        ),
        "acceptableEscalationReasons": list(
            slot.get("acceptableEscalationReasons", [])
        ),
        "allowNeedsReviewEscalation": bool(
            slot.get("allowNeedsReviewEscalation", False)
        ),
        "correctSpecialistReason": str(
            slot.get("correctSpecialistReason", "")
        ),
        "acceptableSpecialistReasons": list(
            slot.get("acceptableSpecialistReasons", [])
        ),
        "isStoryPost": False,
        **expected_metadata,
    }

    for field, value in expected.items():
        if post.get(field) != value:
            post[field] = copy.deepcopy(value)
            repairs.append(
                f"Applied authoritative blueprint value for {field}."
            )

    return repairs


def validate_post(
    payload: dict[str, Any],
    comparison_posts: list[dict[str, Any]],
    accepted_posts: list[dict[str, Any]],
    expected_id: str,
    expected_day: int,
    slot: dict[str, Any],
    similarity_threshold: float,
) -> list[str]:
    errors: list[str] = []
    posts = payload.get("posts")
    if not isinstance(posts, list) or len(posts) != 1:
        return ["The response must contain exactly one post."]

    post = posts[0]
    expected_action = str(slot["correctAction"])
    expected_category = str(slot["category"])
    expected_difficulty = str(slot["difficulty"])
    expected_reason = str(slot.get("correctEscalationReason", ""))
    expected_acceptable = list(slot.get("acceptableEscalationReasons", []))
    expected_needs_review = bool(
        slot.get("allowNeedsReviewEscalation", False)
    )
    expected_specialist = str(slot.get("correctSpecialistReason", ""))
    expected_acceptable_specialist = list(
        slot.get("acceptableSpecialistReasons", [])
    )
    expected_metadata = {
        field: slot.get("metadata", {}).get(field, POST_DEFAULTS[field])
        for field in METADATA_FIELDS
    }

    expectations = {
        "id": expected_id,
        "day": expected_day,
        "correctAction": expected_action,
        "category": expected_category,
        "difficulty": expected_difficulty,
        "correctEscalationReason": expected_reason,
        "acceptableEscalationReasons": expected_acceptable,
        "allowNeedsReviewEscalation": expected_needs_review,
        "correctSpecialistReason": expected_specialist,
        "acceptableSpecialistReasons": expected_acceptable_specialist,
        "isStoryPost": False,
        **expected_metadata,
    }
    for field, expected in expectations.items():
        if post.get(field) != expected:
            errors.append(f"{field} must be {expected!r}.")

    if expected_day <= 2:
        if expected_reason != "":
            errors.append(
                "Blueprint error: Days 0-2 must leave "
                "correctEscalationReason blank."
            )
        if expected_acceptable:
            errors.append(
                "Blueprint error: Days 0-2 must leave "
                "acceptableEscalationReasons empty."
            )
        if expected_needs_review:
            errors.append(
                "Blueprint error: Needs Review is unavailable before Day 3."
            )
    elif expected_action == "Escalate":
        if expected_reason not in VALID_PARENT_REASONS:
            errors.append(
                "Blueprint escalation reason is not an approved parent reason."
            )
    elif expected_reason:
        errors.append(
            "Blueprint error: non-escalated posts must have a blank reason."
        )

    if expected_specialist:
        if expected_day < 10:
            errors.append(
                "Blueprint error: specialist reasons are unavailable before Day 10."
            )
        if expected_action != "Escalate":
            errors.append(
                "Blueprint error: specialist reasons require Escalate."
            )
        if expected_reason != "MisinformationPublicHarm":
            errors.append(
                "Blueprint error: specialist reasons currently apply only to MisinformationPublicHarm."
            )
        if expected_specialist not in VALID_SPECIALIST_REASONS:
            errors.append(
                "Blueprint specialist reason is not approved."
            )
    elif expected_acceptable_specialist:
        errors.append(
            "Blueprint error: acceptable specialist reasons require a primary specialist reason."
        )

    if expected_day >= 6 and not slot.get("metadata"):
        errors.append(
            "Blueprint error: Day 6+ slots must define coherent account metadata."
        )

    if expected_day <= 2 and post.get("category") not in DAY_0_TO_2_CATEGORIES:
        errors.append(
            f"category {post.get('category')!r} is unavailable on Day "
            f"{expected_day}."
        )
    if post.get("category") in SPECIALIST_CATEGORIES:
        errors.append(
            f"specialist category {post.get('category')!r} is too early."
        )

    haystack = " ".join(
        str(post.get(field, ""))
        for field in (
            "author", "text", "bio", "scenario", "notes", "location", "platform"
        )
    ).casefold()

    visible_world_text = " ".join(
        str(post.get(field, ""))
        for field in ("author", "text", "bio", "location")
    ).casefold()
    found_real_places = sorted(
        place for place in BLOCKED_REAL_PLACE_TERMS
        if re.search(rf"\b{re.escape(place)}\b", visible_world_text)
    )
    if found_real_places:
        errors.append(
            "Uses real-world place name(s) instead of the fictional setting: "
            + ", ".join(found_real_places)
            + "."
        )

    location_value = str(post.get("location", "")).strip()
    allowed_location = (
        not location_value
        or location_value in APPROVED_FICTIONAL_LOCATIONS
        or (
            location_value.startswith("Near ")
            and location_value[5:] in APPROVED_FICTIONAL_LOCATIONS
        )
    )
    if expected_day >= 6 and not allowed_location:
        errors.append(
            f"location {location_value!r} is not in the approved fictional location list."
        )

    platform_value = str(post.get("platform", "")).strip()
    if expected_day >= 6 and platform_value not in APPROVED_FICTIONAL_PLATFORMS:
        errors.append(
            f"platform {platform_value!r} is not an approved fictional platform."
        )

    author_value = str(post.get("author", "")).strip()
    if PLATFORM_TOKEN_PATTERN.search(author_value):
        errors.append("Author username must not contain a platform name.")
    if PLATFORM_TOKEN_PATTERN.search(str(post.get("text", ""))):
        errors.append(
            "Visible post text should refer to 'the app' or 'the platform' rather "
            "than repeatedly naming a fictional platform."
        )

    batch_posts = accepted_posts + [post]
    if sum(
        1 for item in batch_posts
        if str(item.get("category", "")) == "Misinformation"
    ) > 4:
        errors.append("Batch exceeds the maximum of four misinformation posts.")

    medical_misinfo_count = sum(
        1
        for item in batch_posts
        if str(item.get("category", "")) == "Misinformation"
        and MEDICAL_MISINFORMATION_PATTERN.search(
            " ".join(
                str(item.get(field, ""))
                for field in ("text", "scenario", "explanation")
            )
        )
    )
    if medical_misinfo_count > 1:
        errors.append(
            "Batch exceeds the maximum of one health/medical misinformation post."
        )

    current_has_cancer = bool(
        CANCER_CONTENT_PATTERN.search(
            " ".join(
                str(post.get(field, ""))
                for field in ("text", "scenario", "explanation", "tags")
            )
        )
    )
    recent_has_cancer = any(
        CANCER_CONTENT_PATTERN.search(
            " ".join(
                str(item.get(field, ""))
                for field in ("text", "scenario", "explanation", "tags")
            )
        )
        for item in (comparison_posts + accepted_posts)[-75:]
    )
    if current_has_cancer and recent_has_cancer:
        errors.append(
            "Cancer-related content already exists in the rolling 75-post window."
        )

    if expected_day >= 6:
        platform_count = sum(
            1 for item in batch_posts
            if str(item.get("platform", "")).strip() == platform_value
        )
        if platform_count > 3:
            errors.append(
                f"Platform {platform_value!r} appears more than three times in this batch."
            )

    # Numeric username suffixes are intentionally not hard validation errors.
    # They can look repetitive, but blocking on them caused valid production
    # batches to fail after otherwise good posts had already been accepted.
    # Variety is now steered through the prompt and manual review rather than
    # stopping the whole generator.

    for identity in sorted(PROTECTED_STORY_IDENTITIES):
        if re.search(rf"\b{re.escape(identity)}\b", haystack):
            errors.append(f"Uses protected story identity {identity!r}.")
    for phrase in sorted(EXCLUDED_TOPIC_PHRASES):
        if phrase in haystack:
            errors.append(f"Uses excluded topic phrase {phrase!r}.")
    for phrase in sorted(DEFERRED_TOPIC_PHRASES):
        if phrase in haystack:
            errors.append(f"Uses not-yet-active topic phrase {phrase!r}.")

    placeholder_matches = re.findall(
        r"\[(?!link removed\])[^\]]*(?:town|city|name|location|user|place)[^\]]*\]",
        haystack,
        flags=re.IGNORECASE,
    )
    if placeholder_matches:
        errors.append(
            "Uses a visible placeholder instead of a natural fictional detail."
        )

    found_brands = sorted(
        term for term in PROHIBITED_BRAND_TERMS
        if re.search(rf"\b{re.escape(term)}\b", haystack)
    )
    if found_brands:
        errors.append(
            "Uses prohibited real-world brand/platform term(s): "
            + ", ".join(found_brands)
            + "."
        )

    found_placeholders = sorted(
        term for term in PLACEHOLDER_TERMS if term in haystack
    )
    if found_placeholders:
        errors.append(
            "Uses immersion-breaking placeholder term(s): "
            + ", ".join(found_placeholders)
            + "."
        )

    if LIVE_URL_PATTERN.search(haystack):
        errors.append("Uses a live-looking URL; use [link removed].")

    errors.extend(
        editorial_quality_errors(post, expected_action, expected_category)
    )
    errors.extend(sensitivity_tag_errors(post, slot))
    errors.extend(policy_quality_errors(post))

    explanation_lower = str(post.get("explanation", "")).casefold()
    verified = post.get("verifiedStatus", "")
    account_age = post.get("accountAgeDays", "")
    previous_flags = post.get("previousFlags", "")

    if "verified account" in explanation_lower and str(verified).casefold() not in {
        "true", "verified", "yes"
    }:
        errors.append(
            "Explanation relies on verified status, but metadata is not verified."
        )

    if any(
        phrase in explanation_lower
        for phrase in ("new account", "newly created", "recently created")
    ):
        try:
            if int(account_age) > 30:
                errors.append(
                    "Explanation calls the account new, but accountAgeDays exceeds 30."
                )
        except (TypeError, ValueError):
            errors.append(
                "Explanation calls the account new, but accountAgeDays is missing."
            )

    if "previous flags" in explanation_lower:
        try:
            if int(previous_flags) <= 0:
                errors.append(
                    "Explanation relies on previous flags, but metadata has none."
                )
        except (TypeError, ValueError):
            errors.append(
                "Explanation relies on previous flags, but metadata is missing."
            )

    author = str(post.get("author", "")).casefold().strip()
    if any(
        author and author == str(other.get("author", "")).casefold().strip()
        for other in accepted_posts
    ):
        errors.append("Author username duplicates another post in this batch.")

    if expected_day >= 6:
        metadata_tuple = tuple(
            str(post.get(field, "")).casefold().strip()
            for field in (
                "location", "platform", "bio", "verifiedStatus", "previousFlags"
            )
        )
        for other in accepted_posts:
            other_tuple = tuple(
                str(other.get(field, "")).casefold().strip()
                for field in (
                    "location", "platform", "bio", "verifiedStatus", "previousFlags"
                )
            )
            if metadata_tuple == other_tuple:
                errors.append(
                    "Account metadata tuple duplicates another accepted post in this batch."
                )
                break

    generated_text = normalise_text(str(post.get("text", "")))
    for other in comparison_posts + accepted_posts:
        other_text = normalise_text(str(other.get("text", "")))
        if not other_text:
            continue
        similarity = SequenceMatcher(None, generated_text, other_text).ratio()
        if similarity >= similarity_threshold:
            errors.append(
                f"Text is too similar to {other.get('id', '<unknown>')} "
                f"(lexical similarity {similarity:.2f})."
            )
            break

    return errors



def policy_quality_errors(post: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    day = int(post.get("day", 0) or 0)
    action = str(post.get("correctAction", ""))
    reason = str(post.get("correctEscalationReason", ""))
    specialist = str(post.get("correctSpecialistReason", ""))
    acceptable = {str(item) for item in post.get("acceptableEscalationReasons", []) or []}
    haystack = " ".join(
        str(post.get(field, ""))
        for field in ("author", "text", "scenario", "explanation", "notes", "location", "platform")
    )

    if not str(post.get("explanation", "")).strip():
        errors.append("Approved runtime posts must have a non-empty explanation.")
    if action == "Escalate" and day >= 3 and not reason:
        errors.append("Day 3+ Escalate posts must have correctEscalationReason.")
    if reason and reason not in VALID_PARENT_REASONS:
        errors.append(f"Invalid correctEscalationReason {reason!r}.")
    invalid_acceptable = sorted(item for item in acceptable if item not in VALID_PARENT_REASONS)
    if invalid_acceptable:
        errors.append("Invalid acceptableEscalationReasons: " + ", ".join(invalid_acceptable) + ".")
    if specialist:
        if specialist not in VALID_SPECIALIST_REASONS:
            errors.append(f"Invalid correctSpecialistReason {specialist!r}.")
        if day < 10:
            errors.append("Specialist reasons are unavailable before Day 10.")
    if action == "Escalate" and day >= 10 and reason == "MisinformationPublicHarm" and not specialist:
        errors.append("Day 10+ MisinformationPublicHarm escalations must include correctSpecialistReason.")

    if day >= 3 and FRAUD_REQUEST_PATTERN.search(haystack) and (action != "Escalate" or reason != "FraudScam"):
        errors.append("Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.")
    if day >= 3 and DANGEROUS_CHALLENGE_PATTERN.search(haystack) and (action == "Remove" or reason == "ThreatViolence"):
        errors.append("Likely dangerous challenge should be Escalate / MisinformationPublicHarm, not Remove or ThreatViolence without a target.")
    if day >= 3 and HEALTH_HARM_PATTERN.search(haystack) and (action == "Remove" or reason != "MisinformationPublicHarm"):
        errors.append("Likely harmful medical misinformation should be Escalate / MisinformationPublicHarm once reasons are unlocked.")
    if reason == "ThreatViolence" and not THREAT_LANGUAGE_PATTERN.search(haystack):
        errors.append("ThreatViolence needs actual threat, incitement, planning or intent language.")
    if day >= 3 and HARASSMENT_ESCALATION_PATTERN.search(haystack) and action in {"Approve", "Remove"}:
        errors.append("Likely sustained harassment/brigading should be Escalate / HarassmentAbuse once reasons are unlocked.")
    if day >= 3 and FIRST_PERSON_CRISIS_PATTERN.search(haystack) and action == "Remove":
        errors.append("Likely first-person crisis should be Escalate / SelfHarmCrisis once reasons are unlocked.")
    if day >= 3 and PRIVACY_SIGNAL_PATTERN.search(haystack):
        has_privacy = reason == "PrivacySensitiveInfo" or "PrivacySensitiveInfo" in acceptable
        has_fraud_privacy = reason == "FraudScam" and "PrivacySensitiveInfo" in acceptable
        if not (has_privacy or has_fraud_privacy):
            errors.append("Likely private/sensitive information should include PrivacySensitiveInfo as primary or acceptable reason.")

    return errors

def run_semantic_duplicate_check(
    root: Path,
    config: dict[str, Any],
    model: str,
    comparison_posts: list[dict[str, Any]],
    generated_posts: list[dict[str, Any]],
) -> tuple[list[str], list[str], set[str]]:
    history_vectors = get_history_embeddings(
        root, config, model, comparison_posts
    )
    generated_vectors = request_embeddings(
        config, model, [str(post.get("text", "")) for post in generated_posts]
    )

    existing_threshold = float(config.get("semantic_existing_threshold", 0.90))
    batch_threshold = float(config.get("semantic_batch_threshold", 0.84))
    failures: list[str] = []
    score_lines: list[str] = []
    rejected_ids: set[str] = set()

    for index, (post, vector) in enumerate(zip(generated_posts, generated_vectors)):
        post_id = str(post.get("id", index))
        best_score = 0.0
        best_id = "none"
        for other, other_vector in zip(comparison_posts, history_vectors):
            score = cosine_similarity(vector, other_vector)
            if score > best_score:
                best_score = score
                best_id = str(other.get("id", "<unknown>"))
        score_lines.append(
            f"{post_id}: nearest history={best_id} score={best_score:.3f}"
        )
        if best_score >= existing_threshold:
            failures.append(
                f"{post_id} is semantically too similar to history post {best_id} "
                f"({best_score:.3f} >= {existing_threshold:.3f})."
            )
            rejected_ids.add(post_id)

        for earlier_index in range(index):
            earlier = generated_posts[earlier_index]
            earlier_id = str(earlier.get("id", earlier_index))
            score = cosine_similarity(vector, generated_vectors[earlier_index])
            if score >= batch_threshold:
                failures.append(
                    f"{post_id} is semantically too similar to batch post {earlier_id} "
                    f"({score:.3f} >= {batch_threshold:.3f})."
                )
                rejected_ids.add(post_id)

    return failures, score_lines, rejected_ids


def main() -> int:
    # Local preflight: exercise prompt construction before contacting LM Studio.
    _preflight_slot = {
        "category": "Normal",
        "correctAction": "Approve",
        "difficulty": "Easy",
        "scenarioBrief": "Harmless preflight example.",
    }
    _preflight_prompt = build_user_prompt(
        1, "DAY1-000", _preflight_slot, [], []
    )
    if "DAY1-000" not in _preflight_prompt or "isStoryPost = false" not in _preflight_prompt:
        raise GenerationError("Generator prompt preflight failed before LM Studio was contacted.")

    started = time.monotonic()
    args = parse_args()
    config_path = Path(args.config).resolve()
    root = config_path.parent
    config = load_json(config_path)

    target_day = int(config["target_day"])
    count = int(config["count"])
    max_attempts = int(config["max_attempts_per_post"])

    schema_path = find_named_file(root / "reference", "06 - post-schema.json")
    batch_schema = load_json(schema_path)
    single_schema = build_single_post_schema(batch_schema)
    reference_text = load_reference_text(root)
    posts_path, existing_posts = load_existing_posts(root)
    history_posts = (
        load_output_history(root)
        if bool(config.get("include_candidate_history", True))
        else []
    )
    comparison_posts = existing_posts + history_posts
    blueprint_path, blueprint, slots = load_blueprint(root, config)
    ids = reserve_ids(comparison_posts, target_day, count)

    validate_chat_model(config)
    embedding_model = resolve_embedding_model(config)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    candidate_dir = root / "output" / "candidates"
    rejected_dir = root / "output" / "rejected"
    report_dir = root / "output" / "reports"
    checkpoint_dir = root / "output" / "checkpoints"
    for folder in (candidate_dir, rejected_dir, report_dir, checkpoint_dir):
        folder.mkdir(parents=True, exist_ok=True)

    blueprint_name = str(blueprint.get("name", blueprint_path.stem))
    safe_blueprint = re.sub(r"[^a-zA-Z0-9_-]+", "-", blueprint_name).strip("-")
    checkpoint_path = checkpoint_dir / f"day{target_day}-{safe_blueprint}-current.json"

    accepted_by_id: dict[str, dict[str, Any]] = {}
    repair_log: list[str] = []
    fallback_log: list[str] = []
    default_log: list[str] = []

    if checkpoint_path.exists():
        checkpoint = load_json(checkpoint_path)
        if (
            checkpoint.get("blueprintName") == blueprint_name
            and checkpoint.get("reservedIds") == ids
        ):
            accepted_by_id = {
                str(post.get("id")): post
                for post in checkpoint.get("posts", [])
                if isinstance(post, dict) and post.get("id")
            }
            repair_log = list(checkpoint.get("repairs", []))
            fallback_log = list(checkpoint.get("fallbacks", []))
            default_log = list(checkpoint.get("defaults", []))
            print(f"Resuming checkpoint with {len(accepted_by_id)}/{count} posts.")
        else:
            stale = checkpoint_path.with_name(
                checkpoint_path.stem + f"-stale-{timestamp}.json"
            )
            checkpoint_path.replace(stale)
            print(f"Archived incompatible checkpoint to {stale}")

    system_prompt = build_system_prompt(reference_text)

    print(f"Workspace: {root}")
    print(f"Runtime reference characters: {len(reference_text):,}")
    print(f"Existing dataset: {posts_path}")
    print(f"Generated history posts: {len(history_posts)}")
    print(f"Schema: {schema_path}")
    print(f"Blueprint: {blueprint_path}")
    print(f"Chat model: {config['model']}")
    print("Chat API: LM Studio native /api/v1/chat")
    print(f"Reasoning mode: {config.get('reasoning', 'off')}")
    suffix = str(config.get("writer_prompt_suffix", "")).strip()
    print(f"Writer prompt suffix: {suffix or '(none)'}")
    print(f"Embedding model: {embedding_model}")
    print(f"Generating {count} diverse Day {target_day} posts...")

    for index, (post_id, raw_slot) in enumerate(zip(ids, slots), start=1):
        if post_id in accepted_by_id:
            print(f"\nPost {index}/{count}: {post_id} already checkpointed; skipping.")
            continue

        accepted_posts = [
            accepted_by_id[item_id]
            for item_id in ids
            if item_id in accepted_by_id
        ]
        slot = resolve_slot_variant(
            raw_slot,
            post_id,
            comparison_posts=comparison_posts,
            accepted_posts=accepted_posts,
        )
        print(
            f"\nPost {index}/{count}: {post_id} | {slot['correctAction']} | "
            f"{slot['category']} | {slot['difficulty']}"
        )
        previous_errors: list[str] = []
        success = False

        for attempt in range(1, max_attempts + 1):
            user_prompt = build_user_prompt(
                target_day, post_id, slot, accepted_posts, previous_errors
            )
            try:
                raw = request_raw(config, single_schema, system_prompt, user_prompt)
            except (requests.RequestException, GenerationError) as exc:
                previous_errors = [str(exc)]
                print(f"  Attempt {attempt}: request failed: {exc}")
                continue

            raw_path = report_dir / (
                f"day{target_day}-{post_id}-{timestamp}-attempt{attempt}-raw.json"
            )
            write_json(raw_path, raw)

            try:
                payload, syntax_repairs = parse_content(raw)
            except GenerationError as exc:
                previous_errors = [str(exc)]
                print(f"  Attempt {attempt}: {exc}")
                continue

            payload, structure_repairs, fallbacks, defaults = normalise_model_payload(payload)
            structure_repairs.extend(
                apply_blueprint_contract(
                    payload,
                    slot,
                    post_id,
                    target_day,
                )
            )
            if (
                isinstance(payload.get("posts"), list)
                and len(payload["posts"]) == 1
                and isinstance(payload["posts"][0], dict)
            ):
                assign_sensitivity_tags(payload["posts"][0], slot)
            repairs = syntax_repairs + structure_repairs
            print(
                f"  Attempt {attempt}: defaults={len(defaults)}, "
                f"repairs={len(repairs)}, fallbacks={len(fallbacks)}."
            )

            errors = schema_errors(payload, batch_schema)
            errors.extend(
                validate_post(
                    payload,
                    comparison_posts,
                    accepted_posts,
                    post_id,
                    target_day,
                    slot,
                    float(config.get("duplicate_similarity_threshold", 0.86)),
                )
            )

            if errors:
                previous_errors = errors
                write_json(
                    rejected_dir
                    / f"day{target_day}-{post_id}-{timestamp}-attempt{attempt}.json",
                    payload,
                )
                lines = ["VALIDATION ERRORS", *errors]
                if repairs:
                    lines.extend(["", "REPAIRS", *repairs])
                if fallbacks:
                    lines.extend(["", "FALLBACKS", *fallbacks])
                if defaults:
                    lines.extend(["", "DEFAULTS ADDED", *defaults])
                (report_dir / f"day{target_day}-{post_id}-{timestamp}-attempt{attempt}-errors.txt").write_text(
                    "\n".join(lines) + "\n", encoding="utf-8"
                )
                print(f"  Attempt {attempt}: rejected with {len(errors)} issue(s).")
                for error in errors[:6]:
                    print(f"    - {error}")
                continue

            post = payload["posts"][0]
            accepted_by_id[post_id] = post
            repair_log.extend([f"{post_id}: {item}" for item in repairs])
            fallback_log.extend([f"{post_id}: {item}" for item in fallbacks])
            default_log.extend([f"{post_id}: {item}" for item in defaults])
            write_json(
                checkpoint_path,
                {
                    "blueprintName": blueprint_name,
                    "reservedIds": ids,
                    "posts": [
                        accepted_by_id[item_id]
                        for item_id in ids
                        if item_id in accepted_by_id
                    ],
                    "repairs": repair_log,
                    "fallbacks": fallback_log,
                    "defaults": default_log,
                },
            )
            print(f"  Attempt {attempt}: accepted and checkpointed.")
            success = True
            break

        if not success:
            failure = report_dir / f"day{target_day}-{post_id}-{timestamp}-failed.txt"
            failure.write_text(
                "FAILED TO GENERATE THIS POST\n\n" + "\n".join(previous_errors) + "\n",
                encoding="utf-8",
            )
            print(f"\nStopped. Accepted posts remain checkpointed. See:\n  {failure}")
            return 1

    generated_posts = [accepted_by_id[post_id] for post_id in ids]
    final_payload = {"posts": generated_posts}
    final_schema_errors = schema_errors(final_payload, batch_schema)
    if final_schema_errors:
        failure = report_dir / f"day{target_day}-pilot-{timestamp}-final-schema-errors.txt"
        failure.write_text("\n".join(final_schema_errors) + "\n", encoding="utf-8")
        print(f"\nCombined batch failed final schema validation:\n  {failure}")
        return 1

    final_quality_errors = batch_quality_errors(generated_posts, target_day)
    if final_quality_errors:
        failure = report_dir / f"day{target_day}-pilot-{timestamp}-batch-quality-failed.txt"
        failure.write_text(
            "BATCH QUALITY CHECK FAILED\n\n"
            + "\n".join(final_quality_errors)
            + "\n",
            encoding="utf-8",
        )
        print(f"\nCombined batch failed quality validation:\n  {failure}")
        return 1

    print("\nRunning semantic duplicate detection...")
    semantic_failures, semantic_scores, rejected_ids = run_semantic_duplicate_check(
        root, config, embedding_model, comparison_posts, generated_posts
    )
    if semantic_failures:
        rejected_posts = [
            post for post in generated_posts
            if str(post.get("id", "")) in rejected_ids
        ]
        write_json(
            rejected_dir / f"day{target_day}-pilot-{timestamp}-semantic-rejected.json",
            {"posts": rejected_posts},
        )
        for rejected_id in rejected_ids:
            accepted_by_id.pop(rejected_id, None)
        repair_log = [
            line for line in repair_log
            if not any(line.startswith(f"{item_id}:") for item_id in rejected_ids)
        ]
        fallback_log = [
            line for line in fallback_log
            if not any(line.startswith(f"{item_id}:") for item_id in rejected_ids)
        ]
        default_log = [
            line for line in default_log
            if not any(line.startswith(f"{item_id}:") for item_id in rejected_ids)
        ]
        write_json(
            checkpoint_path,
            {
                "blueprintName": blueprint_name,
                "reservedIds": ids,
                "posts": [
                    accepted_by_id[item_id]
                    for item_id in ids
                    if item_id in accepted_by_id
                ],
                "repairs": repair_log,
                "fallbacks": fallback_log,
                "defaults": default_log,
            },
        )
        failure = report_dir / f"day{target_day}-pilot-{timestamp}-semantic-failed.txt"
        failure.write_text(
            "SEMANTIC DUPLICATE CHECK FAILED\n\n"
            + "\n".join(semantic_failures)
            + "\n\nNEAREST-HISTORY SCORES\n"
            + "\n".join(semantic_scores)
            + "\n\nRejected posts were removed from the checkpoint. Run the generator again to regenerate only those slots.\n",
            encoding="utf-8",
        )
        print(f"Semantic check rejected {len(rejected_ids)} post(s). See:\n  {failure}")
        print("Run the generator again; completed slots will be reused.")
        return 1

    candidate_path = candidate_dir / f"day{target_day}-pilot-{timestamp}.json"
    report_path = report_dir / f"day{target_day}-pilot-{timestamp}-validation.txt"
    write_json(candidate_path, final_payload)

    elapsed = time.monotonic() - started
    blueprint_lines = [
        f"{post_id}: {slot['correctAction']} | {slot['category']} | {slot['difficulty']}"
        for post_id, slot in zip(ids, slots)
    ]
    report_path.write_text(
        "\n".join(
            [
                "VALIDATION PASSED",
                f"Generated: {datetime.now().isoformat(timespec='seconds')}",
                f"Elapsed seconds: {elapsed:.1f}",
                f"Chat model: {config['model']}",
                f"Embedding model: {embedding_model}",
                f"Target day: {target_day}",
                f"Post count: {count}",
                f"Candidate: {candidate_path}",
                "",
                "BLUEPRINT",
                *blueprint_lines,
                "",
                "SEMANTIC DUPLICATE CHECK",
                *semantic_scores,
                "",
                "ACTUAL REPAIRS",
                *(repair_log or ["None."]),
                "",
                "CONTENT FALLBACKS",
                *(fallback_log or ["None."]),
                "",
                f"SCHEMA DEFAULTS ADDED: {len(default_log)}",
                "The master input/posts.json was not modified.",
                "Manual policy and writing review is still required.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    completed_checkpoint = checkpoint_path.with_name(
        checkpoint_path.stem.replace("-current", "") + f"-completed-{timestamp}.json"
    )
    checkpoint_path.replace(completed_checkpoint)

    print("\nValidation passed.")
    print(f"Candidate:\n  {candidate_path}")
    print(f"Report:\n  {report_path}")
    print(f"Elapsed: {elapsed / 60:.1f} minutes")
    print("The master input/posts.json was not modified.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, GenerationError) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)


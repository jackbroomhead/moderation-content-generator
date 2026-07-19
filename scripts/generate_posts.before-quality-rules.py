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
}

PLACEHOLDER_TERMS = {
    "fictionaluser", "targetname", "portalname", "example street",
    "example lane", "example road", "example mews", "test hospital",
    "test user", "cityhospitalportal",
}

LIVE_URL_PATTERN = re.compile(
    r"\b(?:https?://|www\.|bit\.ly/|tinyurl\.com/|t\.co/)\S+",
    re.IGNORECASE,
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
    if len(slots) != int(config["count"]):
        raise GenerationError(
            f"Blueprint contains {len(slots)} slots but config count is {config['count']}."
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
- Days 0-2 may contain Escalate posts, but both escalation-reason fields must
  remain blank because the player has only the generic Escalate action.
- From Day 3, Escalate posts must use the approved parent reason supplied by
  the blueprint.
- Needs Review is never a primary JSON escalation reason.
- Use natural, plausible names, handles, organisations and places. Do not use
  placeholder words such as FictionalUser, TargetName, PortalName, Example
  Street or Test Hospital.
- Real cities and broad public locations may be used. Never use a real private
  address, identifiable private person, public-figure allegation, phone number,
  usable financial detail, medical record, or deliberately real organisation.
- Do not mention major real-world brands, social platforms or exact branded
  product models. Use generic terms such as smartphone, games console,
  messaging app, payment account, online retailer or parcel service.
- Never output a live-looking URL. Use [link removed].
- Political, anti-government and anti-AI opinions are allowed unless another
  concrete policy violation is present.
- Include enough evidence for a fair and defensible decision.
- Explanations must state the policy reason rather than merely repeat the answer.
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
- isStoryPost

Rules:
- author must be a unique, natural fictional username
- explanation must state why the required action follows policy
- use plausible names and places rather than visible placeholders
- do not use major brands, named social platforms or branded product models
- use [link removed] instead of any URL
- return strict JSON only in exactly this outer shape: {{"posts":[{{...}}]}}
- do not return a single post object at the root
- no Markdown fences, commentary, or reasoning
- no nested metadata object
- no story characters, real allegations, excluded topics, or deferred topics
- the case must be self-contained
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

    expectations = {
        "id": expected_id,
        "day": expected_day,
        "correctAction": expected_action,
        "category": expected_category,
        "difficulty": expected_difficulty,
        "correctEscalationReason": expected_reason,
        "acceptableEscalationReasons": expected_acceptable,
        "allowNeedsReviewEscalation": expected_needs_review,
        "isStoryPost": False,
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

    for identity in sorted(PROTECTED_STORY_IDENTITIES):
        if re.search(rf"\b{re.escape(identity)}\b", haystack):
            errors.append(f"Uses protected story identity {identity!r}.")
    for phrase in sorted(EXCLUDED_TOPIC_PHRASES):
        if phrase in haystack:
            errors.append(f"Uses excluded topic phrase {phrase!r}.")
    for phrase in sorted(DEFERRED_TOPIC_PHRASES):
        if phrase in haystack:
            errors.append(f"Uses not-yet-active topic phrase {phrase!r}.")

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

    author = str(post.get("author", "")).casefold().strip()
    if any(
        author and author == str(other.get("author", "")).casefold().strip()
        for other in accepted_posts
    ):
        errors.append("Author username duplicates another post in this batch.")

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

    for index, (post_id, slot) in enumerate(zip(ids, slots), start=1):
        if post_id in accepted_by_id:
            print(f"\nPost {index}/{count}: {post_id} already checkpointed; skipping.")
            continue

        accepted_posts = [
            accepted_by_id[item_id]
            for item_id in ids
            if item_id in accepted_by_id
        ]
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

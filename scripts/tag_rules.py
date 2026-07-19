from __future__ import annotations

import re
from typing import Any, Iterable


# Accessibility tags describe sensitive subjects visible to the player.
# They are deliberately broader than moderation categories.
CONTROLLED_SENSITIVITY_TAGS = (
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
)

# Legacy tags are normalised rather than retained as separate player filters.
TAG_ALIASES: dict[str, str | None] = {
    "Chemotherapy": "Cancer",
    "MedicalMisinformation": None,
}

TAG_PATTERNS: dict[str, re.Pattern[str]] = {
    "Cancer": re.compile(
        r"(?i)\b(?:cancer|chemo(?:therapy)?|radiotherapy|oncology|"
        r"tumou?r|carcinoma|leukaemia|leukemia)\b"
    ),
    "Fertility": re.compile(
        r"(?i)\b(?:fertility|infertility|infertile|conceiv(?:e|ing)|"
        r"trying for a baby|ivf|in vitro fertilisation)\b"
    ),
    "Pregnancy": re.compile(
        r"(?i)\b(?:pregnan(?:t|cy)|postpartum|postnatal|antenatal)\b"
    ),
    "Miscarriage": re.compile(
        r"(?i)\b(?:miscarriage|pregnancy loss|stillbirth|stillborn)\b"
    ),
    "Menopause": re.compile(
        r"(?i)\b(?:menopause|menopausal|perimenopause|perimenopausal)\b"
    ),
    "EatingDisorders": re.compile(
        r"(?i)\b(?:eating disorder|anorexi|bulimi|purging|binge eating|"
        r"starv(?:e|ing) myself|stop eating|go without food|calorie "
        r"restriction|thinspo|pro[- ]?ana|restrictive eating)\b"
    ),
    "BodyImage": re.compile(
        r"(?i)\b(?:body image|body dysmorphia|too fat|too thin|"
        r"hate my body|weight shame|weight shaming)\b"
    ),
    "SelfHarm": re.compile(
        r"(?i)\b(?:self[- ]?harm|hurt myself|cut myself|overdose|"
        r"end my life|ending it all|won't be here|not going to be here)\b"
    ),
    "Suicide": re.compile(
        r"(?i)\b(?:suicid(?:e|al)|end my life|ending it all|"
        r"won't be here in the morning|not going to be here in the morning)\b"
    ),
    "AnimalCruelty": re.compile(
        r"(?i)\b(?:animal cruelty|cruelty to animals|cull(?:ing)? (?:the )?"
        r"(?:stray|feral)|poison bait|hurt (?:a|the) (?:dog|cat|animal|pet)|"
        r"neglect(?:ing|ed)? (?:a|the) (?:dog|cat|animal|pet))\b"
    ),
    "GraphicViolence": re.compile(
        r"(?i)\b(?:graphic violence|gore|dismember(?:ment|ed)|"
        r"decapitat(?:ion|ed)|mutilat(?:ion|ed))\b"
    ),
    "DomesticAbuse": re.compile(
        r"(?i)\b(?:domestic abuse|domestic violence|coercive control|"
        r"abusive partner|violent partner)\b"
    ),
    "SexualViolence": re.compile(
        r"(?i)\b(?:sexual assault|sexual violence|rape|raped)\b"
    ),
    "SubstanceMisuse": re.compile(
        r"(?i)\b(?:substance misuse|drug misuse|alcohol dependency|"
        r"alcohol dependence|addicted to (?:drugs|alcohol))\b"
    ),
}


def canonicalise_tags(tags: Iterable[Any] | None) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []

    for raw in tags or []:
        tag = str(raw).strip()
        if not tag:
            continue

        if tag in TAG_ALIASES:
            alias = TAG_ALIASES[tag]
            if alias is None:
                continue
            tag = alias

        if tag not in CONTROLLED_SENSITIVITY_TAGS or tag in seen:
            continue

        seen.add(tag)
        output.append(tag)

    order = {tag: index for index, tag in enumerate(CONTROLLED_SENSITIVITY_TAGS)}
    return sorted(output, key=lambda tag: order[tag])


def infer_sensitivity_tags(post: dict[str, Any]) -> list[str]:
    # Tags describe what the player can see. Use the visible post first, with
    # scenario/context as a fallback for incomplete generated copy.
    visible = " ".join(
        str(post.get(field, ""))
        for field in ("text", "scenario")
    )

    inferred = [
        tag for tag, pattern in TAG_PATTERNS.items()
        if pattern.search(visible)
    ]

    category = str(post.get("category", ""))
    action = str(post.get("correctAction", ""))

    # A Self-Harm moderation case always exposes self-harm-related content,
    # even when the wording is indirect.
    if category == "Self-Harm":
        inferred.append("SelfHarm")

    # Add Suicide only for crisis-style escalation language, not every
    # self-harm or eating-disorder case.
    if category == "Self-Harm" and action == "Escalate" and re.search(
        r"(?i)\b(?:suicid|end it all|end my life|goodbye|tonight|"
        r"let me go|don't try to stop me|no point anymore|disappear)\b",
        visible,
    ):
        inferred.append("Suicide")

    return canonicalise_tags(inferred)


def suggested_sensitivity_tags(
    post: dict[str, Any],
    required_tags: Iterable[Any] | None = None,
) -> list[str]:
    return canonicalise_tags(
        list(post.get("tags", []) or [])
        + list(required_tags or [])
        + infer_sensitivity_tags(post)
    )


def assign_sensitivity_tags(
    post: dict[str, Any],
    slot: dict[str, Any] | None = None,
) -> list[str]:
    required = (slot or {}).get("requiredTags", [])
    tags = suggested_sensitivity_tags(post, required)
    post["tags"] = tags
    return tags


def sensitivity_tag_errors(
    post: dict[str, Any],
    slot: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    actual = set(canonicalise_tags(post.get("tags", [])))
    required = set(canonicalise_tags((slot or {}).get("requiredTags", [])))

    missing = sorted(required - actual)
    if missing:
        errors.append(
            "Missing required sensitivity tag(s): " + ", ".join(missing) + "."
        )

    raw_tags = [str(tag) for tag in post.get("tags", []) or []]
    unknown = sorted(
        tag for tag in raw_tags
        if tag not in CONTROLLED_SENSITIVITY_TAGS
        and tag not in TAG_ALIASES
    )
    if unknown:
        errors.append(
            "Unknown sensitivity tag(s): " + ", ".join(unknown) + "."
        )

    return errors

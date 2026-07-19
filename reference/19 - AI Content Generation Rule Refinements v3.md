# AI Content Generation Rule Refinements — v3

This file records the design rationale behind the production runtime rules.

It is a living, versioned document and should be updated as the game changes.

## Core refinements

1. Fictionalise real artists, bands, songs, films, games, celebrities and brands
   by default in filler content.
2. Allow numeric usernames, but vary suffixes and username structures across a
   batch.
3. Use natural hashtag variation rather than a rigid maximum.
4. Judge whether the author promotes, reports, questions, warns about or
   condemns harmful content.
5. Keep `Remove` for obvious violations and `Escalate` for cases requiring
   specialist judgement or outside context.
6. Self-harm cases must actually involve self-harm, suicide risk,
   eating-disorder content or a relevant personal crisis.
7. Filler posts should sound like real social-media content rather than policy
   examples.
8. Generation rules are expected to evolve during development.

## Health misinformation

Use plausible wellness and medical misinformation themes including:

- fake alternatives to chemotherapy or radiotherapy
- cancer “cures”
- fertility supplements and fake infertility treatments
- pregnancy, miscarriage, postpartum and menopause misinformation
- hormone-balancing claims
- juice cleanses
- coffee enemas
- detox programmes
- restrictive diets presented as medical treatments
- fictional celebrity-style wellness companies
- encouragement to stop prescribed treatment

Do not copy a real celebrity, product, company or campaign.

Aim for approximately 55% female-oriented scenarios within the health-
misinformation subset and 45% gender-neutral or male-oriented scenarios.

This is a game-content balance target, not a claim about real-world prevalence.

Avoid sexist stereotypes and vary who spreads, questions, reports and debunks
the claims.

## Accessibility tags

Use controlled sensitivity tags in the existing `tags` array:

- Cancer
- Chemotherapy
- Fertility
- Pregnancy
- Miscarriage
- Menopause
- EatingDisorders
- BodyImage
- SelfHarm
- Suicide
- AnimalCruelty
- MedicalMisinformation
- GraphicViolence
- DomesticAbuse
- SexualViolence
- SubstanceMisuse

Tags describe what the player sees, including reporting and debunking content.

Future filtering should replace blocked filler with another eligible post and
must not penalise the player.

Story-critical sensitive posts should later support alternative versions,
reduced detail, summaries or warnings.

## Future world reactivity

Keep three concepts separate:

1. ordinary filler
2. reactive filler
3. fixed story content

Reactive content may later affect world state, such as approved blue-hat posts
causing more NPCs to wear blue hats.

Do not add world-reactivity fields until the Unity schema supports them.


## Task 4e refinement

Future generated content should follow the Task 4d backfill decisions:

- Scams that solicit credentials, money, identity, payment details or fake verification are FraudScam once parent reasons unlock.
- Dangerous challenges route to MisinformationPublicHarm/PublicSafety rather than ThreatViolence unless a target is threatened.
- Harmful medical misinformation is MisinformationPublicHarm, and HealthMedical once specialist reasons unlock.
- Day 3+ escalations need parent reasons; Day 10+ specialist misinformation needs specialist reasons.
- Blank explanations and real-world references are validation problems, not reviewer polish.

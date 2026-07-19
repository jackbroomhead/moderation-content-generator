# Recommended Existing Dataset Corrections

These are proposed corrections for the current source data. They have not been applied to the master workbook or JSON in this package.

## Missing primary reasons

### `DAY0-005`

- Primary: `ThreatViolence`
- Acceptable alternatives: `PrivacySensitiveInfo`, `HarassmentAbuse`
- Rationale: private address plus instruction to confront the target creates a credible real-world harm risk.

### `DAY1-003`

- Primary: `MisinformationPublicHarm`
- `allowNeedsReviewEscalation`: `true`
- Tag: `synthetic-media`
- Rationale: early synthetic-media cases remain under Misinformation / Public Harm.

### `DAY1-005`

- Primary: `PrivacySensitiveInfo`
- Acceptable: `HarassmentAbuse`
- `allowNeedsReviewEscalation`: `true`
- Rationale: private medical information is the dominant harm.

### `DAY4-008`

- Primary: `PrivacySensitiveInfo`
- Rationale: a driving licence is sensitive identity information even when shared with good intentions.

## Policy conflict to review

### `DAY5-011`

Current answer: Remove.

The post says the author feels dizzy and has a racing heart during a water fast. Under the approved policy, evidence of personal danger takes priority over removal for harmful promotion.

Recommended answer:

- `correctAction`: `Escalate`
- `correctEscalationReason`: `SelfHarmCrisis`
- possible `allowNeedsReviewEscalation`: `false` because the crisis signal is explicit.

## Quality correction

### `DAY1-006`

Current category and explanation are unsuitable.

Recommended:

- category: `Normal`
- action: `Approve`
- explanation: “The statement sounds ominous but contains no specific target, threat, plan or harmful action.”
- tags: `hyperbole`, `ambiguous-tone`

## Category aliases to normalise

- `normal` → `Normal`
- `scam` → `Fraud`
- `misinformation` → `Misinformation`
- `harassment` → `Harassment`

## Safe application process

1. Apply corrections to a working copy.
2. Run schema and duplicate validation.
3. Convert to JSON.
4. Test the corrected posts in Unity.
5. Do not overwrite the original workbook until the test build passes.

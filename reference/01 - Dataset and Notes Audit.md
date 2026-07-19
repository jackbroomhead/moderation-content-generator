# Dataset and Notes Audit

## Current source dataset

- Posts: **49**
- Days: **0–6**
- Approve: **21**
- Remove: **14**
- Escalate: **14**
- Difficulties: Easy 25, Medium 19, Hard 5
- Posts allowing a generic Needs Review escalation: **10**

## Existing primary escalation codes

- `ThreatViolence`
- `SelfHarmCrisis`
- `HarassmentAbuse`
- `FraudScam`
- `PrivacySensitiveInfo`
- `MisinformationPublicHarm`

Four escalation posts currently have no primary reason:

- `DAY0-005`
- `DAY1-003`
- `DAY1-005`
- `DAY4-008`

Recommended corrections are recorded in `09 - Existing Dataset Corrections.md`.

## Category inconsistencies

The current data contains aliases and case differences, including:

- `normal` and `Normal`
- `misinformation` and `Misinformation`
- `scam` and `Fraud`
- `harassment` and `Harassment`

The generator must use only the canonical values in `08 - permitted-values.json`.

## Rules confirmed from the design discussion

- The action set remains Approve, Remove and Escalate.
- Escalation reasons remain the original six parent categories.
- Needs Review is optional and not a primary JSON reason.
- Unsure is a separate gameplay deferral: no pay, no completed decision, and the post returns later.
- Obvious ordinary violations are removed; serious, uncertain, crisis, privacy or real-world-harm cases are escalated.
- Later difficulty comes from branching parent escalation reasons, account metadata, repeated behaviour and contextual evidence.
- Synthetic media starts under Misinformation / Public Harm and later becomes a specialist branch.
- Hate and extremism start as broader cases routed by dominant harm and split into specialist branches later.
- Ordinary spam is removed; coordinated platform manipulation becomes a later contextual challenge.
- Child-safety sexual content is entirely excluded from the game.

## Existing examples that conflict with the approved policy

`DAY5-011` describes a person feeling dizzy with a racing heart during a dangerous fast. Under the approved rule, personal crisis takes priority over simple content removal, so this post should be reviewed for `Escalate / SelfHarmCrisis`.

`DAY1-006` has an unclear explanation and an unsuitable Privacy category despite containing no private information. It should be rewritten or reclassified before being used as a model example.

## Source-use rule for the AI

Existing posts are style examples, not an answer key. The approved policy and permitted-values files are authoritative.

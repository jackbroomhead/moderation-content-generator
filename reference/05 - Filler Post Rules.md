# Filler Post Generation Rules — Approved v1

## Purpose

Generate believable background social-media posts that support the moderation loop without advancing the story.

## Required qualities

- fictional users, organisations and events;
- varied tone, spelling, punctuation, length and platform style;
- a controlled balance of Approve, Remove and Escalate outcomes;
- defensible action, parent escalation reason and explanation;
- enough context for the intended difficulty;
- no duplicate or near-duplicate ideas;
- no real private addresses, phone numbers, bank details or medical records;
- no real public figures where the post could be mistaken for a factual allegation;
- use only mechanics visible on the target day.

## Never generate

- story developments or scripted events;
- the Supervisor, Victoria, Theo, Fennec, the date counterpart or other protected recurring narrative identities;
- hacker-group contact, faction missions or corporate instructions;
- child sexualisation, grooming, exploitation or abuse;
- any deferred topic listed in `07 - Confirmed Decisions and Deferred Topics.md`;
- content designed purely for shock without a moderation-learning purpose.

## Current escalation restriction

Use only these primary reason codes:

- `ThreatViolence`
- `SelfHarmCrisis`
- `HarassmentAbuse`
- `FraudScam`
- `PrivacySensitiveInfo`
- `MisinformationPublicHarm`

Do not generate future specialist reason codes as `correctEscalationReason`.

## Needs Review

- `allowNeedsReviewEscalation` may be `true` only for genuinely ambiguous cases.
- The post must still contain a specific primary parent reason.
- Needs Review must not be allowed for obvious emergencies.

## Synthetic media

Before specialist branching exists:

- use `Misinformation` as the category for public-harm manipulation;
- use the dominant parent reason for fraud, privacy or harassment cases;
- add tags such as `synthetic-media`, `deepfake` or `specialist-later`;
- provide evidence such as provenance warnings, contradictory source information, impersonation signals or account context;
- never expect the player to detect a deepfake from image quality alone.

## Day rules

- Days 0–2: simple actions and self-contained evidence.
- Days 3–6: parent escalation reasons only.
- Day 6+: metadata may influence difficulty.
- Day 7+: specialist themes may appear, but current JSON still records a parent reason until the schema/UI is extended.

## Data rules

- Match the exact 25-field game schema.
- Use only canonical categories and values from `08 - permitted-values.json`.
- Use only `Approve`, `Remove` or `Escalate`.
- Use only `Easy`, `Medium` or `Hard`.
- Every Escalate post must have a specific primary reason.
- `acceptableEscalationReasons` may contain only the six approved parent codes.
- Generate to candidate files; never overwrite the master dataset.
- Filler IDs should use the agreed `DAYn-nnn` format and must not collide with story IDs.

## Quality validation

Reject or flag a generated post when:

- its action conflicts with the approved policy;
- it lacks evidence needed for the intended difficulty;
- the explanation merely repeats the answer;
- it uses an unavailable mechanic or specialist branch too early;
- it contains a protected story character;
- it duplicates an existing concept;
- it uses a deferred or excluded category;
- its text is grammatically broken in a way that is not intentional character voice.

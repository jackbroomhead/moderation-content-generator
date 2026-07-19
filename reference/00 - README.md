# AI Content Reference — Approved v1

**Status:** Approved for the first filler-post generator and Obsidian documentation pass.  
**Approved:** 2026-06-30

This package defines the moderation rules that the local AI must follow when creating non-story social-media posts for the game.

## Authority order

When sources disagree, use this order:

1. `02 - Moderation Policy.md`
2. `03 - Escalation Reasons.md`
3. `04 - Day Progression.md`
4. `05 - Filler Post Rules.md`
5. `08 - permitted-values.json`
6. Existing posts as style examples only
7. Older Obsidian notes and source imports

The existing dataset contains useful examples but also contains inconsistent category names, blank escalation reasons and a few policy conflicts. Do not copy those inconsistencies.

## Current escalation design

The player-facing escalation menu remains deliberately simple:

- Threat / Violence
- Self-Harm / Crisis
- Harassment / Abuse
- Fraud / Scam
- Privacy / Sensitive Info
- Misinformation / Public Harm
- Needs Review

The first six map to the six existing JSON reason codes. `Needs Review` is an optional UI answer controlled by `allowNeedsReviewEscalation`; it is not a primary JSON reason.

Later specialist mechanics may branch from these parent options. They must not be added as new top-level JSON reasons until the Unity UI and schema are intentionally extended.

## Package contents

- dataset and notes audit;
- approved moderation policy;
- parent escalation definitions and future branch design;
- day and difficulty progression;
- filler-generation rules;
- strict generation schema;
- permitted values and normalisation aliases;
- recommended corrections to the existing dataset;
- a focused Codex task for applying the policy to the live project.

## Important exclusions

The generator must never create child sexualisation, grooming, exploitation or abuse content. Several undecided topics are also blocked until rules are approved; see `07 - Confirmed Decisions and Deferred Topics.md`.

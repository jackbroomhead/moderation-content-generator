# Codex Task — Apply Approved Moderation Policy

## Goal

Apply the approved moderation policy to the live Obsidian vault and prepare the project for controlled local-AI filler generation.

## Inputs

- `AI_Content_Reference_Final/`
- the live `Moderation_Game` Obsidian folder;
- the current post workbook and JSON converter;
- the current Unity escalation-reason UI and day feature toggles.

## Required documentation changes

1. Add or update an authoritative Moderation Policy and Escalation Taxonomy note.
2. Preserve the original six parent escalation categories:
   - Threat / Violence
   - Self-Harm / Crisis
   - Harassment / Abuse
   - Fraud / Scam
   - Privacy / Sensitive Info
   - Misinformation / Public Harm
3. Document Needs Review as an optional UI answer, not a JSON primary reason.
4. Document Unsure as a future gameplay-only deferral with no schema change.
5. Document the day progression:
   - Days 0–2: core actions;
   - Days 3–6: original parent reason menu;
   - Day 7+: optional specialist branches.
6. Add filler-generation and story-exclusion rules.
7. Add the deferred-topic list and the absolute child-safety exclusion.

## Data changes

Do not overwrite the master workbook.

Create a working copy and propose corrections for:

- `DAY0-005`
- `DAY1-003`
- `DAY1-005`
- `DAY4-008`
- `DAY5-011`
- `DAY1-006`

Normalise category aliases using `08 - permitted-values.json`.

## Implementation constraints

- Do not add future specialist subreason codes to the active JSON schema yet.
- Do not replace the first-level escalation menu.
- Do not implement the specialist tree unless explicitly requested in a separate task.
- Do not edit story posts or protected narrative characters.
- Do not generate child-safety content.
- Keep all generated output in a separate candidate directory.

## Acceptance tests

- Every Escalate post has one of the six approved parent reason codes.
- Non-escalation posts have an empty reason and no acceptable alternatives.
- Needs Review is accepted only when `allowNeedsReviewEscalation=true`.
- No future subreason is stored as a current primary reason.
- Day 0–2 content does not require a player-facing reason selection.
- Day 3–6 uses the original parent menu.
- Existing story content is unchanged.
- The JSON converter and Unity loader still accept the working copy.

## Report back

List every file changed, every data row changed, validation results and any remaining contradiction. Do not silently resolve ambiguous cases.

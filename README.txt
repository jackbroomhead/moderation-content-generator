FULL PROFILE HOTFIX V2

Why this exists
---------------
The first full-profile test revealed two structural problems:

1. A Day 10 synthetic-media post remained semantically too similar to another
   slot.
2. A Day 13 model response returned "13" as a string and stale escalation
   values. JSON Schema then applied the Day 0-2 rule and rejected the post.

This update fixes those issues by:
- forcing all blueprint-controlled fields in code before schema validation;
- adding integer type guards to day-based schema conditions;
- making Day 10 synthetic-media scenarios more distinct;
- correcting the Day 3 scenario-option alignment;
- removing static sensitivity tags from mixed-topic slots;
- preventing animal starvation from being tagged as EatingDisorders;
- strengthening visible-evidence instructions;
- rerunning Day 6, Day 10 and Day 13 from clean checkpoints.

Install
-------
Stop any active Hermes/generator process.

Extract this ZIP directly into:

C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator

Replace the existing files.

Then start Hermes and tell it to read HERMES_TASK_HOTFIX.md.

Do not review the earlier Day 6 test batch; this package deliberately creates a
replacement Day 6 batch because the earlier one exposed blueprint/tag issues.

# Content Generator Fix v3

This patch fixes repeated validation failures where Gemma returns required
fields inside a nested `metadata` object.

## What it does

- Explicitly tells the model to use the game's flat post structure.
- Safely moves recognised fields out of `metadata` and onto the post root.
- Removes the unapproved `metadata` wrapper.
- Supplies empty schema-compatible defaults only for non-core metadata fields.
- Does not manufacture core content or policy decisions.
- Still validates category, action, escalation reason, day, difficulty,
  duplicate text, protected names, and excluded topics.
- Saves normalised payloads and logs every automatic structural change.

## Install

Copy `scripts\generate_posts.py` into the existing
`Content_Generator\scripts` folder and replace the v2 copy.

The existing `config.json`, virtual environment, inputs, references, and
outputs can remain unchanged.

Then run:

```powershell
.\run_generator.ps1
```

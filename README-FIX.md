# Content Generator Fix v2

This replaces the original batch generator with a more reliable version.

## What changed

- Generates one post per LM Studio request instead of all ten at once.
- Saves the complete raw LM Studio response before parsing it.
- Reports `finish_reason`, token usage, and whether reasoning was returned when
  the final message is empty.
- Validates each post before moving to the next.
- Combines the ten accepted posts into the same final batch format.
- Still never edits `input\posts.json`.

## Install

Copy these two items into the root of the existing `Content_Generator` folder:

- `config.json`
- `scripts\generate_posts.py`

Allow them to replace the earlier copies.

Then run:

```powershell
.\run_generator.ps1
```

The existing virtual environment and installed packages can be reused; setup does
not need to be run again.

Raw responses are saved under `output\reports`, including failed attempts.

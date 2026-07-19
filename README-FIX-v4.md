# Content Generator Fix v4

Gemma is now producing useful post content, but occasionally returns malformed
JSON despite the structured-output request.

This patch:

- tries normal `json.loads` first;
- uses `json-repair` only when the syntax is malformed;
- records that repair in the validation report;
- still applies the full JSON Schema and policy validation afterwards;
- does not silently accept invented fields, invalid actions, wrong categories,
  duplicate content, or invalid escalation reasons.

## Install

Copy these items into the root of the existing `Content_Generator` workspace:

- `scripts\generate_posts.py`
- `install_v4.ps1`

Replace the existing generator script.

Then run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install_v4.ps1
.\run_generator.ps1
```

The dependency installation only needs to be done once.

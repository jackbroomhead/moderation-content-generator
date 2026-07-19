# Hermes Task — Run Moderation Content Generation

Work from:

C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator

Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\run_generation_plan.ps1"
```

Rules:

- Do not edit policies, blueprints, approved content or generated posts.
- Do not approve content.
- Do not modify `input/posts.json`.
- Wait for the runner to finish even when its process returns a non-zero code.
- Read the newest `output\automation-logs\*-summary.txt`.
- A run is fully successful only when its status is `completed` and every
  enabled profile has `Success: True`.
- Report:
  1. overall status;
  2. every candidate path;
  3. every validation-report path;
  4. every failure-report path;
  5. any failed or retried profile.

# Content Generator v4 — Cleanup and Freeze

This package replaces the generator rules, reviewer and five production blueprints. It also includes the cleaned approved library built from the 121 reviewed posts.

## What v4 fixes

- fictional locations only;
- no platform names such as `PublicSquare` inside usernames;
- wider ordinary social-media topics;
- 14 Approve / 6 Remove / 5 Escalate per full batch;
- no more than four misinformation posts per 25;
- health misinformation capped at one per 25;
- cancer capped at one per rolling 75;
- platform metadata capped at three uses per 25;
- reviewer exports proper integers and booleans;
- action edits automatically clear stale escalation fields.

## Install

1. Close the reviewer and make sure no generation job is running.
2. Back up the current `Content_Generator` folder or commit it to Git.
3. Extract this package directly into:

   `C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator`

4. Allow Windows to merge folders and overwrite the files supplied by this package.
5. Do **not** replace your existing `config.json`, `run_generator.ps1`, model files or output history; this package intentionally does not contain them.

## Included cleaned library

The ready-built files are under:

`content-library\v4\approved`

The validation report is:

`content-library\v4\validation-report.txt`

To rebuild it later from everything in `output\approved`:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\build_content_library_v4.ps1"
```

The builder never edits the source approved files.

## Run only the five-post smoke test now

Keep LM Studio open, then run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\start_generation_background.ps1" -PlanPath ".\generation_plan_smoke_v4.json"
```

Check status with:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\check_generation_status.ps1"
```

The smoke batch should contain 3 Approve, 1 Remove and 1 Escalate post. Review those five in Streamlit before using the production plan.

## After the smoke test passes

Run one mixed 25-post test:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\start_generation_background.ps1" -PlanPath ".\generation_plan_production_test_v4.json"
```

Do not launch another multi-profile 75-post development run.

## Runtime/Unity selection

`config\content_selection_v4.json` defines the final feed quotas and eligibility rules. The Unity loader still needs to apply those rules when selecting filler. Authored story posts remain fixed.

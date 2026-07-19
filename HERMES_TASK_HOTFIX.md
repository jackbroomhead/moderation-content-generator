# Hermes Task — Run the Day 6, Day 10 and Day 13 Hotfix Test

Work from:

C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator

Do not run the long generation command directly in one foreground terminal call.

## Start the background run

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\start_generation_background.ps1" -PlanPath ".\generation_plan_hotfix_test.json"
```

This plan starts fresh checkpoints and runs:

- metadata, Day 6
- specialist-misinformation, Day 10
- hard-cases, Day 13

## Monitor

Every 60 seconds, run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\check_generation_status.ps1"
```

Continue until `State:` is no longer `running`.

## Report

Report:

1. final state;
2. success/failure and attempts for all three profiles;
3. candidate paths;
4. validation-report paths;
5. failure-report paths;
6. retries and warnings.

Do not approve posts. Do not edit policies, blueprints, generated posts or
`input\posts.json`.

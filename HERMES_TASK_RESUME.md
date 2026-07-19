# Hermes Task — Resume the Full Profile Test After Timeout

Work from:

C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator

The previous foreground terminal call timed out after 600 seconds. Do not run the
long generation command directly in one terminal tool call.

## Start

Run this short command:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\start_generation_background.ps1" -PlanPath ".\generation_plan_resume.json"
```

It starts the remaining work in a detached PowerShell process and returns
immediately.

The resume plan contains only:

- specialist-misinformation, Day 10
- hard-cases, Day 13

The Day 10 profile should reuse the existing accepted checkpoints and regenerate
only the four posts rejected by semantic duplicate detection.

## Monitor

Every 60 seconds, run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\check_generation_status.ps1"
```

Do not keep one terminal command open for more than 600 seconds.

Continue checking until `State:` is no longer `running`.

## Report

When finished, report:

1. final state;
2. success or failure of specialist-misinformation;
3. success or failure of hard-cases;
4. candidate paths;
5. validation-report paths;
6. failure-report paths;
7. retries and warnings.

Do not approve posts. Do not edit policies, blueprints, generated posts or
`input\posts.json`.

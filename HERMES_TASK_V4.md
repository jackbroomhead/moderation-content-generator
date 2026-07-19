# Hermes task — v4 smoke test

From the Content_Generator project root:

1. Verify LM Studio is reachable on port 1234.
2. Start `generation_plan_smoke_v4.json` with `start_generation_background.ps1`.
3. Report the returned process ID and log paths, then stop. Do not poll continuously and do not rerun the generator.

After the user confirms the job has finished, a separate task may read the newest progress, summary and manifest files and report the outcome.

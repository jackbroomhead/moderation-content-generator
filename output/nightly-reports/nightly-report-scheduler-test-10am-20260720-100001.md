# Nightly Candidate Generation Report

Timestamp: 2026-07-20T10:00:03
Status: timeout_still_running
Command used: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_nightly_generation.ps1 -TotalPosts 40 -Days 3 -MaxRuntimeMinutes 360 -Label "scheduler-test-10am"
Plan: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\nightly-plans\generation-plan-scheduler-test-10am-20260720-100001.json
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-100001-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-100001-run.log
Model endpoint: http://127.0.0.1:1234
LM Studio check: LM Studio responded at http://127.0.0.1:1234/v1/models.
LM Studio loaded models: qwen/qwen3.5-9b, qwen/qwen3.6-35b-a3b, google/gemma-4-12b-qat, google/gemma-4-e4b, text-embedding-nomic-embed-text-v1.5
Writer model: qwen/qwen3.5-9b
Embedding model: text-embedding-nomic-embed-text-v1.5
Requested TotalPosts: 40
Requested Days: 3
Generated candidate files:
Generated candidate count: 0
Generated IDs: 
Day distribution: 
Action distribution: 
Validation passed: False
Blocking errors: 0
Warnings: 0
Policy-quality warnings: 0
Duplicate/near-duplicate notes: 0
Ready for Streamlit review: False
Failure message: MaxRuntimeMinutes elapsed. The generation process was not killed; check status before starting another run.
Confirmation: no candidates were approved automatically.
Confirmation: nothing was published to Unity.
Confirmation: Unity StreamingAssets and Assets/Resources/posts.json were not touched by this script.

Open local review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review.ps1

Open LAN review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review_lan.ps1

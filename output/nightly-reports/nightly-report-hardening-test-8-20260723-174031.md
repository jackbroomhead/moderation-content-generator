# Nightly Candidate Generation Report

Timestamp: 2026-07-23T17:40:35
Status: completed_with_failures
Command used: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_nightly_generation.ps1 -TotalPosts 8 -DaysCsv "3,6,10,13" -MaxRuntimeMinutes 90 -RetryAttemptsPerProfile 4 -UnloadModelsOnFinish $true -Label "hardening-test-8"
Plan: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\nightly-plans\generation-plan-hardening-test-8-20260723-174031.json
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-run.log
Child summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-summary.txt
Wrapper stdout: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-hardening-test-8-20260723-174031-stdout.log
Wrapper stderr: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-hardening-test-8-20260723-174031-stderr.log
Model endpoint: http://127.0.0.1:1234
LM Studio check: LM Studio responded at http://127.0.0.1:1234/v1/models.
LM Studio loaded models: qwen/qwen3.5-9b, text-embedding-nomic-embed-text-v1.5, qwen/qwen3.6-35b-a3b, google/gemma-4-12b-qat, google/gemma-4-e4b
Writer model: qwen/qwen3.5-9b
Embedding model: text-embedding-nomic-embed-text-v1.5
Requested TotalPosts: 8
Requested Days: 3,6,10,13
Generated Days: 
Missing Expected Days: 3,6,10,13
Per-profile results:
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
Failure message: [2026-07-23T17:40:32] Starting generation run.
[2026-07-23T17:40:32] Fatal error: Exception setting "slot_start_index": "The property 'slot_start_index' cannot be found on this object. Verify that the property exists and can be set."
[2026-07-23T17:40:32] Restored original config.json.
Status: completed_with_failures
Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-summary.txt
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-run.log
Unload requested: True
Writer unload attempted: True
Embedding unload attempted: True
Writer still loaded after unload: False
Embedding still loaded after unload: False
Unload warnings/errors:
- writer unload output: Model "qwen/qwen3.5-9b" unloaded.
- embedding unload output: Model "text-embedding-nomic-embed-text-v1.5" unloaded.

Child summary tail:
- Status: completed_with_failures
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-run.log
- 
- Fatal error: Exception setting "slot_start_index": "The property 'slot_start_index' cannot be found on this object. Verify that the property exists and can be set."
- 

Wrapper stdout tail:
- [2026-07-23T17:40:32] Starting generation run.
- [2026-07-23T17:40:32] Fatal error: Exception setting "slot_start_index": "The property 'slot_start_index' cannot be found on this object. Verify that the property exists and can be set."
- [2026-07-23T17:40:32] Restored original config.json.
- Status: completed_with_failures
- Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-summary.txt
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-174032-run.log

Wrapper stderr tail:

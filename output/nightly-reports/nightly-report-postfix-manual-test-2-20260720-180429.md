# Nightly Candidate Generation Report

Timestamp: 2026-07-20T18:05:05
Status: completed_with_failures
Command used: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_nightly_generation.ps1 -TotalPosts 4 -DaysCsv "3,6,10,13" -MaxRuntimeMinutes 60 -Label "postfix-manual-test-2"
Plan: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\nightly-plans\generation-plan-postfix-manual-test-2-20260720-180429.json
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-run.log
Child summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-summary.txt
Wrapper stdout: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-postfix-manual-test-2-20260720-180429-stdout.log
Wrapper stderr: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-postfix-manual-test-2-20260720-180429-stderr.log
Model endpoint: http://127.0.0.1:1234
LM Studio check: LM Studio responded at http://127.0.0.1:1234/v1/models.
LM Studio loaded models: qwen/qwen3.5-9b, text-embedding-nomic-embed-text-v1.5, qwen/qwen3.6-35b-a3b, google/gemma-4-12b-qat, google/gemma-4-e4b
Writer model: qwen/qwen3.5-9b
Embedding model: text-embedding-nomic-embed-text-v1.5
Requested TotalPosts: 4
Requested Days: 3,6,10,13
Generated candidate files:
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day3-pilot-20260720-180431.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260720-180438.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260720-180446.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260720-180502.json
Generated candidate count: 4
Generated IDs: DAY3-139, DAY6-068, DAY10-089, DAY13-034
Day distribution: 10=1, 13=1, 3=1, 6=1
Action distribution: Approve=4
Validation passed: True
Blocking errors: 0
Warnings: 0
Policy-quality warnings: 0
Duplicate/near-duplicate notes: 6
Ready for Streamlit review: False
Failure message: [2026-07-20T18:04:30] Starting generation run.
[2026-07-20T18:04:30] Profile=postfix-manual-test-2-day3, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 467
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\17 - Day 3-5 Escalation Production Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 1 diverse Day 3 posts...

Post 1/1: DAY3-139 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=2, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day3-pilot-20260720-180431.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-pilot-20260720-180431-validation.txt
Elapsed: 0.1 minutes
The master input/posts.json was not modified.
[2026-07-20T18:04:38] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260720-180430-postfix-manual-test-2-day3-batch1-complete
[2026-07-20T18:04:38] Profile=postfix-manual-test-2-day3, batch=1 completed.
[2026-07-20T18:04:38] Profile=postfix-manual-test-2-day6, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 468
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\20 - Day 6-9 Metadata Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 1 diverse Day 6 posts...

Post 1/1: DAY6-068 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260720-180438.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260720-180438-validation.txt
Elapsed: 0.1 minutes
The master input/posts.json was not modified.
[2026-07-20T18:04:45] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260720-180430-postfix-manual-test-2-day6-batch1-complete
[2026-07-20T18:04:45] Profile=postfix-manual-test-2-day6, batch=1 completed.
[2026-07-20T18:04:45] Profile=postfix-manual-test-2-day10, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 469
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 1 diverse Day 10 posts...

Post 1/1: DAY10-089 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260720-180446.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260720-180446-validation.txt
Elapsed: 0.1 minutes
The master input/posts.json was not modified.
[2026-07-20T18:04:53] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260720-180430-postfix-manual-test-2-day10-batch1-complete
[2026-07-20T18:04:53] Profile=postfix-manual-test-2-day10, batch=1 completed.
[2026-07-20T18:04:53] Profile=postfix-manual-test-2-day13, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 470
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 1 diverse Day 13 posts...

Post 1/1: DAY13-034 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 1 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-180453-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-20T18:05:01] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-20T18:05:01] Profile=postfix-manual-test-2-day13, batch=1, attempt=2 of 2
Resuming checkpoint with 0/1 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 470
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 1 diverse Day 13 posts...

Post 1/1: DAY13-034 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260720-180502.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-180502-validation.txt
Elapsed: 0.1 minutes
The master input/posts.json was not modified.
[2026-07-20T18:05:05] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260720-180430-postfix-manual-test-2-day13-batch1-complete
[2026-07-20T18:05:05] Profile=postfix-manual-test-2-day13, batch=1 completed.
[2026-07-20T18:05:05] Restored original config.json.
Status: completed
Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-summary.txt
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-run.log

Child summary tail:
- Status: completed
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-run.log
- 
- Profile: postfix-manual-test-2-day3 | Batch: 1 | Success: True | Attempts: 1
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day3-pilot-20260720-180431.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-pilot-20260720-180431-validation.txt
- Failure report: 
- Error: 
- 
- Profile: postfix-manual-test-2-day6 | Batch: 1 | Success: True | Attempts: 1
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260720-180438.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260720-180438-validation.txt
- Failure report: 
- Error: 
- 
- Profile: postfix-manual-test-2-day10 | Batch: 1 | Success: True | Attempts: 1
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260720-180446.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260720-180446-validation.txt
- Failure report: 
- Error: 
- 
- Profile: postfix-manual-test-2-day13 | Batch: 1 | Success: True | Attempts: 2
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260720-180502.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-180502-validation.txt
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-180453-semantic-failed.txt
- Error: 
- 

Wrapper stdout tail:
- Running semantic duplicate detection...
- Semantic check rejected 1 post(s). See:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-180453-semantic-failed.txt
- Run the generator again; completed slots will be reused.
- [2026-07-20T18:05:01] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
- [2026-07-20T18:05:01] Profile=postfix-manual-test-2-day13, batch=1, attempt=2 of 2
- Resuming checkpoint with 0/1 posts.
- Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
- Runtime reference characters: 7,799
- Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
- Generated history posts: 470
- Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
- Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
- Chat model: qwen/qwen3.5-9b
- Chat API: LM Studio native /api/v1/chat
- Reasoning mode: off
- Writer prompt suffix: (none)
- Embedding model: text-embedding-nomic-embed-text-v1.5
- Generating 1 diverse Day 13 posts...
- 
- Post 1/1: DAY13-034 | Approve | Lifestyle | Easy
-   Attempt 1: defaults=5, repairs=1, fallbacks=0.
-   Attempt 1: accepted and checkpointed.
- 
- Running semantic duplicate detection...
- 
- Validation passed.
- Candidate:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260720-180502.json
- Report:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-180502-validation.txt
- Elapsed: 0.1 minutes
- The master input/posts.json was not modified.
- [2026-07-20T18:05:05] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260720-180430-postfix-manual-test-2-day13-batch1-complete
- [2026-07-20T18:05:05] Profile=postfix-manual-test-2-day13, batch=1 completed.
- [2026-07-20T18:05:05] Restored original config.json.
- Status: completed
- Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-summary.txt
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-180430-run.log

Wrapper stderr tail:
Confirmation: no candidates were approved automatically.
Confirmation: nothing was published to Unity.
Confirmation: Unity StreamingAssets and Assets/Resources/posts.json were not touched by this script.

Open local review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review.ps1

Open LAN review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review_lan.ps1

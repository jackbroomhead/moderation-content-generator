# Nightly Candidate Generation Report

Timestamp: 2026-07-21T00:04:19
Status: completed_with_failures
Command used: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_nightly_generation.ps1 -TotalPosts 40 -DaysCsv "3,6,10,13" -MaxRuntimeMinutes 360 -UnloadModelsOnFinish $true -Label "nightly"
Plan: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\nightly-plans\generation-plan-nightly-20260721-000001.json
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-run.log
Child summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-summary.txt
Wrapper stdout: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-nightly-20260721-000001-stdout.log
Wrapper stderr: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-nightly-20260721-000001-stderr.log
Model endpoint: http://127.0.0.1:1234
LM Studio check: LM Studio responded at http://127.0.0.1:1234/v1/models.
LM Studio loaded models: qwen/qwen3.5-9b, text-embedding-nomic-embed-text-v1.5, qwen/qwen3.6-35b-a3b, google/gemma-4-12b-qat, google/gemma-4-e4b
Writer model: qwen/qwen3.5-9b
Embedding model: text-embedding-nomic-embed-text-v1.5
Requested TotalPosts: 40
Requested Days: 3,6,10,13
Generated candidate files:
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260721-000108.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260721-000309.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260721-000410.json
Generated candidate count: 30
Generated IDs: DAY6-069, DAY6-070, DAY6-071, DAY6-072, DAY6-073, DAY6-074, DAY6-075, DAY6-076, DAY6-077, DAY6-078, DAY10-100, DAY10-101, DAY10-102, DAY10-103, DAY10-104, DAY10-105, DAY10-106, DAY10-107, DAY10-108, DAY10-109, DAY13-045, DAY13-046, DAY13-047, DAY13-048, DAY13-049, DAY13-050, DAY13-051, DAY13-052, DAY13-053, DAY13-054
Day distribution: 10=10, 13=10, 6=10
Action distribution: Approve=24, Escalate=3, Remove=3
Validation passed: True
Blocking errors: 0
Warnings: 0
Policy-quality warnings: 0
Duplicate/near-duplicate notes: 9
Ready for Streamlit review: False
Failure message: [2026-07-21T00:00:02] Starting generation run.
[2026-07-21T00:00:02] Profile=nightly-day3, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 491
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\17 - Day 3-5 Escalation Production Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 3 posts...

Post 1/10: DAY3-140 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY3-141 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 3/10: DAY3-142 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY3-143 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=6, repairs=0, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=6, repairs=0, fallbacks=0.
  Attempt 3: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-DAY3-143-20260721-000002-failed.txt
[2026-07-21T00:00:29] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-21T00:00:29] Profile=nightly-day3, batch=1, attempt=2 of 2
Resuming checkpoint with 3/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 491
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\17 - Day 3-5 Escalation Production Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 3 posts...

Post 1/10: DAY3-140 already checkpointed; skipping.

Post 2/10: DAY3-141 already checkpointed; skipping.

Post 3/10: DAY3-142 already checkpointed; skipping.

Post 4/10: DAY3-143 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 5/10: DAY3-144 | Escalate | Fraud | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 6/10: DAY3-145 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY3-146 | Approve | Normal | Easy
  Attempt 1: defaults=6, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY3-147 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=2, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 9/10: DAY3-148 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY3-149 | Approve | Harassment | Medium
  Attempt 1: defaults=6, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - posts.0: Additional properties are not allowed ('acceptableSpecialierReasons' was unexpected)
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 1 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-pilot-20260721-000029-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-21T00:01:07] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260721-000002-nightly-day3-batch1-failed
[2026-07-21T00:01:07] Profile=nightly-day3, batch=1 failed after 2 attempt(s).
[2026-07-21T00:01:07] Profile=nightly-day6, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 491
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\20 - Day 6-9 Metadata Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 6 posts...

Post 1/10: DAY6-069 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY6-070 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 3/10: DAY6-071 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY6-072 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely sustained harassment/brigading should be Escalate / HarassmentAbuse once reasons are unlocked.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 5/10: DAY6-073 | Escalate | Fraud | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Visible post text should refer to 'the app' or 'the platform' rather than repeatedly naming a fictional platform.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 6/10: DAY6-074 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY6-075 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY6-076 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Text is too similar to DAY6-069 (lexical similarity 1.00).
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 9/10: DAY6-077 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY6-078 | Approve | Harassment | Medium
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260721-000108.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260721-000108-validation.txt
Elapsed: 1.0 minutes
The master input/posts.json was not modified.
[2026-07-21T00:02:06] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260721-000002-nightly-day6-batch1-complete
[2026-07-21T00:02:06] Profile=nightly-day6, batch=1 completed.
[2026-07-21T00:02:06] Profile=nightly-day10, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 501
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 10 posts...

Post 1/10: DAY10-100 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY10-101 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 3/10: DAY10-102 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY10-103 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=0, fallbacks=0.
  Attempt 3: accepted and checkpointed.

Post 5/10: DAY10-104 | Escalate | Misinformation | Hard
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 6/10: DAY10-105 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY10-106 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY10-107 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 9/10: DAY10-108 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY10-109 | Approve | Harassment | Medium
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 1 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260721-000207-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-21T00:03:09] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-21T00:03:09] Profile=nightly-day10, batch=1, attempt=2 of 2
Resuming checkpoint with 9/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 501
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 10 posts...

Post 1/10: DAY10-100 already checkpointed; skipping.

Post 2/10: DAY10-101 already checkpointed; skipping.

Post 3/10: DAY10-102 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY10-103 already checkpointed; skipping.

Post 5/10: DAY10-104 already checkpointed; skipping.

Post 6/10: DAY10-105 already checkpointed; skipping.

Post 7/10: DAY10-106 already checkpointed; skipping.

Post 8/10: DAY10-107 already checkpointed; skipping.

Post 9/10: DAY10-108 already checkpointed; skipping.

Post 10/10: DAY10-109 already checkpointed; skipping.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260721-000309.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260721-000309-validation.txt
Elapsed: 0.1 minutes
The master input/posts.json was not modified.
[2026-07-21T00:03:14] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260721-000002-nightly-day10-batch1-complete
[2026-07-21T00:03:14] Profile=nightly-day10, batch=1 completed.
[2026-07-21T00:03:14] Profile=nightly-day13, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 511
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 13 posts...

Post 1/10: DAY13-045 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY13-046 | Approve | Normal | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 3/10: DAY13-047 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY13-048 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 5/10: DAY13-049 | Escalate | Misinformation | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 6/10: DAY13-050 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY13-051 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY13-052 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 9/10: DAY13-053 | Approve | Normal | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY13-054 | Approve | Harassment | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 1 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260721-000315-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-21T00:04:10] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-21T00:04:10] Profile=nightly-day13, batch=1, attempt=2 of 2
Resuming checkpoint with 9/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 511
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 13 posts...

Post 1/10: DAY13-045 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY13-046 already checkpointed; skipping.

Post 3/10: DAY13-047 already checkpointed; skipping.

Post 4/10: DAY13-048 already checkpointed; skipping.

Post 5/10: DAY13-049 already checkpointed; skipping.

Post 6/10: DAY13-050 already checkpointed; skipping.

Post 7/10: DAY13-051 already checkpointed; skipping.

Post 8/10: DAY13-052 already checkpointed; skipping.

Post 9/10: DAY13-053 already checkpointed; skipping.

Post 10/10: DAY13-054 already checkpointed; skipping.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260721-000410.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260721-000410-validation.txt
Elapsed: 0.1 minutes
The master input/posts.json was not modified.
[2026-07-21T00:04:16] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260721-000002-nightly-day13-batch1-complete
[2026-07-21T00:04:16] Profile=nightly-day13, batch=1 completed.
[2026-07-21T00:04:16] Restored original config.json.
Status: completed_with_failures
Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-summary.txt
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-run.log
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
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-run.log
- 
- Profile: nightly-day3 | Batch: 1 | Success: False | Attempts: 2
- Candidate: 
- Validation: 
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-pilot-20260721-000029-semantic-failed.txt
- Error: No validated candidate was produced.
- 
- Profile: nightly-day6 | Batch: 1 | Success: True | Attempts: 1
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260721-000108.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260721-000108-validation.txt
- Failure report: 
- Error: 
- 
- Profile: nightly-day10 | Batch: 1 | Success: True | Attempts: 2
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260721-000309.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260721-000309-validation.txt
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260721-000207-semantic-failed.txt
- Error: 
- 
- Profile: nightly-day13 | Batch: 1 | Success: True | Attempts: 2
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260721-000410.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260721-000410-validation.txt
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260721-000315-semantic-failed.txt
- Error: 
- 

Wrapper stdout tail:
- Generating 10 diverse Day 13 posts...
- 
- Post 1/10: DAY13-045 | Approve | Lifestyle | Easy
-   Attempt 1: defaults=5, repairs=1, fallbacks=0.
-   Attempt 1: accepted and checkpointed.
- 
- Post 2/10: DAY13-046 already checkpointed; skipping.
- 
- Post 3/10: DAY13-047 already checkpointed; skipping.
- 
- Post 4/10: DAY13-048 already checkpointed; skipping.
- 
- Post 5/10: DAY13-049 already checkpointed; skipping.
- 
- Post 6/10: DAY13-050 already checkpointed; skipping.
- 
- Post 7/10: DAY13-051 already checkpointed; skipping.
- 
- Post 8/10: DAY13-052 already checkpointed; skipping.
- 
- Post 9/10: DAY13-053 already checkpointed; skipping.
- 
- Post 10/10: DAY13-054 already checkpointed; skipping.
- 
- Running semantic duplicate detection...
- 
- Validation passed.
- Candidate:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260721-000410.json
- Report:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260721-000410-validation.txt
- Elapsed: 0.1 minutes
- The master input/posts.json was not modified.
- [2026-07-21T00:04:16] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260721-000002-nightly-day13-batch1-complete
- [2026-07-21T00:04:16] Profile=nightly-day13, batch=1 completed.
- [2026-07-21T00:04:16] Restored original config.json.
- Status: completed_with_failures
- Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-summary.txt
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260721-000002-run.log

Wrapper stderr tail:
Confirmation: no candidates were approved automatically.
Confirmation: nothing was published to Unity.
Confirmation: Unity StreamingAssets and Assets/Resources/posts.json were not touched by this script.

Open local review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review.ps1

Open LAN review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review_lan.ps1

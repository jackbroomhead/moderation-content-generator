# Nightly Candidate Generation Report

Timestamp: 2026-07-20T19:03:56
Status: completed_with_failures
Command used: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_nightly_generation.ps1 -TotalPosts 40 -DaysCsv "3,6,10,13" -MaxRuntimeMinutes 360 -Label "scheduler-test-7pm"
Plan: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\nightly-plans\generation-plan-scheduler-test-7pm-20260720-190000.json
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-run.log
Child summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-summary.txt
Wrapper stdout: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-scheduler-test-7pm-20260720-190000-stdout.log
Wrapper stderr: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-scheduler-test-7pm-20260720-190000-stderr.log
Model endpoint: http://127.0.0.1:1234
LM Studio check: LM Studio responded at http://127.0.0.1:1234/v1/models.
LM Studio loaded models: qwen/qwen3.5-9b, text-embedding-nomic-embed-text-v1.5, qwen/qwen3.6-35b-a3b, google/gemma-4-12b-qat, google/gemma-4-e4b
Writer model: qwen/qwen3.5-9b
Embedding model: text-embedding-nomic-embed-text-v1.5
Requested TotalPosts: 40
Requested Days: 3,6,10,13
Generated candidate files:
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260720-190239.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260720-190346.json
Generated candidate count: 20
Generated IDs: DAY10-090, DAY10-091, DAY10-092, DAY10-093, DAY10-094, DAY10-095, DAY10-096, DAY10-097, DAY10-098, DAY10-099, DAY13-035, DAY13-036, DAY13-037, DAY13-038, DAY13-039, DAY13-040, DAY13-041, DAY13-042, DAY13-043, DAY13-044
Day distribution: 10=10, 13=10
Action distribution: Approve=16, Escalate=2, Remove=2
Validation passed: True
Blocking errors: 0
Warnings: 0
Policy-quality warnings: 0
Duplicate/near-duplicate notes: 10
Ready for Streamlit review: False
Failure message: [2026-07-20T19:00:00] Starting generation run.
[2026-07-20T19:00:01] Profile=scheduler-test-7pm-day3, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 471
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
  Attempt 1: defaults=6, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 3/10: DAY3-142 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=2, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY3-143 | Remove | Fraud | Easy
  Attempt 1: defaults=6, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=6, repairs=0, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-DAY3-143-20260720-190001-failed.txt
[2026-07-20T19:00:26] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-20T19:00:26] Profile=scheduler-test-7pm-day3, batch=1, attempt=2 of 2
Resuming checkpoint with 3/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 471
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
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-DAY3-143-20260720-190026-failed.txt
[2026-07-20T19:00:34] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260720-190000-scheduler-test-7pm-day3-batch1-failed
[2026-07-20T19:00:34] Profile=scheduler-test-7pm-day3, batch=1 failed after 2 attempt(s).
[2026-07-20T19:00:34] Profile=scheduler-test-7pm-day6, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 471
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
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Visible post text should refer to 'the app' or 'the platform' rather than repeatedly naming a fictional platform.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 3/10: DAY6-071 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY6-072 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-DAY6-072-20260720-190034-failed.txt
[2026-07-20T19:01:04] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-20T19:01:04] Profile=scheduler-test-7pm-day6, batch=1, attempt=2 of 2
Resuming checkpoint with 3/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 471
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\20 - Day 6-9 Metadata Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 6 posts...

Post 1/10: DAY6-069 already checkpointed; skipping.

Post 2/10: DAY6-070 already checkpointed; skipping.

Post 3/10: DAY6-071 already checkpointed; skipping.

Post 4/10: DAY6-072 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 5/10: DAY6-073 | Escalate | Fraud | Hard
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 6/10: DAY6-074 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY6-075 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY6-076 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 9/10: DAY6-077 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY6-078 | Approve | Harassment | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 2 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260720-190105-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-20T19:01:45] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260720-190000-scheduler-test-7pm-day6-batch1-failed
[2026-07-20T19:01:45] Profile=scheduler-test-7pm-day6, batch=1 failed after 2 attempt(s).
[2026-07-20T19:01:45] Profile=scheduler-test-7pm-day10, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 471
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 10 posts...

Post 1/10: DAY10-090 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY10-091 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 3/10: DAY10-092 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY10-093 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 5/10: DAY10-094 | Escalate | Misinformation | Hard
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 6/10: DAY10-095 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY10-096 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY10-097 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 9/10: DAY10-098 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY10-099 | Approve | Harassment | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely sustained harassment/brigading should be Escalate / HarassmentAbuse once reasons are unlocked.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 1 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260720-190145-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-20T19:02:38] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-20T19:02:38] Profile=scheduler-test-7pm-day10, batch=1, attempt=2 of 2
Resuming checkpoint with 9/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 471
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 10 posts...

Post 1/10: DAY10-090 already checkpointed; skipping.

Post 2/10: DAY10-091 already checkpointed; skipping.

Post 3/10: DAY10-092 already checkpointed; skipping.

Post 4/10: DAY10-093 already checkpointed; skipping.

Post 5/10: DAY10-094 already checkpointed; skipping.

Post 6/10: DAY10-095 already checkpointed; skipping.

Post 7/10: DAY10-096 already checkpointed; skipping.

Post 8/10: DAY10-097 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 9/10: DAY10-098 already checkpointed; skipping.

Post 10/10: DAY10-099 already checkpointed; skipping.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260720-190239.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260720-190239-validation.txt
Elapsed: 0.1 minutes
The master input/posts.json was not modified.
[2026-07-20T19:02:45] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260720-190000-scheduler-test-7pm-day10-batch1-complete
[2026-07-20T19:02:45] Profile=scheduler-test-7pm-day10, batch=1 completed.
[2026-07-20T19:02:45] Profile=scheduler-test-7pm-day13, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 481
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 13 posts...

Post 1/10: DAY13-035 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY13-036 | Approve | Normal | Hard
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 3/10: DAY13-037 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY13-038 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 5/10: DAY13-039 | Escalate | Misinformation | Hard
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 6/10: DAY13-040 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY13-041 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY13-042 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Text is too similar to DAY13-035 (lexical similarity 1.00).
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 9/10: DAY13-043 | Approve | Normal | Hard
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY13-044 | Approve | Harassment | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 2 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-190246-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-20T19:03:45] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-20T19:03:46] Profile=scheduler-test-7pm-day13, batch=1, attempt=2 of 2
Resuming checkpoint with 8/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 481
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 13 posts...

Post 1/10: DAY13-035 already checkpointed; skipping.

Post 2/10: DAY13-036 already checkpointed; skipping.

Post 3/10: DAY13-037 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY13-038 already checkpointed; skipping.

Post 5/10: DAY13-039 already checkpointed; skipping.

Post 6/10: DAY13-040 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY13-041 already checkpointed; skipping.

Post 8/10: DAY13-042 already checkpointed; skipping.

Post 9/10: DAY13-043 already checkpointed; skipping.

Post 10/10: DAY13-044 already checkpointed; skipping.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260720-190346.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-190346-validation.txt
Elapsed: 0.2 minutes
The master input/posts.json was not modified.
[2026-07-20T19:03:56] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260720-190000-scheduler-test-7pm-day13-batch1-complete
[2026-07-20T19:03:56] Profile=scheduler-test-7pm-day13, batch=1 completed.
[2026-07-20T19:03:56] Restored original config.json.
Status: completed_with_failures
Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-summary.txt
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-run.log

Child summary tail:
- Status: completed_with_failures
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-run.log
- 
- Profile: scheduler-test-7pm-day3 | Batch: 1 | Success: False | Attempts: 2
- Candidate: 
- Validation: 
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-DAY3-143-20260720-190026-failed.txt
- Error: No validated candidate was produced.
- 
- Profile: scheduler-test-7pm-day6 | Batch: 1 | Success: False | Attempts: 2
- Candidate: 
- Validation: 
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260720-190105-semantic-failed.txt
- Error: No validated candidate was produced.
- 
- Profile: scheduler-test-7pm-day10 | Batch: 1 | Success: True | Attempts: 2
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260720-190239.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260720-190239-validation.txt
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260720-190145-semantic-failed.txt
- Error: 
- 
- Profile: scheduler-test-7pm-day13 | Batch: 1 | Success: True | Attempts: 2
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260720-190346.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-190346-validation.txt
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-190246-semantic-failed.txt
- Error: 
- 

Wrapper stdout tail:
- Post 1/10: DAY13-035 already checkpointed; skipping.
- 
- Post 2/10: DAY13-036 already checkpointed; skipping.
- 
- Post 3/10: DAY13-037 | Approve | Public Information | Easy
-   Attempt 1: defaults=5, repairs=1, fallbacks=0.
-   Attempt 1: accepted and checkpointed.
- 
- Post 4/10: DAY13-038 already checkpointed; skipping.
- 
- Post 5/10: DAY13-039 already checkpointed; skipping.
- 
- Post 6/10: DAY13-040 | Approve | News / Public Event | Easy
-   Attempt 1: defaults=5, repairs=1, fallbacks=0.
-   Attempt 1: accepted and checkpointed.
- 
- Post 7/10: DAY13-041 already checkpointed; skipping.
- 
- Post 8/10: DAY13-042 already checkpointed; skipping.
- 
- Post 9/10: DAY13-043 already checkpointed; skipping.
- 
- Post 10/10: DAY13-044 already checkpointed; skipping.
- 
- Running semantic duplicate detection...
- 
- Validation passed.
- Candidate:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260720-190346.json
- Report:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260720-190346-validation.txt
- Elapsed: 0.2 minutes
- The master input/posts.json was not modified.
- [2026-07-20T19:03:56] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260720-190000-scheduler-test-7pm-day13-batch1-complete
- [2026-07-20T19:03:56] Profile=scheduler-test-7pm-day13, batch=1 completed.
- [2026-07-20T19:03:56] Restored original config.json.
- Status: completed_with_failures
- Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-summary.txt
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260720-190000-run.log

Wrapper stderr tail:
Confirmation: no candidates were approved automatically.
Confirmation: nothing was published to Unity.
Confirmation: Unity StreamingAssets and Assets/Resources/posts.json were not touched by this script.

Open local review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review.ps1

Open LAN review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review_lan.ps1

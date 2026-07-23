# Nightly Candidate Generation Report

Timestamp: 2026-07-22T00:04:31
Status: completed_with_failures
Command used: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_nightly_generation.ps1 -TotalPosts 40 -DaysCsv "3,6,10,13" -MaxRuntimeMinutes 360 -UnloadModelsOnFinish $true -Label "nightly"
Plan: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\nightly-plans\generation-plan-nightly-20260722-000001.json
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-run.log
Child summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-summary.txt
Wrapper stdout: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-nightly-20260722-000001-stdout.log
Wrapper stderr: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-nightly-20260722-000001-stderr.log
Model endpoint: http://127.0.0.1:1234
LM Studio check: LM Studio responded at http://127.0.0.1:1234/v1/models.
LM Studio loaded models: qwen/qwen3.5-9b, text-embedding-nomic-embed-text-v1.5, qwen/qwen3.6-35b-a3b, google/gemma-4-12b-qat, google/gemma-4-e4b
Writer model: qwen/qwen3.5-9b
Embedding model: text-embedding-nomic-embed-text-v1.5
Requested TotalPosts: 40
Requested Days: 3,6,10,13
Generated candidate files:
Generated candidate count: 0
Generated IDs: 
Day distribution: 
Action distribution: 
Validation passed: True
Blocking errors: 0
Warnings: 0
Policy-quality warnings: 0
Duplicate/near-duplicate notes: 10
Ready for Streamlit review: False
Failure message: [2026-07-22T00:00:02] Starting generation run.
[2026-07-22T00:00:02] Profile=nightly-day3, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 521
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
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY3-143 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=6, repairs=0, fallbacks=0.
  Attempt 3: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-DAY3-143-20260722-000003-failed.txt
[2026-07-22T00:00:29] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-22T00:00:29] Profile=nightly-day3, batch=1, attempt=2 of 2
Resuming checkpoint with 3/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 521
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
  Attempt 2: defaults=6, repairs=0, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: accepted and checkpointed.

Post 5/10: DAY3-144 | Escalate | Fraud | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Contains an email address; use non-usable fictional context.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 6/10: DAY3-145 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY3-146 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY3-147 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 9/10: DAY3-148 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY3-149 | Approve | Harassment | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 1 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-pilot-20260722-000030-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-22T00:01:12] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260722-000002-nightly-day3-batch1-failed
[2026-07-22T00:01:12] Profile=nightly-day3, batch=1 failed after 2 attempt(s).
[2026-07-22T00:01:12] Profile=nightly-day6, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 521
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\20 - Day 6-9 Metadata Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 6 posts...

Post 1/10: DAY6-079 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY6-080 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 3/10: DAY6-081 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY6-082 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=0, fallbacks=0.
  Attempt 3: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-DAY6-082-20260722-000112-failed.txt
[2026-07-22T00:01:37] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-22T00:01:37] Profile=nightly-day6, batch=1, attempt=2 of 2
Resuming checkpoint with 3/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 521
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\20 - Day 6-9 Metadata Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 6 posts...

Post 1/10: DAY6-079 already checkpointed; skipping.

Post 2/10: DAY6-080 already checkpointed; skipping.

Post 3/10: DAY6-081 already checkpointed; skipping.

Post 4/10: DAY6-082 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 5/10: DAY6-083 | Escalate | Fraud | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - This is obvious credential theft and should normally be Remove, not Escalate.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 6/10: DAY6-084 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY6-085 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY6-086 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 9/10: DAY6-087 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY6-088 | Approve | Harassment | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 2 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260722-000138-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-22T00:02:13] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260722-000002-nightly-day6-batch1-failed
[2026-07-22T00:02:13] Profile=nightly-day6, batch=1 failed after 2 attempt(s).
[2026-07-22T00:02:13] Profile=nightly-day10, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 521
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 10 posts...

Post 1/10: DAY10-110 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY10-111 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 3/10: DAY10-112 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY10-113 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 5/10: DAY10-114 | Escalate | Misinformation | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 6/10: DAY10-115 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY10-116 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY10-117 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 9/10: DAY10-118 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY10-119 | Approve | Harassment | Medium
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 2 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260722-000214-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-22T00:03:01] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-22T00:03:01] Profile=nightly-day10, batch=1, attempt=2 of 2
Resuming checkpoint with 8/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 521
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 10 posts...

Post 1/10: DAY10-110 already checkpointed; skipping.

Post 2/10: DAY10-111 already checkpointed; skipping.

Post 3/10: DAY10-112 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY10-113 already checkpointed; skipping.

Post 5/10: DAY10-114 | Escalate | Misinformation | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 6/10: DAY10-115 already checkpointed; skipping.

Post 7/10: DAY10-116 already checkpointed; skipping.

Post 8/10: DAY10-117 already checkpointed; skipping.

Post 9/10: DAY10-118 already checkpointed; skipping.

Post 10/10: DAY10-119 already checkpointed; skipping.

Running semantic duplicate detection...
Semantic check rejected 2 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260722-000302-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-22T00:03:13] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260722-000002-nightly-day10-batch1-failed
[2026-07-22T00:03:13] Profile=nightly-day10, batch=1 failed after 2 attempt(s).
[2026-07-22T00:03:13] Profile=nightly-day13, batch=1, attempt=1 of 2
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 521
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 13 posts...

Post 1/10: DAY13-055 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY13-056 | Approve | Normal | Hard
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 3/10: DAY13-057 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY13-058 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=0, fallbacks=0.
  Attempt 3: accepted and checkpointed.

Post 5/10: DAY13-059 | Escalate | Misinformation | Hard
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 6/10: DAY13-060 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY13-061 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 8/10: DAY13-062 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Text is too similar to DAY13-055 (lexical similarity 1.00).
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 9/10: DAY13-063 | Approve | Normal | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 10/10: DAY13-064 | Approve | Harassment | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 3 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260722-000313-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-22T00:04:14] No valid candidate/validation pair was produced. Retrying with accepted checkpoints preserved.
[2026-07-22T00:04:14] Profile=nightly-day13, batch=1, attempt=2 of 2
Resuming checkpoint with 7/10 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 521
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: (none)
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 10 diverse Day 13 posts...

Post 1/10: DAY13-055 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/10: DAY13-056 already checkpointed; skipping.

Post 3/10: DAY13-057 | Approve | Public Information | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 4/10: DAY13-058 already checkpointed; skipping.

Post 5/10: DAY13-059 already checkpointed; skipping.

Post 6/10: DAY13-060 | Approve | News / Public Event | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 7/10: DAY13-061 already checkpointed; skipping.

Post 8/10: DAY13-062 already checkpointed; skipping.

Post 9/10: DAY13-063 already checkpointed; skipping.

Post 10/10: DAY13-064 already checkpointed; skipping.

Running semantic duplicate detection...
Semantic check rejected 1 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260722-000414-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-22T00:04:29] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260722-000002-nightly-day13-batch1-failed
[2026-07-22T00:04:29] Profile=nightly-day13, batch=1 failed after 2 attempt(s).
[2026-07-22T00:04:29] Restored original config.json.
Status: completed_with_failures
Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-summary.txt
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-run.log
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
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-run.log
- 
- Profile: nightly-day3 | Batch: 1 | Success: False | Attempts: 2
- Candidate: 
- Validation: 
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-pilot-20260722-000030-semantic-failed.txt
- Error: No validated candidate was produced.
- 
- Profile: nightly-day6 | Batch: 1 | Success: False | Attempts: 2
- Candidate: 
- Validation: 
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260722-000138-semantic-failed.txt
- Error: No validated candidate was produced.
- 
- Profile: nightly-day10 | Batch: 1 | Success: False | Attempts: 2
- Candidate: 
- Validation: 
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260722-000302-semantic-failed.txt
- Error: No validated candidate was produced.
- 
- Profile: nightly-day13 | Batch: 1 | Success: False | Attempts: 2
- Candidate: 
- Validation: 
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260722-000414-semantic-failed.txt
- Error: No validated candidate was produced.
- 

Wrapper stdout tail:
- Embedding model: text-embedding-nomic-embed-text-v1.5
- Generating 10 diverse Day 13 posts...
- 
- Post 1/10: DAY13-055 | Approve | Lifestyle | Easy
-   Attempt 1: defaults=5, repairs=1, fallbacks=0.
-   Attempt 1: accepted and checkpointed.
- 
- Post 2/10: DAY13-056 already checkpointed; skipping.
- 
- Post 3/10: DAY13-057 | Approve | Public Information | Easy
-   Attempt 1: defaults=5, repairs=1, fallbacks=0.
-   Attempt 1: accepted and checkpointed.
- 
- Post 4/10: DAY13-058 already checkpointed; skipping.
- 
- Post 5/10: DAY13-059 already checkpointed; skipping.
- 
- Post 6/10: DAY13-060 | Approve | News / Public Event | Easy
-   Attempt 1: defaults=5, repairs=1, fallbacks=0.
-   Attempt 1: accepted and checkpointed.
- 
- Post 7/10: DAY13-061 already checkpointed; skipping.
- 
- Post 8/10: DAY13-062 already checkpointed; skipping.
- 
- Post 9/10: DAY13-063 already checkpointed; skipping.
- 
- Post 10/10: DAY13-064 already checkpointed; skipping.
- 
- Running semantic duplicate detection...
- Semantic check rejected 1 post(s). See:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260722-000414-semantic-failed.txt
- Run the generator again; completed slots will be reused.
- [2026-07-22T00:04:29] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260722-000002-nightly-day13-batch1-failed
- [2026-07-22T00:04:29] Profile=nightly-day13, batch=1 failed after 2 attempt(s).
- [2026-07-22T00:04:29] Restored original config.json.
- Status: completed_with_failures
- Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-summary.txt
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260722-000002-run.log

Wrapper stderr tail:

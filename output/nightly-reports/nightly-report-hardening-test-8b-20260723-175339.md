# Nightly Candidate Generation Report

Timestamp: 2026-07-23T17:55:26
Status: completed_with_failures
Command used: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_nightly_generation.ps1 -TotalPosts 8 -DaysCsv "3,6,10,13" -MaxRuntimeMinutes 90 -RetryAttemptsPerProfile 4 -UnloadModelsOnFinish $true -Label "hardening-test-8b"
Plan: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\nightly-plans\generation-plan-hardening-test-8b-20260723-175339.json
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-run.log
Child summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-summary.txt
Wrapper stdout: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-hardening-test-8b-20260723-175339-stdout.log
Wrapper stderr: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-hardening-test-8b-20260723-175339-stderr.log
Model endpoint: http://127.0.0.1:1234
LM Studio check: LM Studio responded at http://127.0.0.1:1234/v1/models.
LM Studio loaded models: qwen/qwen3.5-9b, text-embedding-nomic-embed-text-v1.5, qwen/qwen3.6-35b-a3b, google/gemma-4-12b-qat, google/gemma-4-e4b
Writer model: qwen/qwen3.5-9b
Embedding model: text-embedding-nomic-embed-text-v1.5
Requested TotalPosts: 8
Requested Days: 3,6,10,13
Generated Days: 3,6,10,13
Missing Expected Days: 
Per-profile results:
- hardening-test-8b-day3: day=3, requested=2, generated=2, success=True, attempts=1, failure=
- hardening-test-8b-day6: day=6, requested=2, generated=2, success=True, attempts=2, failure=
- hardening-test-8b-day10: day=10, requested=2, generated=2, success=True, attempts=3, failure=
- hardening-test-8b-day13: day=13, requested=2, generated=2, success=True, attempts=1, failure=
Generated candidate files:
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day3-pilot-20260723-175340.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260723-175413.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260723-175446.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260723-175458.json
Generated candidate count: 8
Generated IDs: DAY3-140, DAY3-141, DAY6-089, DAY6-090, DAY10-110, DAY10-111, DAY13-055, DAY13-056
Day distribution: 10=2, 13=2, 3=2, 6=2
Action distribution: Approve=4, Escalate=1, Remove=3
Validation passed: True
Blocking errors: 0
Warnings: 0
Policy-quality warnings: 0
Duplicate/near-duplicate notes: 6
Ready for Streamlit review: False
Failure message: [2026-07-23T17:53:39] Starting generation run.
[2026-07-23T17:53:40] Profile=hardening-test-8b-day3, batch=1, attempt=1 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 531
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\17 - Day 3-5 Escalation Production Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively.

Day 3 should be simple but mixed across Approve, Remove and Escalate. Avoid obvious repeated credential-scam templates and hobby-completion approve posts.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 3 posts...

Post 1/2: DAY3-140 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 2/2: DAY3-141 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day3-pilot-20260723-175340.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-pilot-20260723-175340-validation.txt
Elapsed: 0.2 minutes
The master input/posts.json was not modified.
[2026-07-23T17:53:54] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260723-175339-hardening-test-8b-day3-batch1-complete
[2026-07-23T17:53:54] Profile=hardening-test-8b-day3, batch=1 completed.
[2026-07-23T17:53:54] Profile=hardening-test-8b-day6, batch=1, attempt=1 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 533
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\20 - Day 6-9 Metadata Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively.

Day 6 must make account metadata matter in at least some posts. Vary account age, verification, previous flags, platform and location.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 6 posts...

Post 1/2: DAY6-089 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 2 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
    - Avoid overused hobby/craft/baking/gardening themes in nightly output.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Avoid overused hobby/craft/baking/gardening themes in nightly output.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: accepted and checkpointed.

Post 2/2: DAY6-090 | Remove | Spam | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...
Semantic check rejected 1 post(s). See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260723-175354-semantic-failed.txt
Run the generator again; completed slots will be reused.
[2026-07-23T17:54:13] No valid candidate/validation pair was produced. Retrying with diversity hardening.
[2026-07-23T17:54:13] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260723-175339-hardening-test-8b-day6-batch1-semantic-retry2
[2026-07-23T17:54:13] Archived semantic-failure checkpoints before retry attempt 2.
[2026-07-23T17:54:13] Profile=hardening-test-8b-day6, batch=1, attempt=2 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 533
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\20 - Day 6-9 Metadata Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively.

Day 6 must make account metadata matter in at least some posts. Vary account age, verification, previous flags, platform and location.

NIGHTLY DIVERSITY RETRY: Avoid previous failed themes and avoid hobby/craft/baking/gardening/public-notice templates. Change scenario type, author voice, tone, text structure, metadata tuple and policy category where the blueprint allows it. Do not use 'finally finished', pottery, sourdough, candles, vinyl, library notices, community festivals, obvious credential-verification scams, generic public-safety rumour templates, or raw JSON fragments inside visible post text. For Day 10 and Day 13, prefer specialist misinformation, metadata-aware ambiguity, Needs Review-acceptable cases and hard escalation boundaries over easy approve filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 6 posts...

Post 1/2: DAY6-089 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/2: DAY6-090 | Remove | Spam | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260723-175413.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260723-175413-validation.txt
Elapsed: 0.2 minutes
The master input/posts.json was not modified.
[2026-07-23T17:54:23] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260723-175339-hardening-test-8b-day6-batch1-complete
[2026-07-23T17:54:23] Profile=hardening-test-8b-day6, batch=1 completed.
[2026-07-23T17:54:23] Profile=hardening-test-8b-day10, batch=1, attempt=1 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 535
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively.

Day 10 must include specialist misinformation or hard public-harm misinformation boundaries. Do not let the batch be dominated by Lifestyle/Easy/Approve filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 10 posts...

Post 1/2: DAY10-110 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-DAY10-110-20260723-175423-failed.txt
[2026-07-23T17:54:35] No valid candidate/validation pair was produced. Retrying with diversity hardening.
[2026-07-23T17:54:35] Profile=hardening-test-8b-day10, batch=1, attempt=2 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 535
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively.

Day 10 must include specialist misinformation or hard public-harm misinformation boundaries. Do not let the batch be dominated by Lifestyle/Easy/Approve filler.

NIGHTLY DIVERSITY RETRY: Avoid previous failed themes and avoid hobby/craft/baking/gardening/public-notice templates. Change scenario type, author voice, tone, text structure, metadata tuple and policy category where the blueprint allows it. Do not use 'finally finished', pottery, sourdough, candles, vinyl, library notices, community festivals, obvious credential-verification scams, generic public-safety rumour templates, or raw JSON fragments inside visible post text. For Day 10 and Day 13, prefer specialist misinformation, metadata-aware ambiguity, Needs Review-acceptable cases and hard escalation boundaries over easy approve filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 10 posts...

Post 1/2: DAY10-110 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-DAY10-110-20260723-175435-failed.txt
[2026-07-23T17:54:45] No valid candidate/validation pair was produced. Retrying with diversity hardening.
[2026-07-23T17:54:45] Profile=hardening-test-8b-day10, batch=1, attempt=3 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 535
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively.

Day 10 must include specialist misinformation or hard public-harm misinformation boundaries. Do not let the batch be dominated by Lifestyle/Easy/Approve filler.

NIGHTLY DIVERSITY RETRY: Avoid previous failed themes and avoid hobby/craft/baking/gardening/public-notice templates. Change scenario type, author voice, tone, text structure, metadata tuple and policy category where the blueprint allows it. Do not use 'finally finished', pottery, sourdough, candles, vinyl, library notices, community festivals, obvious credential-verification scams, generic public-safety rumour templates, or raw JSON fragments inside visible post text. For Day 10 and Day 13, prefer specialist misinformation, metadata-aware ambiguity, Needs Review-acceptable cases and hard escalation boundaries over easy approve filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 10 posts...

Post 1/2: DAY10-110 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/2: DAY10-111 | Escalate | Misinformation | Hard
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260723-175446.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260723-175446-validation.txt
Elapsed: 0.2 minutes
The master input/posts.json was not modified.
[2026-07-23T17:54:57] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260723-175339-hardening-test-8b-day10-batch1-complete
[2026-07-23T17:54:57] Profile=hardening-test-8b-day10, batch=1 completed.
[2026-07-23T17:54:57] Profile=hardening-test-8b-day13, batch=1, attempt=1 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 537
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively.

Day 13 should emphasise hard overlaps, Needs Review-acceptable cases, specialist escalation and non-obvious escalation boundaries. Pure filler should be rare.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 13 posts...

Post 1/2: DAY13-055 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 2 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
    - Avoid overused hobby/craft/baking/gardening themes in nightly output.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Avoid repeated public notice, library, maintenance or festival templates.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: accepted and checkpointed.

Post 2/2: DAY13-056 | Remove | Spam | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Uses a live-looking URL; use [link removed].
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260723-175458.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260723-175458-validation.txt
Elapsed: 0.4 minutes
The master input/posts.json was not modified.
[2026-07-23T17:55:24] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260723-175339-hardening-test-8b-day13-batch1-complete
[2026-07-23T17:55:24] Profile=hardening-test-8b-day13, batch=1 completed.
[2026-07-23T17:55:24] Restored original config.json.
Status: completed
Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-summary.txt
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-run.log
Unload requested: True
Writer unload attempted: True
Embedding unload attempted: True
Writer still loaded after unload: False
Embedding still loaded after unload: False
Unload warnings/errors:
- writer unload output: Model "qwen/qwen3.5-9b" unloaded.
- embedding unload output: Model "text-embedding-nomic-embed-text-v1.5" unloaded.

Child summary tail:
- Status: completed
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-run.log
- 
- Profile: hardening-test-8b-day3 | Batch: 1 | Success: True | Attempts: 1 | Requested: 2 | Generated: 2 | Target day: 3
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day3-pilot-20260723-175340.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-pilot-20260723-175340-validation.txt
- Failure report: 
- Error: 
- 
- Profile: hardening-test-8b-day6 | Batch: 1 | Success: True | Attempts: 2 | Requested: 2 | Generated: 2 | Target day: 6
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260723-175413.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260723-175413-validation.txt
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260723-175354-semantic-failed.txt
- Error: 
- 
- Profile: hardening-test-8b-day10 | Batch: 1 | Success: True | Attempts: 3 | Requested: 2 | Generated: 2 | Target day: 10
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day10-pilot-20260723-175446.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-pilot-20260723-175446-validation.txt
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-DAY10-110-20260723-175435-failed.txt
- Error: 
- 
- Profile: hardening-test-8b-day13 | Batch: 1 | Success: True | Attempts: 1 | Requested: 2 | Generated: 2 | Target day: 13
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260723-175458.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260723-175458-validation.txt
- Failure report: 
- Error: 
- 

Wrapper stdout tail:
- Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively.
- 
- Day 13 should emphasise hard overlaps, Needs Review-acceptable cases, specialist escalation and non-obvious escalation boundaries. Pure filler should be rare.
- Embedding model: text-embedding-nomic-embed-text-v1.5
- Generating 2 diverse Day 13 posts...
- 
- Post 1/2: DAY13-055 | Approve | Normal | Easy
-   Attempt 1: defaults=5, repairs=0, fallbacks=0.
-   Attempt 1: rejected with 2 issue(s).
-     - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
-     - Avoid overused hobby/craft/baking/gardening themes in nightly output.
-   Attempt 2: defaults=5, repairs=0, fallbacks=0.
-   Attempt 2: rejected with 1 issue(s).
-     - Avoid repeated public notice, library, maintenance or festival templates.
-   Attempt 3: defaults=5, repairs=1, fallbacks=0.
-   Attempt 3: accepted and checkpointed.
- 
- Post 2/2: DAY13-056 | Remove | Spam | Easy
-   Attempt 1: defaults=5, repairs=1, fallbacks=0.
-   Attempt 1: rejected with 1 issue(s).
-     - Uses a live-looking URL; use [link removed].
-   Attempt 2: defaults=5, repairs=0, fallbacks=0.
-   Attempt 2: accepted and checkpointed.
- 
- Running semantic duplicate detection...
- 
- Validation passed.
- Candidate:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260723-175458.json
- Report:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260723-175458-validation.txt
- Elapsed: 0.4 minutes
- The master input/posts.json was not modified.
- [2026-07-23T17:55:24] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260723-175339-hardening-test-8b-day13-batch1-complete
- [2026-07-23T17:55:24] Profile=hardening-test-8b-day13, batch=1 completed.
- [2026-07-23T17:55:24] Restored original config.json.
- Status: completed
- Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-summary.txt
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-175339-run.log

Wrapper stderr tail:
Confirmation: no candidates were approved automatically.
Confirmation: nothing was published to Unity.
Confirmation: Unity StreamingAssets and Assets/Resources/posts.json were not touched by this script.

Open local review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review.ps1

Open LAN review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review_lan.ps1

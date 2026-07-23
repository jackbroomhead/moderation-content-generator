# Nightly Candidate Generation Report

Timestamp: 2026-07-23T18:35:55
Status: completed_with_failures
Command used: powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_nightly_generation.ps1 -TotalPosts 8 -DaysCsv "3,6,10,13" -MaxRuntimeMinutes 90 -RetryAttemptsPerProfile 4 -UnloadModelsOnFinish $true -Label "hardening-test-8c"
Plan: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\nightly-plans\generation-plan-hardening-test-8c-20260723-183328.json
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-run.log
Child summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-summary.txt
Wrapper stdout: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-hardening-test-8c-20260723-183328-stdout.log
Wrapper stderr: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\nightly-hardening-test-8c-20260723-183328-stderr.log
Model endpoint: http://127.0.0.1:1234
LM Studio check: LM Studio responded at http://127.0.0.1:1234/v1/models.
LM Studio loaded models: qwen/qwen3.5-9b, text-embedding-nomic-embed-text-v1.5, qwen/qwen3.6-35b-a3b, google/gemma-4-12b-qat, google/gemma-4-e4b
Writer model: qwen/qwen3.5-9b
Embedding model: text-embedding-nomic-embed-text-v1.5
Requested TotalPosts: 8
Requested Days: 3,6,10,13
Generated Days: 3,6,13
Missing Expected Days: 10
Per-profile results:
- hardening-test-8c-day3: day=3, requested=2, generated=2, success=True, attempts=4, failure=
- hardening-test-8c-day6: day=6, requested=2, generated=2, success=True, attempts=1, failure=
- hardening-test-8c-day10: day=10, requested=2, generated=0, success=False, attempts=4, failure=Latest failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-DAY10-112-20260723-183504-failed.txt
- hardening-test-8c-day13: day=13, requested=2, generated=2, success=True, attempts=1, failure=
Generated candidate files:
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day3-pilot-20260723-183409.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260723-183423.json
- C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260723-183526.json
Generated candidate count: 6
Generated IDs: DAY3-142, DAY3-143, DAY6-091, DAY6-092, DAY13-057, DAY13-058
Day distribution: 13=2, 3=2, 6=2
Action distribution: Approve=3, Remove=3
Validation passed: True
Blocking errors: 0
Warnings: 0
Policy-quality warnings: 0
Duplicate/near-duplicate notes: 3
Ready for Streamlit review: False
Failure message: [2026-07-23T18:33:29] Starting generation run.
[2026-07-23T18:33:30] Profile=hardening-test-8c-day3, batch=1, attempt=1 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 539
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\17 - Day 3-5 Escalation Production Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.

Day 3 should be simple but mixed across Approve, Remove and Escalate. Avoid craft/baking/gardening/kiln openings and obvious repeated credential-scam templates. Prefer everyday safe posts from book club, tech troubleshooting, sports training, lost property, pet care, workplace admin or harmless marketplace listing domains.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 3 posts...

Post 1/2: DAY3-142 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 2 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
    - Avoid overused hobby/craft/baking/gardening themes in nightly output.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Avoid repeated public notice, library, maintenance or festival templates.
  Attempt 3: defaults=5, repairs=0, fallbacks=0.
  Attempt 3: rejected with 3 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
    - Avoid overused hobby/craft/baking/gardening themes in nightly output.
    - Avoid repeated public notice, library, maintenance or festival templates.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-DAY3-142-20260723-183330-failed.txt
[2026-07-23T18:33:44] No valid candidate/validation pair was produced. Retrying with diversity hardening.
[2026-07-23T18:33:44] Profile=hardening-test-8c-day3, batch=1, attempt=2 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 539
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\17 - Day 3-5 Escalation Production Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.

Day 3 should be simple but mixed across Approve, Remove and Escalate. Avoid craft/baking/gardening/kiln openings and obvious repeated credential-scam templates. Prefer everyday safe posts from book club, tech troubleshooting, sports training, lost property, pet care, workplace admin or harmless marketplace listing domains.

NIGHTLY DIVERSITY RETRY: Avoid previous failed themes and avoid hobby/craft/baking/gardening/public-notice templates. Change scenario type, author voice, tone, text structure, metadata tuple and policy category where the blueprint allows it. Do not use 'Finally got', 'Finally finished', 'Just managed', 'Just wanted to', 'Honestly tired', pottery, kiln, sourdough, candles, vinyl, gardening, guitar achievement posts, PromoKing-style urgent deals, Bellmere bank/market freeze panic, generic evacuation hoaxes, obvious credential-verification scams, or raw JSON fragments inside visible post text. For Day 10 and Day 13, prefer specialist misinformation, metadata-aware ambiguity, Needs Review-acceptable cases and hard escalation boundaries over easy approve filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 3 posts...

Post 1/2: DAY3-142 | Approve | Lifestyle | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Post 2/2: DAY3-143 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 2 issue(s).
    - Visible post text should refer to 'the app' or 'the platform' rather than repeatedly naming a fictional platform.
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
  Attempt 2: defaults=5, repairs=2, fallbacks=0.
  Attempt 2: rejected with 2 issue(s).
    - Visible post text should refer to 'the app' or 'the platform' rather than repeatedly naming a fictional platform.
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
  Attempt 3: defaults=5, repairs=0, fallbacks=0.
  Attempt 3: rejected with 1 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-DAY3-143-20260723-183344-failed.txt
[2026-07-23T18:33:59] No valid candidate/validation pair was produced. Retrying with diversity hardening.
[2026-07-23T18:33:59] Profile=hardening-test-8c-day3, batch=1, attempt=3 of 4
Resuming checkpoint with 1/2 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 539
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\17 - Day 3-5 Escalation Production Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.

Day 3 should be simple but mixed across Approve, Remove and Escalate. Avoid craft/baking/gardening/kiln openings and obvious repeated credential-scam templates. Prefer everyday safe posts from book club, tech troubleshooting, sports training, lost property, pet care, workplace admin or harmless marketplace listing domains.

NIGHTLY DIVERSITY RETRY: Avoid previous failed themes and avoid hobby/craft/baking/gardening/public-notice templates. Change scenario type, author voice, tone, text structure, metadata tuple and policy category where the blueprint allows it. Do not use 'Finally got', 'Finally finished', 'Just managed', 'Just wanted to', 'Honestly tired', pottery, kiln, sourdough, candles, vinyl, gardening, guitar achievement posts, PromoKing-style urgent deals, Bellmere bank/market freeze panic, generic evacuation hoaxes, obvious credential-verification scams, or raw JSON fragments inside visible post text. For Day 10 and Day 13, prefer specialist misinformation, metadata-aware ambiguity, Needs Review-acceptable cases and hard escalation boundaries over easy approve filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 3 posts...

Post 1/2: DAY3-142 already checkpointed; skipping.

Post 2/2: DAY3-143 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
  Attempt 3: defaults=5, repairs=0, fallbacks=0.
  Attempt 3: rejected with 1 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-DAY3-143-20260723-183359-failed.txt
[2026-07-23T18:34:08] No valid candidate/validation pair was produced. Retrying with diversity hardening.
[2026-07-23T18:34:08] Profile=hardening-test-8c-day3, batch=1, attempt=4 of 4
Resuming checkpoint with 1/2 posts.
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 539
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\17 - Day 3-5 Escalation Production Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.

Day 3 should be simple but mixed across Approve, Remove and Escalate. Avoid craft/baking/gardening/kiln openings and obvious repeated credential-scam templates. Prefer everyday safe posts from book club, tech troubleshooting, sports training, lost property, pet care, workplace admin or harmless marketplace listing domains.

NIGHTLY DIVERSITY RETRY: Avoid previous failed themes and avoid hobby/craft/baking/gardening/public-notice templates. Change scenario type, author voice, tone, text structure, metadata tuple and policy category where the blueprint allows it. Do not use 'Finally got', 'Finally finished', 'Just managed', 'Just wanted to', 'Honestly tired', pottery, kiln, sourdough, candles, vinyl, gardening, guitar achievement posts, PromoKing-style urgent deals, Bellmere bank/market freeze panic, generic evacuation hoaxes, obvious credential-verification scams, or raw JSON fragments inside visible post text. For Day 10 and Day 13, prefer specialist misinformation, metadata-aware ambiguity, Needs Review-acceptable cases and hard escalation boundaries over easy approve filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 3 posts...

Post 1/2: DAY3-142 already checkpointed; skipping.

Post 2/2: DAY3-143 | Approve | Normal | Medium
  Attempt 1: defaults=5, repairs=2, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
  Attempt 3: defaults=5, repairs=0, fallbacks=0.
  Attempt 3: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day3-pilot-20260723-183409.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-pilot-20260723-183409-validation.txt
Elapsed: 0.2 minutes
The master input/posts.json was not modified.
[2026-07-23T18:34:23] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260723-183329-hardening-test-8c-day3-batch1-complete
[2026-07-23T18:34:23] Profile=hardening-test-8c-day3, batch=1 completed.
[2026-07-23T18:34:23] Profile=hardening-test-8c-day6, batch=1, attempt=1 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 541
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\20 - Day 6-9 Metadata Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.

Day 6 must make account metadata materially affect the decision in at least some posts. Use account age, previous flags, verification status, post volume, platform, location, bio, repeat behaviour or mismatch between claimed identity and metadata; do not merely attach metadata to otherwise normal posts.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 6 posts...

Post 1/2: DAY6-091 | Approve | Normal | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Avoid overused hobby/craft/baking/gardening themes in nightly output.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Post 2/2: DAY6-092 | Remove | Spam | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260723-183423.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260723-183423-validation.txt
Elapsed: 0.3 minutes
The master input/posts.json was not modified.
[2026-07-23T18:34:39] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260723-183329-hardening-test-8c-day6-batch1-complete
[2026-07-23T18:34:39] Profile=hardening-test-8c-day6, batch=1 completed.
[2026-07-23T18:34:39] Profile=hardening-test-8c-day10, batch=1, attempt=1 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 543
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.

Day 10 must include specialist misinformation but should rotate away from Bellmere bank freeze, savings withdrawal panic, and generic evacuation hoaxes. Prefer health, financial, public-safety, civic or manipulated-media boundaries with plausible ambiguity and avoid easy Approve/Lifestyle filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 10 posts...

Post 1/2: DAY10-112 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-DAY10-112-20260723-183440-failed.txt
[2026-07-23T18:34:52] No valid candidate/validation pair was produced. Retrying with diversity hardening.
[2026-07-23T18:34:52] Profile=hardening-test-8c-day10, batch=1, attempt=2 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 543
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.

Day 10 must include specialist misinformation but should rotate away from Bellmere bank freeze, savings withdrawal panic, and generic evacuation hoaxes. Prefer health, financial, public-safety, civic or manipulated-media boundaries with plausible ambiguity and avoid easy Approve/Lifestyle filler.

NIGHTLY DIVERSITY RETRY: Avoid previous failed themes and avoid hobby/craft/baking/gardening/public-notice templates. Change scenario type, author voice, tone, text structure, metadata tuple and policy category where the blueprint allows it. Do not use 'Finally got', 'Finally finished', 'Just managed', 'Just wanted to', 'Honestly tired', pottery, kiln, sourdough, candles, vinyl, gardening, guitar achievement posts, PromoKing-style urgent deals, Bellmere bank/market freeze panic, generic evacuation hoaxes, obvious credential-verification scams, or raw JSON fragments inside visible post text. For Day 10 and Day 13, prefer specialist misinformation, metadata-aware ambiguity, Needs Review-acceptable cases and hard escalation boundaries over easy approve filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 10 posts...

Post 1/2: DAY10-112 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-DAY10-112-20260723-183452-failed.txt
[2026-07-23T18:35:04] No valid candidate/validation pair was produced. Retrying with diversity hardening.
[2026-07-23T18:35:04] Profile=hardening-test-8c-day10, batch=1, attempt=3 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 543
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.

Day 10 must include specialist misinformation but should rotate away from Bellmere bank freeze, savings withdrawal panic, and generic evacuation hoaxes. Prefer health, financial, public-safety, civic or manipulated-media boundaries with plausible ambiguity and avoid easy Approve/Lifestyle filler.

NIGHTLY DIVERSITY RETRY: Avoid previous failed themes and avoid hobby/craft/baking/gardening/public-notice templates. Change scenario type, author voice, tone, text structure, metadata tuple and policy category where the blueprint allows it. Do not use 'Finally got', 'Finally finished', 'Just managed', 'Just wanted to', 'Honestly tired', pottery, kiln, sourdough, candles, vinyl, gardening, guitar achievement posts, PromoKing-style urgent deals, Bellmere bank/market freeze panic, generic evacuation hoaxes, obvious credential-verification scams, or raw JSON fragments inside visible post text. For Day 10 and Day 13, prefer specialist misinformation, metadata-aware ambiguity, Needs Review-acceptable cases and hard escalation boundaries over easy approve filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 10 posts...

Post 1/2: DAY10-112 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=1, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 3 issue(s).
    - Visible post text should refer to 'the app' or 'the platform' rather than repeatedly naming a fictional platform.
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-DAY10-112-20260723-183504-failed.txt
[2026-07-23T18:35:14] No valid candidate/validation pair was produced. Retrying with diversity hardening.
[2026-07-23T18:35:14] Profile=hardening-test-8c-day10, batch=1, attempt=4 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 543
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\21 - Day 10-12 Specialist Misinformation Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.

Day 10 must include specialist misinformation but should rotate away from Bellmere bank freeze, savings withdrawal panic, and generic evacuation hoaxes. Prefer health, financial, public-safety, civic or manipulated-media boundaries with plausible ambiguity and avoid easy Approve/Lifestyle filler.

NIGHTLY DIVERSITY RETRY: Avoid previous failed themes and avoid hobby/craft/baking/gardening/public-notice templates. Change scenario type, author voice, tone, text structure, metadata tuple and policy category where the blueprint allows it. Do not use 'Finally got', 'Finally finished', 'Just managed', 'Just wanted to', 'Honestly tired', pottery, kiln, sourdough, candles, vinyl, gardening, guitar achievement posts, PromoKing-style urgent deals, Bellmere bank/market freeze panic, generic evacuation hoaxes, obvious credential-verification scams, or raw JSON fragments inside visible post text. For Day 10 and Day 13, prefer specialist misinformation, metadata-aware ambiguity, Needs Review-acceptable cases and hard escalation boundaries over easy approve filler.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 10 posts...

Post 1/2: DAY10-112 | Remove | Fraud | Easy
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 2 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: rejected with 3 issue(s).
    - Visible post text should refer to 'the app' or 'the platform' rather than repeatedly naming a fictional platform.
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.
    - Likely credential/payment/private-data scam should be Escalate / FraudScam once reasons are unlocked.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: rejected with 1 issue(s).
    - Avoid repeated obvious credential-scam wording; use a fresher fraud or social-engineering pattern.

Stopped. Accepted posts remain checkpointed. See:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-DAY10-112-20260723-183514-failed.txt
[2026-07-23T18:35:26] Profile=hardening-test-8c-day10, batch=1 failed after 4 attempt(s).
[2026-07-23T18:35:26] Profile=hardening-test-8c-day13, batch=1, attempt=1 of 4
Workspace: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator
Runtime reference characters: 7,799
Existing dataset: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\input\posts.json
Generated history posts: 543
Schema: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\06 - post-schema.json
Blueprint: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\reference\22 - Day 13 Plus Hard Cases Blueprint.json
Chat model: qwen/qwen3.5-9b
Chat API: LM Studio native /api/v1/chat
Reasoning mode: off
Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.

Day 13 must avoid simple gaming achievements, pure hobby posts, and obvious urgent promo spam as main cases. Prefer hard harassment boundaries, fraud vs privacy overlaps, misinformation vs public-safety overlaps, Needs Review-acceptable ambiguity, metadata-relevant repeat offender cases, specialist misinformation ambiguity, and non-obvious escalation boundaries.
Embedding model: text-embedding-nomic-embed-text-v1.5
Generating 2 diverse Day 13 posts...

Post 1/2: DAY13-057 | Remove | Harassment | Hard
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
  Attempt 2: defaults=5, repairs=0, fallbacks=0.
  Attempt 2: rejected with 1 issue(s).
    - Visible post text should refer to 'the app' or 'the platform' rather than repeatedly naming a fictional platform.
  Attempt 3: defaults=5, repairs=1, fallbacks=0.
  Attempt 3: accepted and checkpointed.

Post 2/2: DAY13-058 | Remove | Misinformation | Hard
  Attempt 1: defaults=5, repairs=0, fallbacks=0.
  Attempt 1: rejected with 1 issue(s).
    - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
  Attempt 2: defaults=5, repairs=1, fallbacks=0.
  Attempt 2: accepted and checkpointed.

Running semantic duplicate detection...

Validation passed.
Candidate:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260723-183526.json
Report:
  C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260723-183526-validation.txt
Elapsed: 0.4 minutes
The master input/posts.json was not modified.
[2026-07-23T18:35:52] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260723-183329-hardening-test-8c-day13-batch1-complete
[2026-07-23T18:35:52] Profile=hardening-test-8c-day13, batch=1 completed.
[2026-07-23T18:35:52] Restored original config.json.
Status: completed_with_failures
Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-summary.txt
Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-manifest.json
Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-run.log
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
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-run.log
- 
- Profile: hardening-test-8c-day3 | Batch: 1 | Success: True | Attempts: 4 | Requested: 2 | Generated: 2 | Target day: 3
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day3-pilot-20260723-183409.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-pilot-20260723-183409-validation.txt
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day3-DAY3-143-20260723-183359-failed.txt
- Error: 
- 
- Profile: hardening-test-8c-day6 | Batch: 1 | Success: True | Attempts: 1 | Requested: 2 | Generated: 2 | Target day: 6
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day6-pilot-20260723-183423.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day6-pilot-20260723-183423-validation.txt
- Failure report: 
- Error: 
- 
- Profile: hardening-test-8c-day10 | Batch: 1 | Success: False | Attempts: 4 | Requested: 2 | Generated: 0 | Target day: 10
- Candidate: 
- Validation: 
- Failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-DAY10-112-20260723-183514-failed.txt
- Error: Latest failure report: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day10-DAY10-112-20260723-183504-failed.txt
- 
- Profile: hardening-test-8c-day13 | Batch: 1 | Success: True | Attempts: 1 | Requested: 2 | Generated: 2 | Target day: 13
- Candidate: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260723-183526.json
- Validation: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260723-183526-validation.txt
- Failure report: 
- Error: 
- 

Wrapper stdout tail:
- Reasoning mode: off
- Writer prompt suffix: Nightly generation should prioritise varied, review-worthy candidates over safe filler. Keep the requested policy outcome from each selected blueprint slot, but vary topic, voice, account context and structure aggressively. Safe posts may use book club logistics, harmless tech troubleshooting, sports training updates, volunteering rotas, school club notices, lost property, house move/admin, pet care, TV/film discussion, workplace admin, or marketplace listings without fraud. Remove posts should vary beyond obvious spam/phishing and may use repeated nuisance promotion, non-credible giveaway spam, low-level abusive insults without protected targeting, spammy engagement bait, non-dangerous false rumours that should be removed, or platform-rule violating self-promo. Escalate posts should vary across subtle social-engineering scams, privacy-sensitive info leaks, targeted harassment with context, public-safety misinformation, health misinformation, financial misinformation that is not a bank freeze, and ambiguous Needs Review-acceptable cases.
- 
- Day 13 must avoid simple gaming achievements, pure hobby posts, and obvious urgent promo spam as main cases. Prefer hard harassment boundaries, fraud vs privacy overlaps, misinformation vs public-safety overlaps, Needs Review-acceptable ambiguity, metadata-relevant repeat offender cases, specialist misinformation ambiguity, and non-obvious escalation boundaries.
- Embedding model: text-embedding-nomic-embed-text-v1.5
- Generating 2 diverse Day 13 posts...
- 
- Post 1/2: DAY13-057 | Remove | Harassment | Hard
-   Attempt 1: defaults=5, repairs=0, fallbacks=0.
-   Attempt 1: rejected with 1 issue(s).
-     - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
-   Attempt 2: defaults=5, repairs=0, fallbacks=0.
-   Attempt 2: rejected with 1 issue(s).
-     - Visible post text should refer to 'the app' or 'the platform' rather than repeatedly naming a fictional platform.
-   Attempt 3: defaults=5, repairs=1, fallbacks=0.
-   Attempt 3: accepted and checkpointed.
- 
- Post 2/2: DAY13-058 | Remove | Misinformation | Hard
-   Attempt 1: defaults=5, repairs=0, fallbacks=0.
-   Attempt 1: rejected with 1 issue(s).
-     - Avoid repeated low-diversity openings such as 'Finally finished...' or hobby-completion templates.
-   Attempt 2: defaults=5, repairs=1, fallbacks=0.
-   Attempt 2: accepted and checkpointed.
- 
- Running semantic duplicate detection...
- 
- Validation passed.
- Candidate:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\candidates\day13-pilot-20260723-183526.json
- Report:
-   C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\reports\day13-pilot-20260723-183526-validation.txt
- Elapsed: 0.4 minutes
- The master input/posts.json was not modified.
- [2026-07-23T18:35:52] Archived checkpoints to C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\checkpoint-archive\20260723-183329-hardening-test-8c-day13-batch1-complete
- [2026-07-23T18:35:52] Profile=hardening-test-8c-day13, batch=1 completed.
- [2026-07-23T18:35:52] Restored original config.json.
- Status: completed_with_failures
- Summary: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-summary.txt
- Manifest: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-manifest.json
- Run log: C:\Users\jackb\Documents\Game Dev\ModeratorPOC\Content_Generator\output\automation-logs\generation-20260723-183329-run.log

Wrapper stderr tail:
Confirmation: no candidates were approved automatically.
Confirmation: nothing was published to Unity.
Confirmation: Unity StreamingAssets and Assets/Resources/posts.json were not touched by this script.

Open local review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review.ps1

Open LAN review dashboard:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_review_lan.ps1

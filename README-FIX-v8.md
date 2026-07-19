# Content Generator v8 — diversity and semantic quality

This version adds:

- a fixed Day 1 category/action/difficulty blueprint;
- distinct scenario briefs for every slot;
- output-history checks, so previous candidate batches are not repeated;
- semantic duplicate detection through LM Studio's `/v1/embeddings` endpoint;
- automatic Nomic embedding-model discovery;
- checkpointing after every accepted post;
- resume support after a generation or semantic-quality failure;
- separate reporting for actual repairs, content fallbacks, and harmless schema defaults;
- elapsed-time reporting.

## Install

Extract into the root of the existing `Content_Generator` folder and replace:

- `scripts\generate_posts.py`
- `config.json`

Add:

- `reference\12 - Day 1 Generation Blueprint.json`

Keep Gemma and Nomic Embed Text v1.5 available in LM Studio, start the local server, then run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\run_generator.ps1
```

No new Python packages are required.

If a later post fails, accepted posts remain in `output\checkpoints` and the next run resumes them. If semantic duplicate detection rejects a post, only that slot is removed from the checkpoint and regenerated on the next run.

# Content Generator Fix v10 — Qwen3.6 27B

This version changes the routine writer model to Qwen3.6 27B and disables
thinking through the model's supported API parameter.

## Why this differs from v9

Qwen3.6 does not officially use the older `/no_think` prompt switch. The
generator now sends:

```json
"chat_template_kwargs": {
  "enable_thinking": false
}
```

It also uses Qwen's recommended non-thinking sampling profile:

- temperature: 0.7
- top_p: 0.8
- top_k: 20
- presence_penalty: 1.5

## Install

Extract into the existing `Content_Generator` folder and replace:

- `config.json`
- `scripts\generate_posts.py`

Keep the existing reference files, inputs, outputs, checkpoints, embedding
cache, and blueprint.

## LM Studio

Download and load:

```text
qwen/qwen3.6-27b
```

Use the Q4_K_M GGUF revision for the first test. Keep the Nomic embedding model
available.

Because the Q4 model is close to 16 GB, a 16 GB graphics card may need partial
CPU/system-RAM offload. Use a modest context window such as 8,192 for this
generator.

Then run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\run_generator.ps1
```

The existing compatible checkpoint should resume rather than regenerate
already accepted posts.

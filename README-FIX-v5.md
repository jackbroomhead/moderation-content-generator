# Content Generator Fix v5

The uploaded LM Studio responses show the model is reaching its 8,192-token
context limit. The full policy pack plus examples consumed about 7,100–7,300
prompt tokens, leaving too little room for reasoning and the final JSON.

This patch:

- replaces the full per-request policy injection with a compact runtime rules file;
- reduces examples from eight to two;
- reduces the example fields to text, category, and action;
- keeps the full JSON Schema validation;
- keeps JSON syntax repair and safe metadata flattening;
- keeps all existing duplicate, day, action, category, and policy checks;
- prints the runtime reference character count at startup.

## Install

Extract into the root of the existing `Content_Generator` workspace and replace:

- `scripts\generate_posts.py`
- `config.json`

Add:

- `reference\11 - Runtime Generation Rules.md`
- `install_v5.ps1`

Then run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install_v5.ps1
.\run_generator.ps1
```

The longer files in `reference` remain in place for humans and future tooling;
the generator simply stops sending all of them on every single-post request.

# Content Generator Fix v6

This patch fixes a remaining schema mismatch where Gemma emits:

```json
"previousFlags": []
```

The current post schema allows `previousFlags` to be a string or integer, not
an array.

The generator now safely converts:

- `[]` to `""`
- a non-empty array to its item count

It also tells the model explicitly that `previousFlags` must never be an array.

## Install

Replace only:

```text
scripts\generate_posts.py
```

Then run:

```powershell
.\run_generator.ps1
```

No dependency installation or setup step is required.

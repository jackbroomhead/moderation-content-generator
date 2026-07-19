# Content Generator Fix v7

This is the structural fix for repeated missing-field failures.

The local model now generates only the content-bearing fields:

- id
- author
- text
- category
- correctAction
- difficulty
- explanation
- day
- correctEscalationReason
- acceptableEscalationReasons
- allowNeedsReviewEscalation

The Python generator then adds the remaining required game metadata fields
using safe defaults and validates the expanded post against the complete
authoritative schema.

If Gemma still omits:

- `author`: the script creates a deterministic fictional username from the ID.
- `explanation`: the script creates a deterministic policy explanation from
  the already-generated action, category, and escalation reason.

This avoids spending retries on presentation metadata while preserving strict
validation of the actual moderation decision and post content.

## Install

Replace only:

```text
scripts\generate_posts.py
```

Then run:

```powershell
.\run_generator.ps1
```

No setup or dependency installation is required.

# Multi-Day Filler Scheduling

## Why generation currently says Day 1

The first generator blueprint intentionally targets Day 1. It was a controlled
pilot used to prove model calling, schema validation, checkpointing, semantic
duplicate detection, and human review.

The generator itself is not limited to Day 1. It reads:

- `target_day` from `config.json`
- `blueprint_file` from `config.json`
- the matching blueprint's `day` and `slots`

A new day therefore needs a deliberate blueprint and matching configuration.

## Meaning of `day`

For filler posts, `day` means the earliest day on which the post is eligible to
appear. It does not force the post to appear on that exact day.

For story posts, the authored story schedule remains fixed and separate from
the random filler pool.

## Runtime selection rule

A filler post is eligible when all of the following are true:

```text
post.day <= currentDay
post is not a fixed story post
post has not already appeared in this playthrough
post.category is currently unlocked
post.difficulty is allowed for the current day
```

The game then selects randomly from the eligible pool using difficulty weights.

## Proposed difficulty progression

This should be tuned during playtesting:

| Game day | Suggested filler weighting |
|---|---|
| 1 | 80% Easy, 20% Medium |
| 2 | 65% Easy, 35% Medium |
| 3–4 | 40% Easy, 55% Medium, 5% Hard |
| 5–6 | 20% Easy, 65% Medium, 15% Hard |
| 7+ | 10% Easy, 60% Medium, 30% Hard |

Easy posts should still appear later so the queue does not feel artificially
uniform.

## Blueprint progression

Do not create every later-day blueprint by copying Day 1. Each blueprint should
reflect which mechanics and categories the player has learned.

Recommended next sequence:

1. Keep the two reviewed Day 1 batches as the initial filler library.
2. Confirm the game's exact category and escalation unlock schedule.
3. Create a Day 2 blueprint with new scenarios and mostly Easy content.
4. Create Day 3+ blueprints only when the corresponding escalation mechanics
   and tutorial content are confirmed.
5. Generate, review, and approve each day independently.
6. Later, support mixed-day bulk jobs through Hermes rather than one enormous
   generation request.

## Story posts

Story posts should carry an explicit marker before random filler integration,
for example:

```json
{
  "isStoryPost": true
}
```

Filler posts should use:

```json
{
  "isStoryPost": false,
  "selectionWeight": 1.0
}
```

These fields are recommended for the future Unity migration but should not be
added to the authoritative schema until the current game data and loader have
been inspected.

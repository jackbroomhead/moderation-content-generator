# v4 cleanup and freeze report

## Completed

- Normalised **121 manually reviewed posts** from five approved source files.
- Preserved the source approved files without modifying them.
- Converted metadata strings back to integers and booleans.
- Cleared stale escalation and specialist fields after action changes.
- Replaced residual real-world locations with the controlled fictional setting.
- Removed platform names and location names from unsafe usernames.
- Rebalanced platform metadata so no platform exceeds three appearances in a 25-post chunk.
- Reduced the cleaned library to **one cancer-related item** across 121 posts.
- Produced a validation report with **zero blocking errors**.

## Important historical-pool note

The existing reviewed Day 10 source was deliberately generated as a specialist-misinformation test, so its historical contents remain specialist-heavy. The v4 generator does not repeat that structure: every new 25-post profile targets 14 Approve, 6 Remove and 5 Escalate posts, with no more than four misinformation posts and only one rotating specialist escalation.

The Unity/runtime selector must apply `config/content_selection_v4.json` so the historical specialist test posts cannot dominate a normal feed.

## Smoke-test expectation

The five-post prefix is:

1. Approve
2. Approve
3. Approve
4. Remove
5. Escalate

Run and review this five-post test before any new 25-post batch.

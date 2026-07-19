# v4.1 Username Hotfix

This hotfix fixes the production-test failure where the generator became stuck at DAY10-036 because early accepted posts used too many numeric username suffixes.

Changes:
- Keeps the hard check that the same numeric suffix must not recur in a batch.
- Removes the hard percentage cap for numeric suffix density, because early-batch ratios are noisy and can block even non-numeric replacement handles.
- Keeps prompt guidance to prefer natural word-based handles.

Install:
1. Close generation/review windows.
2. Copy the contents of this patch into the Content_Generator folder and overwrite files.
3. Re-run `generation_plan_production_test_v4.json`.

This does not modify config.json, output history, approved library files, or model settings.

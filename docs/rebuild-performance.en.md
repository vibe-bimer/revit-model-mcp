# Rebuild performance and cost

Measured on Revit 2020 with the 899 selectable components of `建筑结构.rvt`. The Chinese page next to this one
carries the full session record; this is the summary.

## What one copy costs

| Stage | Per copy | Note |
| --- | ---: | --- |
| Cross-document paste | ≈14 s | Revit's own cost for 899 components (≈15 ms each) |
| Save | ≈2.2 s | one backup kept |
| Clean-up between copies | ≈2 s | removes the previous copy so the next one lands in a fresh id block |
| **Total** | **≈18–19 s** | ten copies from one task: 165 s; thirty: about 8–9 minutes |

## How it got there

| Round | Change | Ten copies | Per copy |
| --- | --- | ---: | ---: |
| Start | every copy pasted twice (the retry check ran before the mapping existed) | 286 s | 28.6 s |
| ① | check the mapping before repeating a copy | 286 s | 28.6 s |
| ② | keep the pasted types, write one backup | 266 s | 26.6 s |
| ③ | repeat a refused copy first, isolate only as a last resort | **185 s** | **18.5 s** |

## Parallelism

Instances can run side by side (each takes its port and channel directory from `REVIT_MCP_HTTP_PORT`,
`REVIT_MCP_TOKEN` and `REVIT_MCP_CHANNEL_DIR`, and opens its own copy of the model so Revit does not ask about
an already open file). It only pays off when id ranges may overlap: reserving a block per instance means
burning ids at about 3 ms each, which measured slower than a serial batch (three instances, 21 copies: over
25 minutes, the third batch alone 10.7 minutes).

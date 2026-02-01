# siriusA-core

## Why this exists
Recent agent platforms (e.g., Moltbook/Moltbot) showed how easily irreversible mistakes happen.
This repo demonstrates a deterministic pre- and pre-execution gate that stops them.

**Stop scams twice**: block at the *entrance* (Pre-Guard) and right *before execution* (Tx-Guard), then **save the reason as a single artifact** (Chain).

- Verdict: **PASS / DELAY / BLOCK**
- Merge rule: **severity = max**, **evidence = union**
- Output: JSON artifacts (auditable, shareable)

---

## Quickstart (3 commands)

> Requires: Python 3.10+ (recommended)

### 0) (Optional) create venv & install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt 2>/dev/null || true


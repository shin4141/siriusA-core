# siriusA-core
Deterministic pre-execution safety gate (PASS/DELAY/BLOCK) + artifact schema. SiriusA core runtime.

## Quickstart
```bash
python cli.py examples/decision_request.json
```
Expected output: JSON artifact with severity PASS/DELAY/BLOCK.

PASS example: artifacts/demo_artifact_pass.json
DELAY example: artifacts/demo_artifact_delay.json

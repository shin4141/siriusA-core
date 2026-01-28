import json
import sys
from pathlib import Path

# add ./src to import path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from siriusa_core.pre_guard import run_pre_guard, pre_artifact_to_dict
from siriusa_core.gate import run_gate, artifact_to_dict

ORDER = {"PASS": 0, "DELAY": 1, "BLOCK": 2}


def max_severity(a: str, b: str) -> str:
    return a if ORDER[a] >= ORDER[b] else b


def main():
    if len(sys.argv) < 3:
        print("Usage: python chain_cli.py <pre_guard_json> <tx_guard_json>")
        sys.exit(2)

    pre_path = sys.argv[1]
    tx_path = sys.argv[2]

    with open(pre_path, "r", encoding="utf-8") as f:
        pre_req = json.load(f)
    with open(tx_path, "r", encoding="utf-8") as f:
        tx_req = json.load(f)

    pre_art = run_pre_guard(pre_req)
    tx_art = run_gate(tx_req)

    pre_d = pre_artifact_to_dict(pre_art)
    tx_d = artifact_to_dict(tx_art)

    severity = max_severity(pre_d["severity"], tx_d["severity"])

    # until: only meaningful for DELAY (from tx side)
    until = tx_d.get("until") if severity == "DELAY" else None

    evidence = []
    for e in pre_d.get("evidence", []):
        evidence.append(f"pre:{e}")
    for e in tx_d.get("evidence", []):
        evidence.append(f"tx:{e}")

    out = {
        "chain_id": f'{pre_d.get("decision_id","pre")}__{tx_d.get("decision_id","tx")}',
        "severity": severity,
        "until": until,
        "pre": pre_d,
        "tx": tx_d,
        "evidence": evidence,
        "explain": "Chain artifact: Pre-Guard + Tx-Guard canonicalized (severity=max, evidence=union).",
    }

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

import json
import sys
from pathlib import Path

# Ensure ./src is importable when running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from siriusa_core.gate import run_gate, artifact_to_dict


def main():
    import argparse, json, os, sys
    from src.siriusa_core.gate import run_gate, artifact_to_dict

    p = argparse.ArgumentParser()

    # Backward compatible:
    #   python cli.py <in>
    #   python cli.py <in> <out>
    p.add_argument("in_pos", nargs="?", default=None)
    p.add_argument("out_pos", nargs="?", default=None)

    # New style:
    #   python cli.py --in <in> --out <out>
    p.add_argument("--in", dest="in_flag", default=None)
    p.add_argument("--out", dest="out_flag", default=None)

    args = p.parse_args()

    in_path = args.in_flag or args.in_pos
    out_path = args.out_flag or args.out_pos

    if not in_path:
        p.error("input file required (positional <in> or --in <in>)")

    with open(in_path, "r", encoding="utf-8") as f:
        req = json.load(f)

    result = artifact_to_dict(run_gate(req))

    # If no out_path: stdout (CI-friendly)
    if not out_path:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

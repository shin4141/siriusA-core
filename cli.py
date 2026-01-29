import argparse
import json
import os
import sys

def _parse_args():
    # Backward compatible:
    #  A) python cli.py <in>
    #  B) python cli.py <in> <out>
    #  C) python cli.py --in <in> --out <out>
    if len(sys.argv) >= 2 and not sys.argv[1].startswith("--"):
        in_path = sys.argv[1]
        out_path = sys.argv[2] if len(sys.argv) >= 3 else None
        return argparse.Namespace(in_path=in_path, out_path=out_path)

    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", dest="out_path", required=False, default=None)
    return p.parse_args()

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




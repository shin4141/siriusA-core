import argparse
import json
import os
import sys

def _parse_args():
    # backward compatible:
    #   python pre_cli.py <in> <out>
    #   python pre_cli.py --in <in> --out <out>
    if len(sys.argv) >= 3 and not sys.argv[1].startswith("--"):
        return argparse.Namespace(in_path=sys.argv[1], out_path=sys.argv[2])

    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", dest="out_path", required=True)
    return p.parse_args()

def main():
    import argparse, json, os

    p = argparse.ArgumentParser()
    # Backward compatible:
    #   python pre_cli.py <in>
    #   python pre_cli.py <in> <out>
    p.add_argument("in_pos", nargs="?", default=None)
    p.add_argument("out_pos", nargs="?", default=None)

    # New style:
    #   python pre_cli.py --in <in> --out <out>
    p.add_argument("--in", dest="in_flag", default=None)
    p.add_argument("--out", dest="out_flag", default=None)

    args = p.parse_args()
    in_path = args.in_flag or args.in_pos
    out_path = args.out_flag or args.out_pos

    if not in_path:
        p.error("input file required (positional <in> or --in <in>)")

    with open(in_path, "r", encoding="utf-8") as f:
        req = json.load(f)

    from src.siriusa_core.pre_guard import run_pre_guard, pre_artifact_to_dict
    result = pre_artifact_to_dict(run_pre_guard(req))

    if not out_path:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()


import json
import sys
from siriusa_core.gate import run_gate, artifact_to_dict

def main():
  if len(sys.argv) < 2:
    print("Usage: python cli.py <path/to/decision_request.json>")
    sys.exit(2)

  path = sys.argv[1]
  req = json.loads(open(path, "r", encoding="utf-8").read())
  art = run_gate(req)
  print(json.dumps(artifact_to_dict(art), ensure_ascii=False, indent=2))

if __name__ == "__main__":
  main()

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Literal, Optional

Severity = Literal["PASS", "DELAY", "BLOCK"]


@dataclass
class Artifact:
    decision_id: str
    severity: Severity
    until: Optional[str]  # ISO8601
    evidence: List[str]
    explain: str


def run_gate(req: Dict[str, Any]) -> Artifact:
    decision_id = str(req.get("decision_id", "unknown"))
    irreversible = bool(req.get("irreversible", False))
    deadline_hours = int(req.get("deadline_hours", 0) or 0)
    stake = str(req.get("stake", "")).lower()

    # BLOCK first (must be above DELAY)
    if irreversible and stake == "high" and (0 < deadline_hours <= 6):
        return Artifact(
            decision_id=decision_id,
            severity="BLOCK",
            until=None,
            evidence=["rule:irreversible+stake=high+deadline<=6 => BLOCK"],
            explain="BLOCK: high-stake irreversible action under short deadline.",
        )

    # Then DELAY
    if irreversible and (0 < deadline_hours <= 48):
        until_dt = datetime.now(timezone.utc) + timedelta(hours=48)
        return Artifact(
            decision_id=decision_id,
            severity="DELAY",
            until=until_dt.isoformat(),
            evidence=["rule:irreversible+deadline<=48 => DELAY48h"],
            explain="DELAY is used to restore reversibility (Flip), not to deny execution.",
        )

    return Artifact(
        decision_id=decision_id,
        severity="PASS",
        until=None,
        evidence=["rule:default => PASS"],
        explain="PASS under minimal demo rules.",
    )

def artifact_to_dict(a: Artifact) -> Dict[str, Any]:
    return asdict(a)

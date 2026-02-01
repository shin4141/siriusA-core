from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Literal, Optional

Severity = Literal["PASS", "DELAY", "BLOCK"]


@dataclass
class PreArtifact:
    decision_id: str
    severity: Severity
    until: Optional[str]
    evidence: List[str]
    explain: str


def run_pre_guard(req: Dict[str, Any]) -> PreArtifact:
    decision_id = str(req.get("decision_id", "unknown"))
    source = str(req.get("source", "")).lower()
    link = str(req.get("link", "")).lower()
    urgency = str(req.get("urgency", "")).lower()
    text = str(req.get("text", "")).lower()

    # BLOCK first: credential/API-key request before execution
    if ("api key" in text) or ("apikey" in text) or ("token" in text) or ("secret" in text):
        return PreArtifact(
            decision_id=decision_id,
            severity="BLOCK",
            until=None,
            evidence=["rule:request_api_key => BLOCK"],
            explain="BLOCK: credential/API key request detected before execution.",
        )

    # BLOCK: obvious phishing pattern (minimal demo)
    if "airdrop" in link and source == "dm":
        return PreArtifact(
            decision_id=decision_id,
            severity="BLOCK",
            until=None,
            evidence=["rule:dm+airdrop_link => BLOCK"],
            explain="BLOCK: common phishing pattern detected (DM + airdrop link).",
        )

    # Then DELAY: urgency pressure
    if urgency in ("now", "urgent", "limited"):
        return PreArtifact(
            decision_id=decision_id,
            severity="DELAY",
            until=None,
            evidence=["rule:urgency_pressure => DELAY"],
            explain="DELAY: urgency pressure detected before execution.",
        )

    return PreArtifact(
        decision_id=decision_id,
        severity="PASS",
        until=None,
        evidence=["rule:default => PASS"],
        explain="PASS: no obvious pre-execution risk detected.",
    )

def pre_artifact_to_dict(a: PreArtifact) -> Dict[str, Any]:
    return asdict(a)

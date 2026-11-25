"""Pure synthetic evidence schema and fixed defensive catalog."""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ControlDefinition:
    control_id: str
    title: str
    criterion: str


CATALOG = (
    ControlDefinition("LAB-C001", "Backup restoration", "Synthetic restore exercise records a successful recovery."),
    ControlDefinition("LAB-C002", "Alert triage", "Synthetic alert record documents an assigned owner and disposition."),
    ControlDefinition("LAB-C003", "Patch review", "Synthetic patch review records an approved remediation decision."),
    ControlDefinition("LAB-C004", "Access review", "Synthetic review records approval of a fictional access policy."),
    ControlDefinition("LAB-C005", "Incident escalation", "Synthetic exercise records a documented escalation decision."),
)
_CONTROL_IDS = frozenset(c.control_id for c in CATALOG)
_STATUSES = frozenset(("met", "not_met", "inconclusive", "not_tested"))


@dataclass(frozen=True)
class ControlEvidence:
    control_id: str
    status: str
    evidence_id: str | None


def parse_evidence(raw: object) -> tuple[ControlEvidence, ...]:
    if (type(raw) is not dict
            or raw.keys() != {"schema_version", "source_kind", "controls"}
            or type(raw["schema_version"]) is not int
            or raw["schema_version"] != 1
            or type(raw["source_kind"]) is not str
            or raw["source_kind"] != "synthetic"
            or type(raw["controls"]) is not list
            or len(raw["controls"]) > len(CATALOG)):
        raise ValueError("invalid evidence")

    result = []
    seen = set()
    for record in raw["controls"]:
        if type(record) is not dict or record.keys() != {"control_id", "status", "evidence_id"}:
            raise ValueError("invalid evidence")
        control, status, evidence = record["control_id"], record["status"], record["evidence_id"]
        if (type(control) is not str or control not in _CONTROL_IDS or control in seen
                or type(status) is not str or status not in _STATUSES
                or (evidence is not None and
                    (type(evidence) is not str or re.fullmatch(r"LAB-E[0-9]{3}", evidence) is None))
                or (status in ("met", "not_met") and evidence is None)
                or (status == "not_tested" and evidence is not None)):
            raise ValueError("invalid evidence")
        seen.add(control)
        result.append(ControlEvidence(control, status, evidence))
    return tuple(result)


def summarize(controls: tuple[ControlEvidence, ...]) -> dict[str, int | float | None]:
    """Describe supplied validated outcomes; omitted controls are not evaluated."""
    counts = {status: 0 for status in ("met", "not_met", "inconclusive", "not_tested")}
    for control in controls:
        counts[control.status] += 1
    total = len(controls)
    evaluated = counts["met"] + counts["not_met"]
    return {
        "catalog_total": len(CATALOG),
        "total": total,
        "omitted": len(CATALOG) - total,
        **counts,
        "evaluated": evaluated,
        "evaluation_coverage_pct": round(100 * evaluated / total, 2) if total else None,
        "met_pct_of_evaluated": round(100 * counts["met"] / evaluated, 2) if evaluated else None,
    }

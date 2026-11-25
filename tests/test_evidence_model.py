import dataclasses
import unittest

from tools.evidence_model import CATALOG, ControlDefinition, ControlEvidence, parse_evidence, summarize


EXPECTED = (
    ("LAB-C001", "Backup restoration", "Synthetic restore exercise records a successful recovery."),
    ("LAB-C002", "Alert triage", "Synthetic alert record documents an assigned owner and disposition."),
    ("LAB-C003", "Patch review", "Synthetic patch review records an approved remediation decision."),
    ("LAB-C004", "Access review", "Synthetic review records approval of a fictional access policy."),
    ("LAB-C005", "Incident escalation", "Synthetic exercise records a documented escalation decision."),
)


def row(control="LAB-C001", status="met", evidence="LAB-E001"):
    return {"control_id": control, "status": status, "evidence_id": evidence}


def document(*rows):
    return {"schema_version": 1, "source_kind": "synthetic", "controls": list(rows)}


class TestEvidenceModel(unittest.TestCase):
    def test_catalog_contract(self):
        self.assertIsInstance(CATALOG, tuple)
        self.assertEqual(tuple(dataclasses.astuple(c) for c in CATALOG), EXPECTED)
        self.assertTrue(all(isinstance(c, ControlDefinition) for c in CATALOG))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            CATALOG[0].title = "changed"

    def test_valid_records(self):
        result = parse_evidence(document(row()))
        self.assertEqual(result, (ControlEvidence("LAB-C001", "met", "LAB-E001"),))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            result[0].status = "not_tested"

    def test_empty_allowed(self):
        self.assertEqual(parse_evidence(document()), ())

    def test_all_five_allowed(self):
        rows = [row(c[0]) for c in EXPECTED]
        self.assertEqual(len(parse_evidence(document(*rows))), 5)

    def test_invalid_records(self):
        good = document(row())
        bad = [
            None, [], 1, "PRIVATE_MARKER",
            {**good, "extra": "PRIVATE_MARKER"},
            {"schema_version": 1, "controls": []},
            {**good, "schema_version": True}, {**good, "schema_version": 1.0},
            {**good, "schema_version": 2}, {**good, "source_kind": "real"},
            {**good, "source_kind": []}, {**good, "controls": {}},
            document(*[row() for _ in range(6)]), document(row(), row()),
            document(None), document([]),
            document({"control_id": "LAB-C001", "status": "met"}),
            document({**row(), "extra": {}}),
            document(row("LAB-C006")), document(row("LAB-C000")),
            document(row("LAB-C００１")), document(row([])),
            document(row(status="unknown")), document(row(status=[])),
            document(row(evidence=None)), document(row(status="not_met", evidence=None)),
            document(row(status="not_tested")), document(row(evidence="LAB-E1000")),
            document(row(evidence="LAB-E１２３")), document(row(evidence=1)),
            document(row(evidence={"label": "LAB-E001"})),
            document(row(evidence="PRIVATE_MARKER")), document(row(evidence="LAB-E001\n")),
        ]
        for i, value in enumerate(bad):
            with self.subTest(case=i):
                with self.assertRaisesRegex(ValueError, "^invalid evidence$"):
                    parse_evidence(value)

    def test_evidence_id_rules(self):
        rows = [row(evidence="LAB-E000"), row("LAB-C002", "not_met", "LAB-E999"),
                row("LAB-C003", "inconclusive", None),
                row("LAB-C004", "inconclusive", "LAB-E000"),
                row("LAB-C005", "not_tested", None)]
        self.assertEqual(tuple(r.evidence_id for r in parse_evidence(document(*rows))),
                         ("LAB-E000", "LAB-E999", None, "LAB-E000", None))

    def test_mixed_summary(self):
        records = parse_evidence(document(
            row(), row("LAB-C002", "met", "LAB-E002"),
            row("LAB-C003", "not_met", "LAB-E003"),
            row("LAB-C004", "inconclusive", None),
            row("LAB-C005", "not_tested", None)))
        expected = {
            "catalog_total": 5, "total": 5, "omitted": 0,
            "met": 2, "not_met": 1, "inconclusive": 1, "not_tested": 1,
            "evaluated": 3, "evaluation_coverage_pct": 60.0,
            "met_pct_of_evaluated": 66.67,
        }
        actual = summarize(records)
        self.assertEqual(actual, expected)
        self.assertEqual(list(actual), list(expected))

    def test_empty_summary(self):
        self.assertEqual(summarize(()), {
            "catalog_total": 5, "total": 0, "omitted": 5,
            "met": 0, "not_met": 0, "inconclusive": 0, "not_tested": 0,
            "evaluated": 0, "evaluation_coverage_pct": None,
            "met_pct_of_evaluated": None,
        })

    def test_only_not_tested(self):
        self.assertEqual(summarize(parse_evidence(document(row(status="not_tested", evidence=None)))), {
            "catalog_total": 5, "total": 1, "omitted": 4,
            "met": 0, "not_met": 0, "inconclusive": 0, "not_tested": 1,
            "evaluated": 0, "evaluation_coverage_pct": 0.0,
            "met_pct_of_evaluated": None,
        })

    def test_subset_met(self):
        self.assertEqual(summarize(parse_evidence(document(row()))), {
            "catalog_total": 5, "total": 1, "omitted": 4,
            "met": 1, "not_met": 0, "inconclusive": 0, "not_tested": 0,
            "evaluated": 1, "evaluation_coverage_pct": 100.0,
            "met_pct_of_evaluated": 100.0,
        })

    def test_permutation(self):
        records = parse_evidence(document(row(), row("LAB-C002", "inconclusive", None)))
        self.assertEqual(summarize(records), summarize(tuple(reversed(records))))

"""Read bounded synthetic evidence and render deterministic offline reports."""
import argparse
import json
import os
import stat
import sys
from pathlib import Path

if __package__:
    from .evidence_model import CATALOG, ControlEvidence, parse_evidence, summarize
else:
    from evidence_model import CATALOG, ControlEvidence, parse_evidence, summarize


MAX_INPUT_BYTES = 1_048_576
_DEFINITIONS = {control.control_id: control for control in CATALOG}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("invalid evidence")
        result[key] = value
    return result


def _reject_constant(_):
    raise ValueError("invalid evidence")


def read_evidence(path: Path) -> tuple[ControlEvidence, ...]:
    """Read a regular file in a trusted local directory, then validate its JSON."""
    if not stat.S_ISREG(path.lstat().st_mode):
        raise OSError("input unavailable")
    with path.open("rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise OSError("input unavailable")
        raw = stream.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError("invalid evidence")
    try:
        document = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                              parse_constant=_reject_constant)
        return parse_evidence(document)
    except (ValueError, RecursionError):
        raise ValueError("invalid evidence") from None


def render_report(controls: tuple[ControlEvidence, ...], output_format: str) -> str:
    """Render validated records; no path access or artifact verification."""
    summary = summarize(controls)
    rows = []
    for record in sorted(controls, key=lambda control: control.control_id):
        definition = _DEFINITIONS[record.control_id]
        rows.append({
            "control_id": definition.control_id,
            "title": definition.title,
            "criterion": definition.criterion,
            "status": record.status,
            "evidence_id": record.evidence_id,
        })
    if output_format == "json":
        return json.dumps({
            "schema_version": 1,
            "catalog_version": 1,
            "source_kind": "synthetic",
            "summary": summary,
            "controls": rows,
        }, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if output_format != "markdown":
        raise ValueError("invalid format")
    lines = [
        "# Synthetic Defensive Evidence Report", "",
        "Synthetic data — not evidence of a real engagement",
        "Statuses are supplied; evidence IDs are labels, not verified artifacts.", "",
        "## Summary", "",
        "Coverage is calculated only over submitted controls; omitted catalog controls are not assessed.", "",
    ]
    for key, value in summary.items():
        if key in ("evaluation_coverage_pct", "met_pct_of_evaluated"):
            value = "N/A" if value is None else f"{value:.2f}%"
        lines.append(f"- {key}: {value}")
    lines += [
        "", "## Submitted controls", "",
        "| Control ID | Title | Criterion | Status | Evidence ID |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) if value is not None else "N/A"
                                       for value in row.values()) + " |")
    return "\n".join(lines) + "\n"


def write_report(path: Path, report: str) -> None:
    """Create a new output only; leave partial files for manual review."""
    data = report.encode("utf-8")
    with path.open("xb") as stream:
        if stream.write(data) != len(data):
            raise OSError("output unavailable")


class _ArgumentError(Exception):
    pass


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise _ArgumentError()


def _error(code: int, message: str) -> int:
    sys.stderr.write(f"Error: {message}\n")
    return code


def main(argv: list[str] | None = None) -> int:
    parser = _SafeArgumentParser(description="Render a synthetic defensive evidence report.",
                                 allow_abbrev=False)
    parser.add_argument("--file", required=True, type=Path, help="Synthetic JSON input")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--out", type=Path, help="New output file; never overwrite")
    try:
        args = parser.parse_args(argv)
    except _ArgumentError:
        return _error(2, "invalid arguments")
    except SystemExit as exc:
        return int(exc.code)
    try:
        controls = read_evidence(args.file)
    except OSError:
        return _error(1, "input unavailable")
    except ValueError:
        return _error(1, "invalid evidence")
    rendered = render_report(controls, args.format)
    if args.out is not None:
        try:
            write_report(args.out, rendered)
        except (OSError, ValueError):
            return _error(1, "output unavailable")
    else:
        sys.stdout.buffer.write(rendered.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

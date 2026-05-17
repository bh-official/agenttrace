"""agenttrace CLI — verify, report, export."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _color(text: str, code: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


def cmd_verify(args) -> int:
    from agenttrace.tracer import AgentTracer

    path = Path(args.bundle)
    if not path.exists():
        print(f"Error: {path} not found")
        return 2
    tracer = AgentTracer.__new__(AgentTracer)
    tracer._bundle_path = path
    valid, errors = tracer.verify(path)
    if valid:
        print(_color(f"\n  VALID — hash chain intact: {path}\n", "92"))
        return 0
    else:
        print(_color(f"\n  INVALID — tampering detected: {path}", "91"))
        for err in errors:
            print(f"  {err}")
        print()
        return 1


def cmd_report(args) -> int:
    from agenttrace.report import generate_report

    path = Path(args.bundle)
    if not path.exists():
        print(f"Error: {path} not found")
        return 2
    report = generate_report(path, verify_chain=not args.no_verify)
    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(report.to_text())
    return 0 if report.chain_valid else 1


def cmd_export(args) -> int:
    from agenttrace.report import generate_report

    path = Path(args.bundle)
    if not path.exists():
        print(f"Error: {path} not found")
        return 2
    report = generate_report(path)
    out = Path(args.out)
    out.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    print(f"\n  Exported: {out}\n")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(
        prog="agenttrace",
        description="EU AI Act Article 12 audit trail tool for AI agents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agenttrace verify bundle.jsonl
  agenttrace report bundle.jsonl
  agenttrace report bundle.jsonl --format json
  agenttrace export bundle.jsonl --out report.json
        """,
    )
    p.add_argument("--version", action="version", version="agenttrace 1.0.0")
    sub = p.add_subparsers(dest="command", required=True)

    p_verify = sub.add_parser("verify", help="Verify hash chain integrity of a bundle")
    p_verify.add_argument("bundle", help="Path to .jsonl bundle")
    p_verify.set_defaults(func=cmd_verify)

    p_report = sub.add_parser("report", help="Generate compliance report from a bundle")
    p_report.add_argument("bundle", help="Path to .jsonl bundle")
    p_report.add_argument("--format", choices=["text", "json"], default="text")
    p_report.add_argument("--no-verify", action="store_true", help="Skip hash chain verification")
    p_report.set_defaults(func=cmd_report)

    p_export = sub.add_parser("export", help="Export compliance report to JSON file")
    p_export.add_argument("bundle", help="Path to .jsonl bundle")
    p_export.add_argument("--out", default="agenttrace_report.json", help="Output file path")
    p_export.set_defaults(func=cmd_export)

    args = p.parse_args()
    result = args.func(args)
    sys.exit(result if isinstance(result, int) else 0)


if __name__ == "__main__":
    main()

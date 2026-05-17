"""
agenttrace
==========
EU AI Act Article 12 compliant audit trails for AI agents.
Hash-chained, tamper-evident decision logs.
Zero dependencies. Pure Python 3.10+.

Quick start:
    from agenttrace import AgentTracer

    tracer = AgentTracer(agent_id="my-agent", framework="langgraph")
    tracer.start_session()
    tracer.record_tool_call(tool="web_search", input_text="AI governance")
    tracer.record_decision(action="summarise", policy_decision="allow")
    path = tracer.end_session()

    # Verify integrity
    valid, errors = tracer.verify(path)

    # Generate compliance report
    from agenttrace import generate_report
    report = generate_report(path)
    print(report.to_text())

CLI:
    agenttrace verify bundle.jsonl
    agenttrace report bundle.jsonl
    agenttrace report bundle.jsonl --format json
    agenttrace export bundle.jsonl --out report.json
"""

from agenttrace.report import ComplianceReport, generate_report
from agenttrace.schema import (
    SCHEMA_VERSION,
    EventType,
    PolicyDecision,
    RiskTier,
    TraceEvent,
)
from agenttrace.tracer import AgentTracer, hash_text

__version__ = "1.0.0"
__author__ = "Linda Oraegbunam"
__all__ = [
    "AgentTracer",
    "TraceEvent",
    "EventType",
    "PolicyDecision",
    "RiskTier",
    "ComplianceReport",
    "generate_report",
    "hash_text",
    "SCHEMA_VERSION",
]

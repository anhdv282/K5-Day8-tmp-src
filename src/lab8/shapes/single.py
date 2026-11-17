"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

from typing import Any

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.mock_llm import complete
from lab8.runtime import ToolRejected, run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.tools import get_claim_view, tool_cost
from lab8.trace import Trace

SHAPE = "single"
MAX_STEPS = 8


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(conn, claim_id: str, *, seed: int, crash_at: str | None) -> RunResult:
    budget = Budget()
    trace = Trace(make_run_id(SHAPE, claim_id, seed))

    def done(status: str, amount: int, reason: str | None) -> RunResult:
        return finish(
            conn,
            shape=SHAPE,
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=amount,
            budget=budget,
            trace=trace,
            error_reason=reason,
        )

    budget.add_tool(tool_cost())
    claim = get_claim_view(conn, claim_id)
    if not claim["found"]:
        trace.add("error", {"reason": "unknown_claim"})
        return done("failed", 0, "unknown_claim")

    principal_id = claim["principal_id"]
    order_id = claim["order_id"]

    def decide(seen: dict[str, Any]) -> dict[str, Any]:
        # Mỗi bước ReAct = một lần gọi model (MockLLM) để cost so sánh được với swarm.
        # Prompt KHÔNG chứa ticket: model không có đường nào để tin số ngày trong ticket.
        last = seen.get("last_tool")
        complete(budget, seed=seed, purpose="react", prompt=f"step after={last}")
        trace.add("react_step", {"after": last})
        if last is None:
            if not order_id:
                return {"final": {"status": "needs_info", "amount": 0, "reason": "missing_order_id"}}
            return {"tool": "lookup_order", "args": {"order_id": order_id, "principal_id": principal_id}}
        if last == "lookup_order":
            view = seen["last_result"]
            trace.add("lookup_order", view)
            if not view.get("visible"):
                return {"final": {"status": "escalated", "amount": 0, "reason": view.get("reason")}}
            return {"tool": "lookup_refund_history", "args": {"order_id": order_id, "principal_id": principal_id}, "order": view["order"]}
        if last == "lookup_refund_history":
            trace.add("lookup_refund_history", seen["last_result"])
            return {"tool": "compute_compensation", "args": {"order": ctx["order"]}}
        if last == "compute_compensation":
            quote = seen["last_result"]
            trace.add("quote", quote)
            return {"final": {"status": "quoted", "amount": int(quote["amount_vnd"]), "reason": quote.get("reason")}}
        return {"final": {"status": "failed", "amount": 0, "reason": "unexpected_state"}}

    ctx: dict[str, Any] = {}

    def decide_with_ctx(seen: dict[str, Any]) -> dict[str, Any]:
        action = decide(seen)
        if "order" in action:
            ctx["order"] = action.pop("order")
        return action

    try:
        loop = run_react(
            conn,
            budget,
            observation={"claim": {"claim_id": claim_id, "order_id": order_id}},
            decide=decide_with_ctx,
            max_steps=MAX_STEPS,
            worker=False,
        )
    except ToolRejected as exc:
        trace.add("error", {"reason": "tool_rejected"})
        return done("failed", 0, f"tool_rejected:{exc}")

    final = loop["final"]
    trace.add("loop", {"stopped": loop["stopped"], "status": final.get("status")})
    if loop["stopped"] != "final":
        return done("failed", 0, final.get("error_reason", "step_cap"))

    status = final["status"]
    if status != "quoted":
        return done(status, 0, final.get("reason"))

    proposal = int(final["amount"])
    if proposal <= 0:
        return done("denied", 0, final.get("reason"))

    # Host là người ghi duy nhất. Truyền FULL quote, không tự trừ phần đã hoàn.
    try:
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise

    trace.add("issue_refund", {"ok": outcome["ok"], "reason": outcome["reason"], "conflict": outcome["conflict"]})
    if not outcome["ok"]:
        return done("failed" if outcome["conflict"] else "denied", proposal, outcome["reason"])
    complete(budget, seed=seed, purpose="draft", prompt=f"proposal={proposal}")
    return done("resolved", proposal, None)

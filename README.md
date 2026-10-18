# Steward Eval Kit — a reference x402 merchant for agent evals

**Drop this reference merchant into your agent eval, and your agents learn to
check trust and respect spend caps before paying.**

Most agent evals test paid calls against mocks or fake URLs
(`https://api.example.com/paid`). Mocks don't catch wire drift, quote-shape
changes, or an agent that pays without checking who it's paying and how much.
Steward is a live, stable, pay-per-call merchant on Base (x402 v1, USDC) —
built to be the merchant your eval runs against first.

## The drop-in harness

[`drop-in-harness/eval_steward_reference_merchant.py`](drop-in-harness/eval_steward_reference_merchant.py)
— one file, no signup, no API key:

- **Stage A (no spend, safe for CI):** performs the unpaid GET against
  `GET https://pay.brianbooms.com/api/v1/data/time?tz=UTC` and asserts the 402
  challenge shape: scheme `exact`, network Base, asset USDC, price exactly
  $0.01, and payTo is Steward's published wallet
  (`0xa98e8c6cbc64b7bb30fd0d2015ab24814c661839`). Stage A was verified live
  against the real endpoint on 2026-10-12.
- **Stage B (spends $0.01, OFF by default):** the full paid call —
  402 → pay → retry — asserting HTTP 200 and a settlement transaction. It only
  runs with `STEWARD_EVAL_PAID=1` and a funded wallet key.

```bash
python drop-in-harness/eval_steward_reference_merchant.py          # Stage A only
STEWARD_EVAL_PAID=1 EVM_PRIVATE_KEY=0x... \
  python drop-in-harness/eval_steward_reference_merchant.py        # + Stage B ($0.01)
```

The endpoint fixture is deterministic by design: local time for an IANA
timezone, computed from the tz database — no upstream to fail, no price flake
in CI (the harness also asserts the price has not risen above $0.01).

## What a passing eval proves about your agent

1. It reads a 402 challenge instead of treating it as an error.
2. It verifies the quote before paying — scheme, network, asset, payee, price.
3. It respects a hard spend cap (Steward MCP enforces
   `STEWARD_MAX_SPEND_USDC` $0.05/call and `STEWARD_MAX_SPEND_DAY_USDC`
   $5.00/day by default, refusing to sign above them).
4. It can find the settlement receipt afterwards.

## The merchant behind the fixture

Steward MCP (`@brianbooms/steward-mcp` v0.3.1, `npx -y @brianbooms/steward-mcp`)
exposes 25 tools — 14 paid ($0.01–$0.02, pay-per-call, settled via x402 at
call time) + 11 free discovery tools — and a 32-SKU catalog, so one merchant
covers data/API, developer-tool, trust-verification, and content eval
scenarios. Machine-readable discovery:
https://pay.brianbooms.com/.well-known/x402 and
https://brianbooms.com/.well-known/x402-service.json

## Docs in this repo

- [`integration-proposal.md`](integration-proposal.md) — why Steward fits as a
  canonical reference merchant, and what inclusion looks like per framework.
- [`framework-research-notes.md`](framework-research-notes.md) — dated
  research notes (2026-10-12) on the framework/eval surfaces surveyed.

## Links

- MCP server: https://github.com/brianbooms/steward-mcp
- All Steward examples: https://github.com/brianbooms/steward-examples
- Rail: https://pay.brianbooms.com · Terms: https://brianbooms.com/fair-dealing/

Built by Brian Booms, AI-assisted artist · Synthetic Universe LLC · MIT

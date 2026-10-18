# Integration Proposal — Steward as the Reference x402 Merchant
**2026-10-12 · Eval-default outreach kit**

## The ask, in one sentence

Add Brian Booms' Steward endpoints as the **canonical reference x402 merchant** inside the frameworks and eval harnesses agents are built on — so the first paid call any new agent ever makes, in a tutorial or an eval, is against his rail.

## Why his endpoints are the right reference merchant

| Property | His endpoints (verified 2026-10-12) | Why a maintainer wants it |
|---|---|---|
| Real mainnet | Live on Base (also Polygon/Arbitrum/Avalanche/Solana offers), USDC, facilitator `facilitator.xpay.sh` | Evals against mocks don't catch wire drift; a live merchant does |
| Stable, exact pricing | $0.01 flat for the whole data family (`maxAmountRequired: "10000"`), $0.02 morning-briefing bundle | Deterministic assertions — no price flake in CI |
| No signup / no API key | 402 challenge → pay → retry; nothing else | Zero maintainer setup burden; a reviewer can hand-run the eval in seconds |
| Deterministic, zero-upstream fixtures | `/api/v1/data/time?tz=UTC` is computed locally from the tz database (the challenge body itself says "no upstream to fail") | Evals that can't flake: time, id-generate, unit-convert never depend on a third party |
| Broad category coverage | 30+ live routes: time, weather, FX, ISS passes, readability, summarize, RSS feeds, DNS, TLS cert, Wikipedia, crypto, gas price, holidays, country, astronomy, sleep-tip, affirmation, fortune, quote, joke, plus music/audio + buy routes | One merchant covers data/API, dev-tool (dns/cert/httpcheck), and content categories — a single fixture for many eval scenarios |
| Merchant tooling already exists | Steward MCP server (`@brianbooms/steward-mcp` on npm, live 2026-10-06), x402 buyer libraries | Frameworks get the buyer side for free, not just the merchant |
| Machine-readable discovery | `https://pay.brianbooms.com/.well-known/x402` lists every resource, facilitator, payTo | A maintainer can script fixture generation from the manifest |

## What inclusion looks like, concretely, per target

1. **coinbase/agentkit** — A "merchant example" in the repo, following the precedent of issues #1359 (VeraData) and #1344 (Intelica): an issue + PR adding a Steward example under `typescript/examples/` or `python/examples/`. The example agent: "what time is it in Tokyo?" → custom LangChain tool → `requests.get("https://pay.brianbooms.com/api/v1/data/time?tz=Asia/Tokyo")` → AgentKit pays $0.01 automatically → agent reads `local_time`. Deliverable staged: the issue text + the example folder.
2. **openclaw/skills** — The official `x402-client` skill's quick-start points at `https://api.example.com/paid` — a fake. PR replaces it with the real $0.01 reference endpoint and adds a `--dry-run` → paid walkthrough. Every OpenClaw agent loading the skill then has a live merchant wired in. Deliverable staged: PR description + SKILL.md diff.
3. **elizaos/eliza `plugins/plugin-x402`** — Propose a gated (env-var) live-merchant integration test, with the drop-in harness as the starting point. Honest caveat: maintainers run mocked unit tests today; this is a proposal, not a guaranteed merge. Deliverable staged: proposal text + harness file.
4. **Ghost Protocol / GhostRank** — Propose his endpoints as the canonical default merchant for `GHOST_OPENCLAW_X402_URL` and the worked example in the `openclaw-ghost-pay` skill docs, so verified settlements flow to GhostRank against his rail. Deliverable staged: outreach text.
5. **x402-execution-lab** — Propose the endpoints as the canonical real-mainnet merchant fixtures for the `bench/` train/dev/eval splits. Deliverable staged: outreach text.

## Cost and risk

- **$0 unapproved spend.** All staged work is docs + code. The only money movement in the whole kit is Stage B of the harness ($0.01) and that is OFF by default — it needs Brian's explicit tap and a funded test wallet.
- **Safe/legal/ethical:** no outreach is sent; everything is drafts. No counsel-gated surface (no money transmission for third parties, no identity/KYC, no legal filings).
- **Risk to note:** maintainers may say no, especially ElizaOS (mocked-test norms) and OpenClaw (small team). The AgentKit merchant-example pattern is the highest-probability lane because two merchants already walked it.

## Why this is "never done before"

Nobody is deliberately seeding eval harnesses with their own merchant endpoints today. Merchants list on directories (x402scan, Bazaar) — that's discovery. This play is *defaults*: the endpoint a framework's docs point at, the fixture its tests run, the URL its skill examples show. When the default is his endpoint, every new agent's first paid touch is his revenue.

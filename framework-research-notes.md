# Eval-Default Outreach Kit — Framework Research Notes
**Researched 2026-10-12 · all projects verified real via web search/GitHub fetch (Oct 2026)**

Goal: get Brian Booms' x402 endpoints into agent framework benchmarks/evals as the **reference x402 merchant** — so every new agent running evals touches his endpoints before it ever shops.

Method honesty: searches were index-based (browser.search) plus page fetches of real GitHub repos/issues. No project below is invented. Where a fact wasn't verified (e.g., issue resolution state), it is marked `UNVERIFIED`.

---

## P0 — coinbase/agentkit (Coinbase Developer Platform team)

- **Repo:** https://github.com/coinbase/agentkit (Apache-2.0, 1,326 stars, main branch)
- **Maintainers (from CONTRIBUTING.md):** @John-peterson-coinbase, @stat, @rohan-agarwal-coinbase, @0xRAG, @yuga-cb, @CarsonRoscoe
- **Payments/eval surface:** AgentKit is THE agent-payment toolkit — wallet providers (CDP/Privy/viem) plus action providers for onchain work. Framework extensions: LangChain, Vercel AI SDK, MCP, AutoGen, OpenAI Agents SDK, Pydantic AI, Strands. Examples dirs: `typescript/examples/` and `python/examples/` (chatbot examples per framework).
- **Merchant-reference mechanism — VERIFIED REAL:** GitHub issues #1359 ("Add VeraData as x402 merchant example — LATAM sanctions screening and KYB", api.veradata.dev, $0.01–$0.15) and #1344 ("Add Intelica as x402 merchant example for competitive intelligence", api.intelica.dev, $0.05). Merchants self-nominate via issue using a working template: use case → code example (AgentKit handles 402, pays automatically) → "why it matters" → x402 compliance → pricing table → docs links. This is the proven contribution norm.
- **How inclusion happens:** 1) Open an issue in the VeraData/Intelica format. 2) Fork → branch → PR (commits must be signed per CONTRIBUTING.md; PR template; CI green; maintainers review ~1 day). Inclusion = a named merchant example that every AgentKit developer reads when learning agent payments.
- **Eval-default value:** HIGHEST. AgentKit examples are the tutorial every agent builder runs first. A Steward merchant example puts his $0.01 endpoints in front of every new Coinbase-stack agent.
- `UNVERIFIED:` whether #1359/#1344 were merged (issue bodies were read; comments/labels not fetched). The template norm itself is verified.

## P1 — elizaos/eliza → plugins/plugin-x402 (ElizaOS team)

- **Repo:** https://github.com/elizaOS/eliza (19,540 stars) · plugin at `plugins/plugin-x402`
- **Payments/eval surface:** Official x402 plugin with a REAL test suite: `plugins/plugin-x402/src/x402-replay-durable.test.ts` (19/19 green per PR #13300) and `packages/agent/src/api/x402-contract.test.ts` (14 vitest tests pinning the `X402PluginModule` contract). Tests are mocked unit tests — no live merchant fixtures.
- **Contribution norms:** PRs with vitest + biome checks, PR_EVIDENCE.md pattern (codex review, tsgo --noEmit). Third-party plugin submissions exist (e.g. security-gate-x402's ELIZAOS_PR_SUBMISSION_GUIDE.md) targeting the plugins directory.
- **Merchant-reference mechanism:** No established "merchant example" directory, but the plugin's integration/live-test layer is the natural home for a canonical paid merchant fixture. Honest caveat: maintainers may reject live-merchant fixtures in unit suites; the realistic ask is a `docs/` merchant example + a gated (env-var) live integration test.
- **Eval-default value:** HIGH. ElizaOS is the dominant open agent framework; its x402 plugin is what thousands of agent builders wire in. Brian already ships his own ElizaOS x402 plugin (`~/workspace/ops/x402/framework-plugins/elizaos`) — strong credibility for the pitch.
- `UNVERIFIED:` whether plugin-x402 maintainers accept live-merchant test fixtures (no such fixture exists in the repo today).

## P1 — openclaw/skills (OpenClaw, official skills registry)

- **Repo:** https://github.com/openclaw/skills (public; skill dirs under `skills/`)
- **Payments/eval surface:** Skills are markdown+YAML+helper scripts agents load at runtime. Relevant skills: `openclaw--skills--x402-client` ("x402 Client — Agent Payment Skill", by openclaw) — its Quick Start literally uses `https://api.example.com/paid` as the paid-API placeholder and `--dry-run` preview; and `skills/ghostprotoinfra/openclaw-ghost-pay` ("Execute a real x402 request against a merchant endpoint" + report verified settlements to GhostRank).
- **Merchant-reference mechanism:** The x402-client skill's docs/examples point at a fake URL today. A PR adding Brian's real $0.01 endpoint as the worked example (or as the `--url` default in helper scripts) makes his endpoint the one every OpenClaw agent's first x402 touch targets. Community skills also mirror via tomevault-io/skills-registry; ClawHub (`clawhub install <skill>`) is the distribution channel for new skills.
- **How inclusion happens:** PR to openclaw/skills following the skill schema (SKILL.md frontmatter: name, version, metadata), or publish a new skill via ClawHub. Community skills show real authorship + version fields.
- **Eval-default value:** HIGH. OpenClaw skills are the runtime discovery layer — agents load skills at task start; the example URL in the skill is what they call.
- `UNVERIFIED:` exact PR acceptance criteria for openclaw/skills (repo root page fetch failed; schema derived from mirrored skill files, which are real).

## P2 — Ghost Protocol / GhostRank (ghost-protocol-infrastructure)

- **Repo:** https://github.com/ghost-protocol-infrastructure/ghost_protocol · runtime: https://ghostprotocol.cc
- **Payments/eval surface:** `integrations/openclaw-ghost-pay` — a published skill with helper scripts: `get-payment-requirements.mjs`, `call-x402.mjs` (runs the real `402 → payment → retry` flow against any merchant endpoint), `report-x402-settlement.mjs` — "This is the step that makes successful x402 usage visible to GhostRank." Env var `GHOST_OPENCLAW_X402_URL` sets the default merchant endpoint URL.
- **Merchant-reference mechanism:** GhostRank is a verified-settlement reputation leaderboard for agents. Getting his endpoints adopted as the canonical/default merchant (`GHOST_OPENCLAW_X402_URL` default) or as a verified merchant in their docs means every agent running the Ghost flow pays him first.
- **How inclusion happens:** PR to the skill repo (update docs/defaults) or contact via their skill metadata homepage (`https://github.com/Ghost-Protocol-Infrastructure/GHOST_PROTOCOL/tree/main/integrations/openclaw-ghost-pay`).
- **Eval-default value:** MEDIUM-HIGH. Real but smaller community than AgentKit/ElizaOS; still a genuine "benchmark-like" settlement leaderboard.
- `UNVERIFIED:` ghostprotocol.cc's live leaderboard state (skill files verified real; site not fetched).

## P2 — x402-execution-lab (sunruize93-cmyk)

- **Repo:** https://github.com/sunruize93-cmyk/x402-execution-lab
- **Payments/eval surface:** Real eval harness: a `bench/` module ("Arena Execution Bench") — decision bench with 4 scenario families, 24 conditions across train/dev/eval splits, paired analysis, replayable traces; plus a Payment Lab with 20 scripted failure scenarios. Built for "x402 integrations, agents that purchase services or call paid tools, and controlled policy experiments."
- **Merchant-reference mechanism:** Propose his endpoints as the canonical real-mainnet merchant fixtures for the bench's live scenarios (stable pricing, no signup, sub-cent to cent pricing — ideal for repeatable evals).
- **How inclusion happens:** GitHub issue/PR to the maintainer.
- **Eval-default value:** MEDIUM. Genuine train/dev/eval structure, but a small/unknown-author repo — the play is "never-done-before positioning," not reach.
- `UNVERIFIED:` repo activity/star count not checked.

## Honest non-targets (checked and excluded)

- **x402-foundation/x402 `examples/`:** SDK buyer examples only (httpx/requests/Go/MCP clients). No merchant-reference slot. Not a target for merchant inclusion.
- **zombisploit/a2a-interop-test:** Ferminux-specific A2A/x402 test suite, not a general eval harness. Excluded.
- **LangGraph x402:** open proposal issue (langchain-ai/langgraph#8487) — no suite exists yet. Emerging, not actionable.
- **minia2a.uk:** a reference x402 marketplace (174 services) — real, but Brian PARKED the minia2a wallet-signature thread 2026-10-10. Excluded by standing decision.

---

## Standing directive fit

Brian's explicit directive: endpoints as infrastructure others copy — "eval/benchmark usage" is a standing item (MEMORY.md). AgentKit merchant examples + OpenClaw skill worked examples + GhostRank defaults + ElizaOS live fixtures + the execution-lab bench are five independent lanes into exactly that.

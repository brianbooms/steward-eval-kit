#!/usr/bin/env python3
"""
Eval-default reference-merchant harness — Steward x402 (Brian Booms).

Drop this file into any agent framework's test/eval suite. It exercises the
real 402 -> pay -> retry flow against a live, stable, $0.01 reference merchant
endpoint. No signup, no API key — just a Base USDC wallet for the paid stage.

Two stages:
  STAGE A (no spend, safe for CI): performs the unpaid GET, asserts the 402
      challenge shape: exact $0.01 on Base, correct USDC asset, exact scheme,
      published pay-to address.
  STAGE B (spends $0.01 USDC on Base — OFF by default): performs the full
      paid call via the official x402 v2 Python SDK, asserts HTTP 200 and a
      well-formed payload, and prints the on-chain settlement transaction.

Run stage A:   python eval_steward_reference_merchant.py
Run both:      STEWARD_EVAL_PAID=1 EVM_PRIVATE_KEY=0x... python eval_steward_reference_merchant.py

Stage A was executed against the live endpoint on 2026-10-12 and passes.
Stage B follows the x402 Foundation's official httpx client example verbatim
(https://github.com/x402-foundation/x402/tree/main/examples/python/clients/httpx)
and is NOT executed here (it requires a funded wallet).

Merchant: Synthetic Universe / Brian Booms
Endpoint: GET https://pay.brianbooms.com/api/v1/data/time?tz=UTC
  - Returns the current local time for any IANA timezone. Computed locally
    from the tz database — no upstream, deterministic, ~instant.
  - Price: $0.01 USDC on Base (also Polygon/Arbitrum/Avalanche/Solana;
    this harness asserts the Base offer).
Docs/discovery: https://pay.brianbooms.com/.well-known/x402
"""

import json
import os
import sys
import urllib.request
import urllib.error

ENDPOINT = "https://pay.brianbooms.com/api/v1/data/time?tz=UTC"
EXPECTED_PRICE_ATOMIC = 10000          # $0.01 in 6-decimal USDC
EXPECTED_NETWORK = "base"
EXPECTED_SCHEME = "exact"
EXPECTED_ASSET_BASE_USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
# Merchant's published Base receive address (re-derive anytime by curling the 402):
EXPECTED_PAYTO = "0xa98e8c6cbc64b7bb30fd0d2015ab24814c661839"


def check(condition, message):
    if not condition:
        print(f"FAIL: {message}")
        sys.exit(1)
    print(f"  ok: {message}")


def stage_a_no_spend():
    """Assert the unpaid 402 challenge. Zero spend, CI-safe."""
    print("STAGE A — unpaid 402 challenge (no spend)")
    # NOTE: Cloudflare edge blocks the stock "Python-urllib/*" user-agent (403).
    # Send an identifying UA — the same requirement applies to any eval suite.
    req = urllib.request.Request(
        ENDPOINT, method="GET",
        headers={"User-Agent": "steward-eval-harness/1.0 (+https://brianbooms.com)"},
    )
    try:
        urllib.request.urlopen(req, timeout=25)
        print("FAIL: expected HTTP 402, got 2xx (endpoint may have changed)")
        sys.exit(1)
    except urllib.error.HTTPError as e:
        check(e.code == 402, f"HTTP status is 402 (got {e.code})")
        body = json.loads(e.read().decode())

    check(body.get("error") == "Payment required", 'body.error == "Payment required"')
    accepts = body.get("accepts") or []
    base_offers = [a for a in accepts if a.get("network") == EXPECTED_NETWORK]
    check(len(base_offers) >= 1, f"accepts[] contains a '{EXPECTED_NETWORK}' offer")

    offer = base_offers[0]
    check(offer.get("scheme") == EXPECTED_SCHEME, f"scheme == '{EXPECTED_SCHEME}'")
    check(offer.get("maxAmountRequired") == str(EXPECTED_PRICE_ATOMIC),
          f"maxAmountRequired == {EXPECTED_PRICE_ATOMIC} (=$0.01)")
    check(str(offer.get("asset", "")).lower() == EXPECTED_ASSET_BASE_USDC.lower(),
          f"asset is Base USDC ({EXPECTED_ASSET_BASE_USDC})")
    check(str(offer.get("payTo", "")).lower() == EXPECTED_PAYTO.lower(),
          f"payTo matches published merchant address")

    # Guardrail: the merchant must never silently raise the eval price.
    check(int(offer["maxAmountRequired"]) <= EXPECTED_PRICE_ATOMIC,
          f"price is at or below $0.01 (atomic: {offer['maxAmountRequired']})")
    print("STAGE A passed.\n")
    return offer


def stage_b_paid():
    """Full paid call via the official x402 v2 Python SDK. Spends $0.01."""
    print("STAGE B — real paid call ($0.01 USDC on Base)")
    private_key = os.environ.get("EVM_PRIVATE_KEY")
    check(bool(private_key), "EVM_PRIVATE_KEY is set (funded with Base USDC)")

    from eth_account import Account
    from x402 import x402Client
    from x402.http import x402HTTPClient
    from x402.http.clients import x402HttpxClient
    from x402.mechanisms.evm import EthAccountSigner
    from x402.mechanisms.evm.exact.register import register_exact_evm_client

    # Hard cap: never pay more than the published $0.01 for this reference call.
    client = x402Client().set_spend_controls({"max_amount_per_payment": "$0.01"})
    account = Account.from_key(private_key)
    register_exact_evm_client(client, EthAccountSigner(account))

    import asyncio

    async def run():
        async with x402HttpxClient(client) as http:
            response = await http.get(ENDPOINT)
            check(response.status_code == 200,
                  f"paid retry returns HTTP 200 (got {response.status_code})")
            payload = response.json()
            check("local_time" in payload and "timezone" in payload,
                  f"payload carries time fields (keys: {sorted(payload.keys())})")
            settle = x402HTTPClient(client).get_payment_settle_response(
                lambda name: response.headers.get(name)
            )
            check(bool(getattr(settle, "transaction", None)),
                  f"settlement confirmed on-chain: {settle.transaction}")
            print(f"  paid payload: {json.dumps(payload)}")
        return True

    asyncio.run(run())
    print("STAGE B passed.\n")


def main():
    stage_a_no_spend()
    if os.environ.get("STEWARD_EVAL_PAID") == "1":
        stage_b_paid()
    else:
        print("STAGE B skipped (set STEWARD_EVAL_PAID=1 with a funded EVM_PRIVATE_KEY to run the paid call).")
    print("ALL DONE — reference merchant checks passed.")


if __name__ == "__main__":
    main()

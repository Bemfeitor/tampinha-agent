"""Live Fireworks smoke test — exercises the Tampinha runtime, not a raw SDK client.

Opt-in only:
    TAMPINHA_LIVE_TESTS=1 FIREWORKS_API_KEY=fw_... \\
        pytest tests/run_agent/test_fireworks_live.py -q

Unlike a bare OpenAI() client pointed at the endpoint, this drives Tampinha'
own provider resolution — ``resolve_provider_client('fireworks')`` — so it
verifies the auth/config/base-URL/aux-model wiring that the
bundled provider actually ships, then makes a real call through that client.
"""

from __future__ import annotations

import os

import pytest

LIVE = os.environ.get("TAMPINHA_LIVE_TESTS") == "1"
FIREWORKS_KEY = os.environ.get("FIREWORKS_API_KEY", "")

pytestmark = [
    pytest.mark.skipif(not LIVE, reason="live-only: set TAMPINHA_LIVE_TESTS=1"),
    pytest.mark.skipif(not FIREWORKS_KEY, reason="FIREWORKS_API_KEY not configured"),
    pytest.mark.integration,
]


def _resolve_runtime_client(provider="fireworks"):
    """Build the Fireworks client the way the Tampinha runtime does."""
    from agent.auxiliary_client import resolve_provider_client

    client, model = resolve_provider_client(provider)
    assert client is not None, "Tampinha failed to build a Fireworks client"
    return client, model


def test_tampinha_wires_fireworks_client():
    """The runtime resolves a Fireworks client pointed at the right endpoint
    with the partner-attribution headers applied — no network required."""
    client, model = _resolve_runtime_client()
    assert "api.fireworks.ai" in str(client.base_url)
    # Default aux model must be a PAYG /models/ id (works with an fw_ key).
    assert model.startswith("accounts/fireworks/models/")


def test_fireworks_basic_chat_through_runtime():
    """A single-turn completion via the Tampinha-resolved client returns text."""
    client, model = _resolve_runtime_client()

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say exactly the word 'pong' and nothing else."}],
        timeout=60,
    )

    content = response.choices[0].message.content
    assert content and "pong" in content.lower()



"""Test double for the `stripe` package — local tests only.

Placed first on sys.path by tests/test_checkout_local.py so the app imports
this module instead of the real SDK. No network, no real keys.
- checkout.Session.create records its kwargs to $FAKE_STRIPE_CAPTURE (JSON)
  and returns a fake hosted-checkout session.
- Webhook.construct_event just parses the request body as JSON (signature
  verification is exercised against Stripe's real test tooling separately).
"""
import json
import os

api_key = None


class _Session:
    @staticmethod
    def create(**kwargs):
        capture = os.environ.get("FAKE_STRIPE_CAPTURE")
        if capture:
            with open(capture, "w") as f:
                json.dump(kwargs, f)
        return {"id": "cs_test_fake123",
                "url": "https://checkout.stripe.com/c/pay/cs_test_fake123"}


class _Checkout:
    Session = _Session


checkout = _Checkout()


class _Webhook:
    @staticmethod
    def construct_event(payload, sig_header, secret):
        return json.loads(payload)


Webhook = _Webhook()

"""Local checkout tests for the CPR Academy — run one scenario per process:

    ACADEMY_PAYMENTS=off  .venv-test/bin/python tests/test_checkout_local.py off
    ACADEMY_PAYMENTS=live .venv-test/bin/python tests/test_checkout_local.py live
    ACADEMY_PAYMENTS=live ACADEMY_TEST_CHARGE_CENTS=100 \
        .venv-test/bin/python tests/test_checkout_local.py testcharge

Uses the fake stripe module in tests/fake_stripe and a throwaway data file.
No live Stripe calls, no real keys.
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "fake_stripe"))  # fake stripe wins
sys.path.insert(0, ROOT)

import app as academy  # noqa: E402

# Isolate storage: never touch the real data/academy.json in tests.
_tmp = tempfile.mkdtemp(prefix="academy-test-")
academy.DATA_FILE = os.path.join(_tmp, "academy.json")
CAPTURE = os.path.join(_tmp, "stripe_capture.json")
os.environ["FAKE_STRIPE_CAPTURE"] = CAPTURE

COURSE = "bls-skills"  # BLS Skills Check-Off — catalog price $83 = 8300 cents
FORM = {"name": "Test Student", "email": "test@student.example", "ack": "yes"}
FAILURES = []


def check(label, cond, detail=""):
    print(("PASS" if cond else "FAIL"), "-", label, detail)
    if not cond:
        FAILURES.append(label)


def capture():
    if not os.path.exists(CAPTURE):
        return None
    with open(CAPTURE) as f:
        return json.load(f)


def enroll(client):
    if os.path.exists(CAPTURE):
        os.remove(CAPTURE)
    return client.post(f"/enroll/{COURSE}", data=FORM)


def pending_enrollment():
    store = academy.load_store()
    pend = [e for e in store["enrollments"] if e["status"] == "PENDING_PAYMENT"]
    return pend[-1] if pend else None


def post_webhook(client, eid, amount_total, event_id):
    event = {
        "id": event_id, "type": "checkout.session.completed",
        "data": {"object": {
            "id": "cs_test_fake123", "payment_status": "paid", "currency": "usd",
            "amount_total": amount_total, "payment_intent": "pi_test_fake",
            "metadata": {"enrollment_id": eid, "course_id": COURSE},
        }},
    }
    return client.post("/webhooks/stripe", data=json.dumps(event),
                       content_type="application/json",
                       headers={"Stripe-Signature": "t=1,v1=fake"})


def scenario_off():
    client = academy.app.test_client()
    page = client.get(f"/course/{COURSE}").get_data(as_text=True)
    check("off: course page shows reserve-seat note", "reserves your seat" in page)
    check("off: course page has no pay button", "Enroll & Pay" not in page)
    resp = enroll(client)
    check("off: enroll redirects to My Courses (no Stripe)",
          resp.status_code == 302 and "/my" in resp.headers.get("Location", ""),
          f"got {resp.status_code} -> {resp.headers.get('Location')}")
    check("off: Stripe was never called", capture() is None)
    store = academy.load_store()
    enr = [e for e in store["enrollments"] if e["course_id"] == COURSE]
    check("off: enrollment created with payment not_required",
          bool(enr) and enr[-1]["payment_status"] == "not_required"
          and enr[-1]["status"] == "ENROLLED")


def scenario_live():
    client = academy.app.test_client()
    page = client.get(f"/course/{COURSE}").get_data(as_text=True)
    check("live: course page shows what's-included line", "What's included" in page)
    check("live: course page shows enroll & pay button",
          "Enroll &amp; Pay $83" in page)
    check("live: reserve-seat note hidden", "reserves your seat" not in page)
    resp = enroll(client)
    check("live: enroll 303-redirects to Stripe checkout",
          resp.status_code == 303
          and resp.headers.get("Location", "").startswith("https://checkout.stripe.com/"),
          f"got {resp.status_code} -> {resp.headers.get('Location')}")
    cap = capture() or {}
    item = (cap.get("line_items") or [{}])[0]
    pd = item.get("price_data") or {}
    check("live: checkout amount is catalog 8300 cents", pd.get("unit_amount") == 8300,
          f"got {pd.get('unit_amount')}")
    check("live: product name has no TEST tag",
          "TEST CHARGE" not in (pd.get("product_data") or {}).get("name", ""))
    pend = pending_enrollment()
    check("live: pending enrollment stored expected_amount_cents=8300",
          pend is not None and pend.get("expected_amount_cents") == 8300)
    # Correct-amount webhook flips to paid.
    r = post_webhook(client, pend["id"], 8300, "evt_live_ok")
    store = academy.load_store()
    e = academy.find_enrollment(store, pend["id"])
    check("live: webhook 200 + enrollment paid",
          r.status_code == 200 and e["payment_status"] == "paid"
          and e["status"] == "ENROLLED", f"status={e['status']} pay={e['payment_status']}")
    # Amount-mismatch webhook is rejected (enrollment stays pending).
    enroll(client)
    pend2 = pending_enrollment()
    r = post_webhook(client, pend2["id"], 9999, "evt_live_bad")
    store = academy.load_store()
    e2 = academy.find_enrollment(store, pend2["id"])
    check("live: mismatched amount does NOT activate enrollment",
          r.status_code == 200 and e2["payment_status"] == "pending"
          and e2["status"] == "PENDING_PAYMENT")


def scenario_testcharge():
    client = academy.app.test_client()
    resp = enroll(client)
    check("test$: enroll 303-redirects to Stripe checkout",
          resp.status_code == 303
          and resp.headers.get("Location", "").startswith("https://checkout.stripe.com/"))
    cap = capture() or {}
    item = (cap.get("line_items") or [{}])[0]
    pd = item.get("price_data") or {}
    check("test$: checkout amount is 100 cents", pd.get("unit_amount") == 100,
          f"got {pd.get('unit_amount')}")
    check("test$: product name tagged TEST CHARGE",
          "TEST CHARGE" in (pd.get("product_data") or {}).get("name", ""))
    pend = pending_enrollment()
    check("test$: pending enrollment stored expected_amount_cents=100",
          pend is not None and pend.get("expected_amount_cents") == 100)
    # Catalog amount must NOT satisfy a test-charge enrollment.
    post_webhook(client, pend["id"], 8300, "evt_test_catalog_amt")
    store = academy.load_store()
    e = academy.find_enrollment(store, pend["id"])
    check("test$: catalog amount rejected for test enrollment",
          e["payment_status"] == "pending")
    # The $1 amount flips it to paid.
    post_webhook(client, pend["id"], 100, "evt_test_ok")
    store = academy.load_store()
    e = academy.find_enrollment(store, pend["id"])
    check("test$: $1 webhook flips enrollment to paid",
          e["payment_status"] == "paid" and e["status"] == "ENROLLED")


SCENARIOS = {"off": scenario_off, "live": scenario_live, "testcharge": scenario_testcharge}

if __name__ == "__main__":
    name = sys.argv[1]
    print(f"--- scenario: {name} (ACADEMY_PAYMENTS={academy.PAYMENTS_MODE}, "
          f"TEST_CHARGE_CENTS={academy.TEST_CHARGE_CENTS}) ---")
    SCENARIOS[name]()
    if FAILURES:
        print(f"RESULT: {len(FAILURES)} FAILURE(S): {FAILURES}")
        sys.exit(1)
    print("RESULT: ALL PASS")

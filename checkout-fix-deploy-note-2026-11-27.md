# CPR Academy — Checkout Fix: Deploy Note (Nov 27, 2026)

Code changes are committed locally, NOT pushed and NOT deployed. Derrick does
the push + dashboard steps himself.

## 1. Push
Push the local commit to `github.com/bigdbo1210/cpr-academy` (Render deploys
from that repo).

## 2. Render env vars — Derrick confirms/sets these himself (dashboard only)
Service: `cpr-academy-demo` → Environment:
- `ACADEMY_PAYMENTS` = `live` (render.yaml now also pins `live`, so a
  blueprint sync can no longer revert it to `off`)
- `STRIPE_SECRET_KEY` = the **live** secret key from the CPR Stripe account
  (Stripe Dashboard → Developers → API keys). Dashboard only — never in code,
  chat, or git.
- `STRIPE_WEBHOOK_SECRET` = the signing secret from step 3.
- `ACADEMY_TEST_CHARGE_CENTS` = leave UNSET for normal operation (see step 5).

## 3. Stripe webhook endpoint — register in the Stripe dashboard
Stripe Dashboard (CPR account) → Developers → Webhooks → Add endpoint:
- URL: `https://cpr-academy.onrender.com/webhooks/stripe`
- Events: `checkout.session.completed`, `charge.refunded`,
  `charge.dispute.created`
- Copy its signing secret into Render as `STRIPE_WEBHOOK_SECRET` (step 2).
Without this, a student can pay at Stripe while the Academy keeps them
"Not paid" forever — the webhook is the only path that marks an enrollment paid.

## 4. Deploy
Deploy the latest commit from the Render dashboard (Derrick's established
pattern), after steps 2–3 are in place.

## 5. $1 live test sequence (do this once, right after deploy)
1. Render → Environment: set `ACADEMY_TEST_CHARGE_CENTS` = `100`. Redeploy.
   ⚠️ While this is set, **EVERY** checkout charges $1 and is tagged
   "— TEST CHARGE" in Stripe.
2. Enroll in any course with Derrick's own name/email, pay the $1 with a real
   card.
3. Confirm: the enrollment flips to paid in the Academy, and the $1 charge
   appears in Stripe under descriptor **DONTBEORDINARYCPR**.
4. Refund the $1 charge in the Stripe dashboard.
5. **Delete `ACADEMY_TEST_CHARGE_CENTS` from Render and redeploy
   immediately** — the Academy is then live at real catalog prices.

## What changed in code
- `render.yaml`: `ACADEMY_PAYMENTS` pinned `off` → `live`;
  `ACADEMY_TEST_CHARGE_CENTS` declared `sync: false` (dashboard-managed).
- `app.py`: payments mode passed to the course page; pending enrollments now
  store `expected_amount_cents`; checkout uses the test-charge override when
  set (product name tagged "— TEST CHARGE"); the Stripe webhook validates
  `amount_total` against the stored expected amount (falls back to catalog
  price for older enrollments).
- `templates/course.html`: the "reserves your seat / takes no payment" note
  now shows ONLY when payments are off. In test/live mode the page shows a
  "What's included" line and an "Enroll & Pay $X — Secure Checkout" button.
- `templates/base.html`: nav trimmed to **Courses** + **Instructor**
  ("My Courses" and "Verify a Certificate" links removed; the routes still
  exist in code — students reach My Courses via the email resume flow).
  ⚠️ FLAG: the **Instructor** link was kept — it is Derrick's own instructor
  access. Remove it too if he wants the nav to be Courses only.
- `tests/`: local test harness (fake Stripe module; no live calls).
  20/20 checks passed locally 2026-11-27 (off / live / $1-override scenarios).

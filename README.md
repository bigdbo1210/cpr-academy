# Don't Be Ordinary CPR Academy

**Learn Online. Practice In Person. Save a Life.**

A blended-learning academy for Don't Be Ordinary CPR, AED & First Aid
Training, LLC (Louisville, KY). Students enroll, complete coursework and
an assessment online, receive an **online course completion certificate**
with a public verification code, then book a short in-person skills
session. Only the instructor can mark skills passed — online completion
is never certification by itself.

## Demo flow

1. Browse the catalog (Derrick's real courses and prices) and enroll.
2. Complete 3 modules, then pass the 5-question assessment (80%+).
3. Get your completion certificate + verification code (try the sample
   record: `DBO-2026-0001`).
4. Book a hands-on skills session.
5. Instructor sign-in (`ddennis` / `academy123`, demo only) → dashboard →
   **Mark Skills Passed** after the in-person session. The public
   certificate record then shows skills verified.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Development build: JSON file storage (`data/academy.json`), demo
checkout (no payments taken), demo instructor credentials. Production
hardening (database, real payments, real accounts) is the next phase.

© 2026 Derrick D. Dennis · All Rights Reserved. See LICENSE.

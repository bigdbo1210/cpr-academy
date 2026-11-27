# Wording-Match Check — Stripe Sandbox Catalog vs. Academy Website
**Date:** Nov 22, 2026 · **Type:** Read-only check. Nothing was changed on the site or in Stripe.

**Question asked:** Does the Stripe catalog match the Academy website's class descriptions and wording, word for word?

**Answer: No.** Of the 14 sandbox products, **zero** match the website on both name and price. Three names match exactly (Heartsaver CPR AED, BLS Skills Check-Off, AED Training) — and even those three carry different prices. Most differences are deliberate: the sandbox catalog was built from the Nov 21 repricing proposal, which (a) grosses every price up for the mandatory eBook + Stripe fee, and (b) uses the audit-corrected course names the website does not use yet. The proposal is still **awaiting Derrick's approval**, so today the live site and the catalog describe the same courses with different names, different prices, and — for the Heartsaver line — different credential claims.

**Sources:** Site wording from `app.py` (COURSES / HOW_IT_WORKS / CREDENTIAL_OFFERED — the definitions the pages render from), verified against the live site Nov 22 (homepage, /course/heartsaver-cpr-aed, /course/acls — live pages match the code exactly, including the updated blended ACLS wording). Catalog names/prices from `repricing-proposal-2026-11-21.md` and the Nov 21 sandbox build report. **Limit:** the sandbox products' full description text is not recorded in any project file, so description comparison below is at the level the build documented (credential type, skills session, eBook bundling), not a character-by-character diff of Stripe's description fields.

---

## 1. Names and prices — every course

| # | Website (exact name) | Website price | Stripe sandbox (exact name) | Stripe price | Name match? |
|---|---|---|---|---|---|
| 1 | BLS for Healthcare Providers | $150 | BLS Provider (Blended) | $173 | ✗ different |
| 2 | BLS Instructor-Led (Full Course, In Person) | $150 | BLS Instructor-Led | $173 | ✗ parenthetical dropped |
| 3 | BLS Skills Check-Off | $80 | BLS Skills Check-Off | $100 | ✓ name / ✗ price |
| 4 | HeartCode ACLS Online | $318 | ACLS | $328 | ✗ shortened |
| 5 | HeartCode PALS Online | $318 | PALS | $328 | ✗ shortened |
| 6 | Heartsaver CPR AED | $160 | Heartsaver CPR AED | $169 | ✓ name / ✗ price |
| 7 | Heartsaver Pediatric First Aid CPR AED | $160 | Heartsaver Pediatric | $169 | ✗ shortened |
| 8 | Heartsaver First Aid Training | $100 | Heartsaver First Aid | $107 | ✗ "Training" dropped |
| 9 | OSHA Bloodborne Pathogens | $90 | Heartsaver Bloodborne Pathogens | $93 | ✗ different (see §3) |
| 10 | CPR Instructor Course | $600 | BLS Instructor Course | $619 | ✗ different (see §3) |
| 11 | AED Training | $100 | AED Training | $104 | ✓ name / ✗ price |
| 12 | Babysitters & Nanny Training | $160 | Babysitters & Nanny | $166 | ✗ "Training" dropped |
| 13 | Shaken Baby Syndrome / Abusive Head Trauma | $95 | Shaken Baby Prevention | $99 | ✗ completely different name |
| 14 | — **not on the website** — | — | Heartsaver First Aid CPR AED, Combined | $160 | ✗ catalog-only (see §4) |

**Prices:** every shared course costs more in the catalog than on the site — by design (eBook + Stripe-fee gross-up from the proposal): BLS ×2 +$23, Skills Check-Off +$20, ACLS/PALS +$10 each, Heartsaver CPR AED/Pediatric +$9, First Aid +$7, Babysitters +$6, AED +$4, Shaken Baby +$4, Bloodborne Pathogens +$3, Instructor +$19. The website's own homepage FAQ still quotes the site prices ("BLS is $150. Heartsaver CPR AED is $160, First Aid is $100, and a skills check-off is $80"), so a customer comparing the site to a Stripe checkout page would see two different price lists for the same classes.

## 2. The eBook — in the catalog prices, absent from the website

The word **"eBook" appears nowhere on the Academy website** (Nov 21 audit, still true in today's code). The catalog prices silently include it (BLS +$17.30, Heartsaver +$3.25; ACLS/PALS eBook already inside AHA's HeartCode). The site's BLS/ACLS/PALS blurbs enumerate exactly what the price includes — e.g. BLS: *"This listing includes the HeartCode BLS Online license, your in-person skills session with an AHA Instructor, and your AHA BLS Provider eCard — all included in the $150 price"* — with no eBook mentioned. A student reading the website would not know an eBook is part of what they're paying for at the catalog price.

## 3. Where the catalog uses the CORRECTED names and the website doesn't (audit items 4–6)

These catalog names are the audit's fixes; the website still carries the old wording:

- **BLS:** Site = "BLS for Healthcare Providers" — AHA's retired pre-2020 name (audit #4). Catalog = "BLS Provider (Blended)" — the current name.
- **Bloodborne Pathogens:** Site = "OSHA Bloodborne Pathogens" — "OSHA" is not in AHA's course name (audit #5). Catalog = "Heartsaver Bloodborne Pathogens" — correct.
- **Instructor:** Site = "CPR Instructor Course," whose blurb promises *"The pathway to leading CPR and first aid classes of your own"* — broader than what the course is (audit #6: it is AHA's BLS Instructor Essentials path). Catalog = "BLS Instructor Course" — the accurate scope.

So on these three, the catalog is *more* correct than the website — but they still do not match each other, which is what Derrick asked.

## 4. Course on one side only

- **Catalog only:** "Heartsaver First Aid CPR AED, Combined" ($160). The website has no combined course — it sells CPR AED ($160) and First Aid ($100) separately, $260 total for what the catalog sells as one $160 product (audit #3; the combined course at Derrick's $160-flat rule is step C of the audit's next steps, not yet built on the site).
- **Website only:** none — all 13 site courses have a catalog counterpart.

## 5. Credential wording (eCard vs. certificate) — the Heartsaver conflict repeats in reverse

The website's three Heartsaver pages (CPR AED, Pediatric, First Aid) contradict themselves *on the same page* (audit #2, verified live today on /course/heartsaver-cpr-aed):

- Fact box: *"Document you receive: A Don't Be Ordinary CPR, AED & First Aid Training, LLC course-completion certificate, issued after your instructor verifies your hands-on skills in person. **This is not an AHA eCard.**"*
- Paragraph directly below: *"This is an American Heart Association course… **Your AHA eCard is issued through the American Heart Association** once you complete the course requirements… **That eCard is the credential this course earns.**"*
- "How it works" adds a third version: *"…then your certificate is issued here."*

The sandbox catalog descriptions were written to the eCard side (eCard bundled into the Heartsaver products, per the Nov 21 build report). **Result: the catalog matches the website's lower paragraph and its Disclosure page, and directly conflicts with the website's fact box and "How it works" text on all three Heartsaver courses.** A customer who reads the site's fact box and then the Stripe product description gets opposite answers about what credential they earn.

Other credential/description points:

- **ACLS / PALS — now aligned.** The site's updated pages (verified live Nov 22) sell both as blended: *"$318 includes the HeartCode license, your in-person skills session, and your AHA ACLS/PALS Provider eCard — issued once you have successfully completed both parts."* The catalog's "ACLS (blended, skills incl.)" / "PALS (blended, skills incl.)" at $328 matches that substance. The catalog does **not** repeat the original audit overclaim ("100% online, eCard immediately") — that wording is gone from the site too. Only the name (shortened) and price (+$10 fee gross-up) differ.
- **BLS Skills Check-Off — eBook question is live in the catalog.** Site: *"$80 covers the skills session and the eCard process; no online license is included or charged,"* credential = official AHA BLS Provider eCard. The catalog was built at $100 — the with-eBook figure — even though the proposal flags this as **undecided** (fee-only would be $83; these students did their online course elsewhere). If the sandbox description says an eBook is included, it contradicts the site's model for this course.
- **Bloodborne Pathogens — substance matches, name doesn't.** Site credential text: a Don't Be Ordinary certificate, *"This is not an AHA eCard"*; site "How it works": *"your certificate is issued immediately."* The catalog description likewise says certificate, no eCard (per build report) — aligned — under the different name (§3).
- **House courses (AED Training, Babysitters & Nanny, Shaken Baby) — substance matches.** Site discloses all three as Don't Be Ordinary courses with its own certificate, not an AHA eCard; catalog descriptions say the same (per build report). Differences are name (Babysitters/Shaken Baby) and price only.
- **Instructor course manual:** the proposal prices the catalog product on the basis that the $600 *"already includes a PRINTED manual."* The website never mentions a manual — the blurb is just *"Teach what you know. The pathway to leading CPR and first aid classes of your own — with coaching practice and monitored teaching."*
- **Skills sessions:** aligned everywhere else — both sides include the in-person skills session for all blended courses at no separate charge, and both sides mark Shaken Baby and Bloodborne Pathogens as online-only with no skills session.

## 6. Bottom line

- **Word-for-word match: NO — 0 of 14.**
- Differences fall in three buckets: (1) **prices** — all higher in the catalog by the proposal's eBook + fee math, while the proposal itself is still awaiting Derrick's approval and the site (including its FAQ) still quotes the old prices; (2) **names** — the catalog uses shortened names for 6 courses and the audit-corrected names for 3, none of which the website uses yet; (3) **credential wording** — the Heartsaver eCard-vs-certificate contradiction is unresolved on the website, and the catalog sides against the site's own fact boxes.
- Nothing here is a surprise error in the catalog build — it faithfully implements the Nov 21 proposal. The mismatch exists because the **website has not yet been updated** to the proposal (audit next steps B–E are still pending Derrick's go). Until the site and the catalog are moved together, they will not match — and the live-account catalog should not be built until they do.

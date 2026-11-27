# CPR Academy — Wording vs. Price: Split Decision Sheet
Prepared Nov 22, 2026, after the wording-match check (wording-match-check-2026-11-22.md).

## Why this sheet exists
The Nov 22 check found 0 of 14 Stripe sandbox products match the Academy website on both name and price. The mismatches are NOT one decision — they are two different kinds:

1. **Wording / name / credential fixes** — already approved by Derrick Nov 21 as part of the audit fix list. No price change involved.
2. **Price changes** — the Nov 21 repricing proposal (eBook + Stripe-fee gross-up). Still AWAITING Derrick's approval. A "go" on wording must not be read as a "go" on these prices.

Keep the two approvals separate.

---

## Bucket A — Wording only (already approved Nov 21, no prices touched)
- Rename on the website to the corrected names the catalog already uses:
  - "BLS for Healthcare Providers" → "BLS Provider (Blended)"
  - "OSHA Bloodborne Pathogens" → "Heartsaver Bloodborne Pathogens"
  - "CPR Instructor Course" → "BLS Instructor Course" (and narrow its blurb — it is the AHA BLS Instructor Essentials path, not a general CPR/first-aid instructor pathway)
- Fix the Heartsaver contradiction on CPR AED, Pediatric, and First Aid pages: fact box says "course-completion certificate — this is not an AHA eCard" while the paragraph below and the Disclosure page say the AHA eCard is the credential. One answer, everywhere: the eCard side (matches catalog and Disclosure).
- State the mandatory eBook on the website — the word "eBook" appears nowhere on the site today, while catalog prices include it.
- Add the combined Heartsaver First Aid CPR AED course page to the website (catalog-only today; site sells the halves separately for $260 total).
- Shortened catalog names to align one way or the other, word for word: ACLS / PALS, Heartsaver Pediatric, Heartsaver First Aid, Babysitters & Nanny, Shaken Baby Prevention — Derrick's word-for-word rule (Nov 22) means site and catalog must carry the identical string, whichever form he picks.

## Bucket B — Prices only (proposal, NOT approved — Derrick's numbers, stated plain, no recommendation)
Current site price → proposal price:
- BLS Provider (Blended): $150 → $173
- BLS Instructor-Led: $150 → $173
- Heartsaver CPR AED: $160 → $169
- Heartsaver Pediatric: $160 → $169
- Heartsaver First Aid: $100 → $107
- ACLS: $318 → $328
- PALS: $318 → $328
- Bloodborne Pathogens: $90 → $93
- Instructor Course: $600 → $619
- AED Training: $100 → $104
- Babysitters & Nanny: $160 → $166
- Shaken Baby: $95 → $99

Open flags from the proposal itself:
1. **BLS Skills Check-Off** — site $80. Fee-only $83, or $100 with the eBook. Students did the online part elsewhere, so whether the mandatory-eBook rule applies to them is Derrick's call. Sandbox is currently built at $100.
2. **Combined Heartsaver First Aid CPR AED** — Derrick set $160 flat. Grossed up with eBook + fee it would be $169. Sandbox currently holds $160 flat.
3. **Instructor Course** — proposal assumes the $600 already includes a printed manual, fee-only gross-up to $619. Confirm the manual assumption.

Note: the website homepage FAQ still quotes the site prices ($150 / $160 / $100 / $80). Whichever bucket-B decision lands, the FAQ must move with it in the same deploy — otherwise customers see two price lists.

## Bucket C — Launch gate (separate from both buckets)
- Stripe: personal verification is COMPLETE (Nov 22). One Derrick-only step remains: turn on two-step authentication, which unlocks "Agree and submit." Bank/payout details have not yet been requested by Stripe.
- Website on the Stripe account already corrected to the Academy only: cpr-academy.onrender.com (confirmed Nov 22). The in-person site is out of this launch entirely, per Derrick's Nov 22 direction.
- Sequence after activation (from launch-test-checklist-2026-11-22.md): recreate the catalog in the LIVE account with the final approved names/prices → wire Academy checkout → one real test payment end to end. If activation slips, Monday Nov 23 is a soft open (seats reserved, no payment), not a broken checkout.

## The two yeses needed, separately
1. "Run Bucket A" — wording/name/credential alignment, prices untouched.
2. Bucket B, line by line or as a whole — including the three flags.

Nothing goes live in the live Stripe account until both are settled, because building the live catalog locks in names and prices together.

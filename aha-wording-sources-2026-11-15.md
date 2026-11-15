# AHA wording sources for catalog descriptions (pulled Nov 15, 2026)

Directive (Derrick, Nov 15): for every course the American Heart Association offers, the
site's course description must be AHA's own official wording, not our summaries — and the
homepage card text must align cleanly. This file records, per course, the AHA source the
live description (app.py `blurb`, shown on the homepage card and the course page) came from.
All AHA pages below were opened and read on 2026-11-15.

## AHA courses — description is AHA's wording, verbatim or near-verbatim

- **BLS for Healthcare Providers (HeartCode BLS)** — AHA description verbatim from the
  Shop CPR product page, "HeartCode® BLS Online":
  https://shopcpr.heart.org/heartcode-bls
  ("HeartCode BLS Online is the online portion of BLS blended learning that will adequately
  prepare students for hands-on practice and testing of BLS skills. It uses a variety of
  eLearning assets such as dramatizations, animations, self-directed learning, and
  interactive activities to teach students BLS knowledge and skills.")
  One site framing sentence follows it (what this listing includes at the $150 price) —
  that sentence is ours, as with the ACLS/PALS listings.

- **BLS Skills Check-Off** — AHA sells no standalone skills-session product and publishes
  no separate description for it; the session is the hands-on portion of HeartCode BLS.
  The blurb is built from AHA's own sentences: the HeartCode BLS description above
  (https://shopcpr.heart.org/heartcode-bls) and the AHA HeartCode completion rule —
  "Successful completion of both a HeartCode Online course and a hands-on skills session
  is required to receive an American Heart Association course completion eCard, valid for
  two years" (AHA HeartCode FAQ, cpr.heart.org — also quoted in
  aha-acls-pals-pears-source-2026-11-15.md). The opening and booking sentences are site
  framing in plain language.

- **BLS Instructor-Led (Full Course, In Person)** — AHA description verbatim from the
  AHA's official 2025 BLS Provider Course (Instructor-Led Training) FAQ on cpr.heart.org:
  https://cpr.heart.org/-/media/CPR-Files/2025-documents-for-cpr-heart-edits-posting/Courses-Kits/2025-Guidelines-FAQ-BLS-ILT.pdf
  (the "What is the American Heart Association's 2025 BLS Provider Course?" answer, plus
  the FAQ's target-audience answer, quoted in full).

- **HeartCode ACLS Online** — AHA description verbatim from the Shop CPR product page:
  https://shopcpr.heart.org/heartcode-acls
  (full official paragraph, including the "continuously adapting learning path" sentence
  restored Nov 15; previously trimmed). The closing "This listing is the online course
  only…" sentence is site framing preserving the settled online-only disclosure.

- **HeartCode PALS Online** — AHA description verbatim from the Shop CPR product page:
  https://shopcpr.heart.org/heartcode-pals
  (same treatment as ACLS: full official paragraph restored, closing framing sentence
  is ours).

- **Heartsaver CPR AED** — AHA description verbatim from the Shop CPR product page,
  "Heartsaver® CPR AED Online":
  https://shopcpr.heart.org/heartsaver-cpr-aed-online

- **Heartsaver Pediatric First Aid CPR AED** — AHA description verbatim from the Shop CPR
  product page, "Heartsaver® Pediatric First Aid CPR AED Online":
  https://shopcpr.heart.org/heartsaver-pediatric-first-aid-cpr-aed-online

- **Heartsaver First Aid Training** — AHA description verbatim from the Shop CPR product
  page, "Heartsaver® First Aid Online":
  https://shopcpr.heart.org/heartsaver-first-aid-online

- **OSHA Bloodborne Pathogens** (site title kept; AHA counterpart is Heartsaver
  Bloodborne Pathogens) — AHA sentences verbatim from two Shop CPR pages:
  the course page ("Heartsaver® Bloodborne Pathogens is designed to meet Occupational
  Safety and Health Administration (OSHA) requirements for bloodborne pathogens training
  when paired with site-specific instruction"):
  https://shopcpr.heart.org/courses/heartsaver-bloodborne-pathogens
  and the product page ("Bloodborne Pathogens Online is a self-directed course that uses
  interactive lessons to teach you comprehensive skills for protecting, acting, cleaning,
  and telling as it relates to practical application for dealing with bloodborne
  pathogens"):
  https://shopcpr.heart.org/heartsaver-bloodborne-pathogens-online
  DELIBERATE OMISSION: the product page's next sentence ("This program is for anyone with
  limited or no medical training who needs an AHA course completion card") was NOT used.
  This catalog course is the Academy's own online course and issues a Don't Be Ordinary
  CPR certificate, not an AHA card — quoting that sentence would imply an AHA eCard,
  which the site's audit rules forbid. The closing annual-requirement sentence is ours
  (it also appears in this course's How It Works).

## Not AHA courses — Derrick's own wording (no AHA source; never presented as AHA)

- **AED Training** — Don't Be Ordinary CPR's own course; plain wording, tidied Nov 15.
- **Babysitters & Nanny Training** — Don't Be Ordinary CPR's own course; plain wording,
  tidied Nov 15.
- **Shaken Baby Syndrome / Abusive Head Trauma** — Don't Be Ordinary CPR's own course;
  plain wording, tidied Nov 15.
- **CPR Instructor Course** — Don't Be Ordinary CPR's own course; plain wording, tidied
  Nov 15. Copy uses "AHA Instructor" vocabulary only; nothing implies the AHA certifies
  trainers (it does not).

## Notes

- Prices, FAQ wording, "an AHA Instructor" (no personal name), and the ACLS/PALS
  online-only framing from commit 392ab0e are unchanged by this pass.
- The ® in "Heartsaver®" first mentions follows AHA's own product-page usage.
- AHA's HeartCode BLS page renders its asset list with a stray empty item
  ("dramatizations, , animations"); the site text reads "dramatizations, animations" —
  a punctuation artifact only, no wording changed.

# CPR Academy — Site Update Change Log (Bucket A wording + Bucket B prices)
**Date:** Nov 22, 2026 · **Scope:** code changes only. NOT deployed — Derrick deploys manually from his Render dashboard. Stripe checkout NOT wired in this pass; the "reserves your seat / no payment today" enrollment language is unchanged.

Goal: the website now matches the live Stripe catalog exactly — same 14 course names, same prices, one credential answer (the AHA eCard side), the mandatory eBook stated, and skills-assessment claims only where they belong.

## Files touched
- `app.py` — COURSES, HOW_IT_WORKS, PREREQUISITES, CREDENTIAL_OFFERED, OFFICIAL_LANGUAGE_IDS, course_detail credential lookup + flash text
- `course_content.py` — appended the assembled `heartsaver-combined` content entry
- `templates/home.html` — FAQ prices
- `templates/base.html` — og/twitter meta description price ("BLS $150" → "BLS $173", both tags)
- `static/img/tiles/tile-heartsaver-combined.jpg` — NEW file, copied from tile-heartsaver-cpr-aed.jpg so the new course has a tile

## Renames (course IDs / URL slugs UNCHANGED — no links break, no redirects needed)
| Was | Now |
|---|---|
| BLS for Healthcare Providers | BLS Provider (Blended) |
| BLS Instructor-Led (Full Course, In Person) | BLS Instructor-Led |
| HeartCode ACLS Online | ACLS |
| HeartCode PALS Online | PALS |
| Heartsaver Pediatric First Aid CPR AED | Heartsaver Pediatric |
| Heartsaver First Aid Training | Heartsaver First Aid |
| OSHA Bloodborne Pathogens | Heartsaver Bloodborne Pathogens |
| CPR Instructor Course | BLS Instructor Course |
| Babysitters & Nanny Training | Babysitters & Nanny |
| Shaken Baby Syndrome / Abusive Head Trauma | Shaken Baby Prevention |

Unchanged names: BLS Skills Check-Off, Heartsaver CPR AED, AED Training.
Also: the BLS Instructor Course blurb was narrowed to the AHA BLS Instructor Essentials pathway (Bucket A) and now states the $619 price includes the printed BLS Instructor manual; its prerequisite now reads "Current AHA BLS Provider certification…". The enrollment-closed flash message no longer hardcodes the old "CPR Instructor Course" name.

## Prices (old → new, everywhere including blurbs, HOW_IT_WORKS, credential texts, FAQ, meta tags)
- BLS Provider (Blended): $150 → **$173**
- BLS Instructor-Led: $150 → **$173**
- BLS Skills Check-Off: $80 → **$83**
- Heartsaver CPR AED: $160 → **$169**
- Heartsaver Pediatric: $160 → **$169**
- Heartsaver First Aid: $100 → **$107**
- Heartsaver First Aid CPR AED (Combined): NEW at **$160**
- ACLS: $318 → **$328**
- PALS: $318 → **$328**
- Heartsaver Bloodborne Pathogens: $90 → **$93**
- BLS Instructor Course: $600 → **$619**
- AED Training: $100 → **$104**
- Babysitters & Nanny: $160 → **$166**
- Shaken Baby Prevention: $95 → **$99**

## New course added
**Heartsaver First Aid CPR AED (Combined)** — id `heartsaver-combined`, $160, blended workflow, added to OFFICIAL_LANGUAGE_IDS (carries the official-AHA page language). Full COURSES / HOW_IT_WORKS / PREREQUISITES entries written. **Its module content is assembled from the two existing courses**: in `course_content.py`, `CONTENT["heartsaver-combined"]` = Heartsaver CPR AED modules + questions followed by Heartsaver First Aid modules + questions (10 modules, 30 questions; its How-it-works says "30-question assessment" to match).

## Heartsaver fact-box contradiction — fixed
The three Heartsaver courses (and the new combined course) previously rendered the shared "blended" fact-box text ("course-completion certificate… This is not an AHA eCard") directly above the paragraph promising the AHA eCard. Fix: `course_detail` now honors a per-course `"credential"` override (`course.get("credential") or CREDENTIAL_OFFERED[...]`), and each Heartsaver course carries eCard wording: official AHA Heartsaver eCard, issued after the online course + in-person skills session (First Aid: once course requirements are complete — no skills claim). Their HOW_IT_WORKS steps no longer end with "then your certificate is issued here" — they now end with the AHA eCard issued through the American Heart Association. The shared "blended" credential text still serves Babysitters & Nanny and the BLS Instructor Course, which do earn the Don't Be Ordinary certificate.

## eBook policy — now stated on the site (the word "eBook" appeared nowhere before)
- BLS Provider (Blended) + BLS Instructor-Led: BLS Provider Manual eBook named as included and required — in the blurb, HOW_IT_WORKS, and CREDENTIAL_OFFERED (aha_blended / instructor_led).
- Heartsaver CPR AED, Heartsaver Pediatric, Heartsaver First Aid, Combined: "the Heartsaver course eBook (included, and required course material)" in blurb + HOW_IT_WORKS + credential text.
- ACLS / PALS: stated that the Provider Manual eBook is included inside the HeartCode course — blurb, HOW_IT_WORKS step 1, and CREDENTIAL_OFFERED (aha_online). Their blended substance (license + in-person skills + eCard after both parts) is otherwise untouched, per the Nov 22 live wording.
- BLS Skills Check-Off: explicitly NO eBook — blurb now ends "No online license and no eBook are included with this session," and HOW_IT_WORKS + credential text say the same.
- House courses with no eBook product (Bloodborne Pathogens, AED, Babysitters, Shaken Baby): no eBook statement added — none exists to include.

## Skills-assessment wording
- Blended courses (BLS, Heartsaver CPR AED, Heartsaver Pediatric, Combined, ACLS, PALS): HOW_IT_WORKS now states the in-person skills session is included in the price.
- **AED Training**: tag changed to "Online course — no skills session"; HOW_IT_WORKS rewritten as fully online and explicitly states "there is no skills session or skills assessment"; fact box now uses the online-certificate text (per-course credential override). Blurb never claimed skills.
- **Heartsaver First Aid**: tag changed to "Online course"; HOW_IT_WORKS rewritten with no skills-session step (eCard issued once course requirements are complete). Blurb never claimed skills.
- **BLS Skills Check-Off**: page states it is the hands-on finish for students who already completed the official AHA HeartCode BLS online course on their own (elsewhere), keeps the honest line that no online license is included or charged, and the $83 covers the skills session + eCard process. For Derrick's own students, the skills session remains inside their course price (stated in the BLS / Heartsaver HOW_IT_WORKS).

## Verification (local, Flask test client — app not deployed)
- All 17 pages return 200: homepage, /policy, /verify, and all 14 course pages.
- Every course page's <h1> and price match the live Stripe catalog list exactly (14/14); homepage lists all 14 names; homepage FAQ shows $173 / $169 / $107 / $83.
- No old course name and no stale price ($150, $318, $600, $95, $90, $80) appears on any rendered page.
- All four Heartsaver fact boxes are eCard-consistent (no "This is not an AHA eCard" contradiction).
- Combined course serves 10 modules / 30 questions assembled from the two source courses.
- Enrollment language verified intact: "Secure checkout opens with our production launch — enrolling today reserves your seat and takes no payment."

## Flags / observations (not changed — Derrick's call)
1. **Enrolled-student module text**: the AED Training and First Aid *module prose* inside `course_content.py` (visible only after enrollment) still mentions a hands-on/skills session (e.g., AED's closing module: "Your hands-on session runs live AED drills…"; First Aid module 1: "the one your skills session will test"). The public course pages no longer claim a skills assessment for either course, but the in-course text was left untouched rather than rewriting Derrick's teaching content unasked.
2. **templates/policy.html** states BLS and Heartsaver courses lead to the AHA eCard "after the authorized course and its in-person skills evaluation" — left as-is (legal/policy text), but it sits slightly against the no-skills-session model for Heartsaver First Aid.
3. The phrases "HeartCode ACLS Online" / "HeartCode PALS Online" still appear *inside* the ACLS/PALS page body text as the name of AHA's online license product ("your official HeartCode ACLS Online license") — the course names themselves are now exactly "ACLS" / "PALS". Left because the license product genuinely carries that name.
4. The combined course reuses the Heartsaver CPR AED tile image until a dedicated tile exists.


---

# Follow-up (Nov 22, 2026, evening) — AED Training & Heartsaver First Aid: NO eBook, NO skills assessment
**Direction (Derrick, Nov 22 evening):** "Those require no ebook or in person skills assessment" — AED Training and Heartsaver First Aid carry neither an eBook nor an in-person skills assessment. Applied fully below. This resolves Flags 1 and 2 from the earlier section of this log. Code only — NOT deployed, no prices changed, no other course's data changed, checkout untouched.

## Heartsaver First Aid — eBook statements removed (`app.py`, 3 places)
No optional-eBook offer was substituted — the course simply has no eBook. AHA eCard credential wording and the $107 price are unchanged.
- **Credential text:** "The $107 includes the online course and the course eBook — no additional charge." → "The $107 includes the online course and the eCard — no additional charge."
- **Blurb:** "This listing includes the online course, the Heartsaver course eBook (included, and required course material), and your AHA eCard — all included in the $107 price." → "This listing includes the online course and your AHA eCard — all included in the $107 price."
- **HOW_IT_WORKS:** deleted the sentence "Your Heartsaver course eBook is included with your enrollment and is required course material." The two steps now read: complete the modules + 15-question assessment, then the AHA Heartsaver First Aid eCard is issued once course requirements are complete.

## AED Training — eBook check (`app.py`, `course_content.py`, templates)
Confirmed: **no eBook language existed for AED Training anywhere** (blurb, credential text, HOW_IT_WORKS, module prose, templates) — nothing to remove. Price $104 unchanged. Its page already stated the course is completed entirely online with no skills session or skills assessment.

## In-course module prose (`course_content.py`) — every change listed
1. **First Aid, Module 1 "First Aid Basics: The First Five Minutes":** "This module's standard is the one your skills session will test: gloves, assessment, and the right first call." → "This module sets the standard the rest of the course builds on: gloves, assessment, and the right first call."
2. **First Aid, Module 5 "Prevention, Choking, and Putting It Together":** "…so that in your skills session, and in real life, the sequence is already in your hands." → "…so that when a real emergency comes, the sequence is already in your hands."
3. **AED Training, Module 4 "Readiness: Pads, Batteries, and Your Workplace Program":** "Your hands-on session runs live AED drills until the four verbs are reflexes." → "Then take it to your own workplace device: run live AED drills on your AED or trainer — pads on, clear, shock — until the four verbs are reflexes." (Drills are now framed as practice on the student's own workplace device/program, per the no-session model.)
Teaching substance is unchanged in all three — only the delivery-model references moved.
**Coupling note:** the Combined course's content is assembled from the Heartsaver CPR AED + First Aid module lists, so prose changes 1–2 also flow into the Combined course's first-aid modules. Both rewrites are deliberately neutral — they neither promise a skills session to First Aid students nor deny one to Combined students, and the Combined course's own page, HOW_IT_WORKS, and credential text still state its included in-person skills session.

## Course-page template (`templates/course.html`, 2 conditional changes — every other course's page renders byte-identical)
- The fact-box "Rescheduling: one complimentary reschedule per skills-session reservation…" line no longer renders on the First Aid and AED pages (condition now excludes `first-aid` and `aed`). It still renders for every other non-online-only course.
- The official-AHA paragraph on the First Aid page no longer ends "…and the in-person skills evaluation" — for `first-aid` only, it now reads "Your AHA eCard is issued through the American Heart Association once you complete the course requirements. That eCard is the credential this course earns." All other official-AHA course pages keep the full sentence.
- Reviewed and left: the non-official paragraph's general sentence "Official AHA eCards are issued only through the American Heart Association after an authorized AHA course and in-person skills evaluation" still appears on the AED page — it is a general statement about AHA eCards (identical on the Shaken Baby and OSHA pages), not a claim that AED Training includes a session.

## Policy page (`templates/policy.html`, AHA disclosure paragraph)
Was: "…lead to the AHA eCard, issued through the American Heart Association after the authorized course and its in-person skills evaluation." (swept First Aid into a skills-evaluation claim).
Now: "…lead to the **AHA eCard**, issued through the American Heart Association. For the BLS courses and the blended Heartsaver courses (Heartsaver CPR AED, Heartsaver Pediatric, and Heartsaver First Aid CPR AED (Combined)), the eCard follows the authorized course and its in-person skills evaluation. Heartsaver First Aid is completed entirely online — its eCard is issued once the online course requirements are complete, with no in-person skills evaluation."

## Verification (local, Flask test client — app not deployed)
- All 17 pages return 200 (homepage, /policy, all 14 course pages + verify flow pages as before).
- **First Aid page, course content:** zero "eBook", zero "skills session", zero "skills evaluation", zero "skills-session reservation"; $107 and the AHA Heartsaver First Aid eCard credential intact.
- **AED page:** zero "eBook", no rescheduling/skills-session line; its How-it-works still states plainly "there is no skills session or skills assessment"; $104 intact.
- **Module prose:** no "skills session" / "hands-on session" remains in the First Aid or AED modules; AED own-device drill framing present; First Aid teaching substance verified intact.
- **Policy page:** new First Aid carve-out present; blended Heartsaver skills-evaluation wording kept.
- **Regression checks:** Heartsaver CPR AED page still states its eBook, skills evaluation, and rescheduling line; Babysitter page rescheduling line intact; BLS page eBook intact; Combined course still assembles 10 modules / 30 questions and its page still states its eBook + skills session.

## Flags / observations (not changed — Derrick's call)
1. **Site-wide meta tagline:** `templates/base.html`'s generic meta/og/twitter descriptions ("Learn online, then finish with a short hands-on skills session" / "Skills sessions in Louisville") appear in the `<head>` of every page, including First Aid and AED. They are site-wide business copy (identical on the online-only Shaken Baby and OSHA pages), not course claims, so they were left — rewriting the site tagline is a wording decision for Derrick.
2. **Enrolled-flow behavior (functional, not wording):** First Aid and AED still carry workflow `"blended"` in `app.py`, so `requires_skills()` is still true for them — after a passing quiz the app still flashes "Now book your hands-on skills session…" and holds the enrollment at ONLINE_COMPLETE, and `templates/learn.html`'s generic header says passing "unlocks skills-session booking" for every course. All public wording is now consistent; making the post-quiz flow match the no-skills model means changing those two courses' workflow, which changes enrollment/certificate behavior — left for Derrick's go rather than bundled into a wording pass.


---

# AHA terminology alignment (Nov 22, 2026, night)
**Direction (Derrick, Nov 22, voice call):** use the American Heart Association's own wording instead of paraphrase — "instead of using my words, if it says blended we'll say blended" — so a student moving between this site and AHA's feels no wording difference. Reference sources: `aha-wording-sources-2026-11-15.md`, `aha-language-audit-2026-11-02.md`, `aha-acls-pals-pears-source-2026-11-15.md`. AHA standard forms applied: **"blended learning"** (the online portion of blended learning + a hands-on skills session), **"hands-on skills session"** (AHA's exact phrase, HeartCode FAQ), **"hands-on practice and skills testing,"** **"Instructor-Led Training,"** and **"course completion eCard / card."** Code only — NOT deployed. No prices changed, no course names changed, no credential facts changed, no workflow changed, lesson teaching substance unchanged.

## Course format tags (`app.py` COURSES — every blended course now carries AHA's "blended learning" label)
| Before | After | Courses |
|---|---|---|
| AHA blended — HeartCode online + in-person skills session | Blended learning — HeartCode online portion + hands-on skills session | BLS Provider (Blended), ACLS, PALS |
| Blended: online + skills session | Blended learning — online portion + hands-on skills session | Heartsaver CPR AED, Heartsaver Pediatric, Heartsaver First Aid CPR AED (Combined), Babysitters & Nanny |
| Skills session only | Hands-on skills session only | BLS Skills Check-Off |
| Instructor-led — full course in person, no online portion | Instructor-Led Training — full course in person, no online portion | BLS Instructor-Led |
| Online course | Online course — no hands-on skills session | Heartsaver First Aid |
| Online course — no skills session | Online course — no hands-on skills session | AED Training, Shaken Baby Prevention |
| Online only — no skills session | Online course — no hands-on skills session | Heartsaver Bloodborne Pathogens |

## `app.py` — catalog text (COURSES blurbs/credentials, HOW_IT_WORKS, PREREQUISITES, CREDENTIAL_OFFERED, status labels)
1. "in-person skills session" → "hands-on skills session" — ×17 across the catalog region (BLS/ACLS/PALS blurbs and HOW_IT_WORKS, Heartsaver blurbs and credential texts).
2. CREDENTIAL_OFFERED `aha_blended` + `aha_online`: "pass your in-person skills evaluation" → "pass your hands-on skills session" (×2).
3. CREDENTIAL_OFFERED `skills_only`: "The $83 includes the skills evaluation and the eCard process… and you pass the skills evaluation." → "The $83 includes the hands-on skills session and the eCard process… and you pass the hands-on skills session."
4. HOW_IT_WORKS `bls` step 6: "Pass the practice, evaluation, and skills testing" → "Pass the hands-on practice and skills testing" (AHA's own phrase).
5. HOW_IT_WORKS `bls-skills`: "Enroll, book your skills session, and upload…" → "Enroll, book your hands-on skills session, and upload…"; "Pass the evaluation and your official AHA BLS Provider eCard…" → "Pass the hands-on skills session and your official AHA BLS Provider eCard…".
6. HOW_IT_WORKS `babysitter` step 2: "Book your in-person session for hands-on practice and review with your instructor." → "Book your hands-on skills session for practice and review with your instructor."
7. HOW_IT_WORKS `bls-instructor-led` step 2: "Book your in-person class session." → "Book your instructor-led class session."
8. PREREQUISITES `bls`: "…at eLearning.heart.org before your skills session." → "…before your hands-on skills session."
9. HOW_IT_WORKS `aed`: "there is no skills session or skills assessment" → "there is no hands-on skills session or skills assessment."
10. HOW_IT_WORKS `shaken-baby` + `osha`: "this course is 100% online — there is no in-person appointment." → "this course is 100% online — there is no hands-on skills session." (×2)
11. Status labels (student-facing, My Courses): "Online complete — book your skills session" → "Online complete — book your hands-on skills session"; "AHA completion verified — book your skills session" → "AHA completion verified — book your hands-on skills session."

## `templates/home.html`
12. Hero: "then prove it hands-on with your instructor in a short skills session." → "then finish with a short hands-on skills session with your instructor."
13. Step 2: heading "Book Your Skills Session" → "Book Your Hands-On Skills Session"; body "Pick a hands-on session block that fits your life." → "Pick a hands-on skills session block that fits your life."
14. Step 3 (per the Nov 2 AHA language audit's recommendation — AHA's credential language is the course completion eCard/card): heading "Get Certified" → "Get Your Card / Certificate"; body "…and Don't Be Ordinary CPR issues your official certification." → "…and your course completion eCard or certificate is issued."
15. Hours card: "Skills sessions and instructor-led classes:" → "Hands-on skills sessions and instructor-led classes:"
16. FAQ (price answer): "and a skills check-off is $83" → "and the BLS Skills Check-Off is $83" (price unchanged).
17. FAQ (blended learning answer): "you book a short in-person skills session with your instructor (20–30 minutes)" → "you book a short hands-on skills session with your instructor (20–30 minutes)".
18. FAQ (card answer): "then you schedule your skills assessment with your instructor. Pass the assessment, and your name goes on the roster" → "then you schedule your hands-on skills session with your instructor. Pass the skills session, and your name goes on the roster".

## `templates/course.html`
19. Official-AHA paragraph: "and the in-person skills evaluation" → "and the hands-on skills session".
20. Non-official paragraph: "after an authorized AHA course and in-person skills evaluation" → "after an authorized AHA course and hands-on skills session".
21. Fact box: "One complimentary reschedule per skills-session reservation" → "per hands-on skills session reservation".

## `templates/policy.html`
22. "Missing an in-person skills appointment" → "Missing a hands-on skills session appointment".
23. "any required in-person session" → "any required hands-on skills session".
24. "the eCard follows the authorized course and its in-person skills evaluation" → "the eCard follows the authorized course and its hands-on skills session".
25. First Aid carve-out: "with no in-person skills evaluation" → "with no hands-on skills session".

## `templates/learn.html` / `templates/my.html`
26. learn.html: "unlocks skills-session booking" → "unlocks hands-on skills session booking" (wording only — the post-quiz workflow itself is unchanged).
27. my.html: "your included skills session unlocks" → "your included hands-on skills session unlocks"; "Before your skills session:" → "Before your hands-on skills session:".

## `course_content.py` — delivery-model references only (teaching substance untouched)
28. Heartsaver CPR AED module: "your hands-on session will put it into muscle memory" → "your hands-on skills session will put it into muscle memory".
29. Pediatric module: "Your hands-on session covers child and infant CPR and AED practice…" → "Your hands-on skills session covers…".
30. Pediatric module: "Your hands-on session will test the pediatric skills…" → "Your hands-on skills session will test…".
31. Babysitters module: "your in-person session practices these skills on manikins" → "your hands-on skills session practices these skills on manikins".
32. Instructor module: "verify online completion before the skills session" → "verify online completion before the hands-on skills session".

## Left alone — and why
- **base.html meta tagline (report only, per instructions — NOT rewritten):** "Learn online, then finish with a short hands-on skills session." AHA terminology would **not** change its key term — it already uses AHA's exact phrase "hands-on skills session." The only AHA-alignment note: the tagline describes the blended path generically on every page, including the online-only courses (First Aid, AED, Shaken Baby, Bloodborne Pathogens) that have no session — the same standing flag as before; any rewrite is Derrick's tagline call.
- AHA-verbatim blurbs (HeartCode BLS/ACLS/PALS, Heartsaver Online descriptions) were already AHA's own wording — untouched except the site-framing sentences' session term (item 1). "Course completion card" inside those verbatim AHA texts is AHA's own phrase — kept.
- Quiz/assessment questions (including the instructor-course question "before the skills session the instructor must verify…") — assessment content, not delivery labels; untouched.
- Instructor-pathway phrasing ("in-person instructor session," "Book your in-person instructor session") — no AHA student-facing standard form exists for it in the sources; untouched.
- Flash messages and workflow logic — behavior unchanged, per scope; the one generic flash already read "hands-on skills session."
- Program-name styling (HeartCode® / Heartsaver® ® marks): the Nov 2 audit rates this a low-risk styling nicety; blurbs already carry Heartsaver® on first mention. Not changed in this pass — Derrick's call if he wants ® styling extended.

## Verification (local, Flask test client — app not deployed)
- All 17 pages return 200 (homepage, /policy, /verify, all 14 course pages).
- All 14 course names and prices on every course page and the homepage match the live Stripe catalog list exactly (the Babysitters & Nanny name renders HTML-escaped as `&amp;`, as before).
- Every blended course's tag, blurb, and HOW_IT_WORKS now uses "blended learning" + "hands-on skills session" consistently; no "in-person skills session / skills evaluation" remains in any student-facing catalog text, template, or module delivery reference.
- First Aid page retains its no-eBook, no-session model with the new aligned tag; policy page retains the First Aid carve-out in the new terminology.

## Academy slogan placement (Nov 22, 2026, night)

Derrick's line: "Get certified, renewed today, and save a life" — display form: **"Get Certified, Renewed Today, and Save a Life."**

- Searched the whole site (app.py, templates/, static/) for the slogan and variants ("save a life," "get certified," "renewed today"). The exact slogan did NOT exist. Closest fragments: hero headline "Learn Online. Practice In Person. Save a Life." and the poster image alt text ("Get Certified or Renewed Today. Train. Prepare. Save a Life.").
- Added the slogan once, visibly, in the homepage hero in templates/home.html: a `<p class="slogan">` directly under the main headline and above the intro paragraph / "Explore Courses" call to action, with a matching style rule (`.hero p.slogan` — gold #f2b134, 17px, weight 800), consistent with the hero's existing gold accent styling.
- Nothing else changed: no prices, course names, AHA terminology, or the base.html meta tagline touched. Not deployed.
- Verified locally (Flask test client): homepage returns 200 and the slogan renders in the page body immediately after the `<h1>`.

## Slogan correction (Nov 22, 2026, night — Derrick's exact wording)

Derrick corrected the slogan: it is **"Get Certified or Renewed Today & Save a Life"** — "or Renewed," and the ampersand symbol &, not the word "and."

- templates/home.html hero slogan line changed from "Get Certified, Renewed Today, and Save a Life." to "Get Certified or Renewed Today &amp; Save a Life." (the `&amp;` entity in source renders as &).
- Searched the rest of the site (app.py, templates/, static/) for other renderings of the slogan: none found. The hero headline "Learn Online. Practice In Person. Save a Life." and the poster image alt text are different lines and were left untouched.
- Verified locally (Flask test client): homepage returns 200 and the rendered text contains the slogan exactly as "Get Certified or Renewed Today & Save a Life."; the old wording no longer appears. Nothing else changed. Not deployed.

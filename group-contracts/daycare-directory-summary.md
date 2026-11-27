# Louisville Licensed Childcare Directory — Summary

**Built:** October 27, 2026 · **For:** Don't Be Ordinary CPR group-outreach program
**File:** `daycare-directory-louisville.csv` (129 rows)

## Totals

| | Count |
|---|---|
| Total facilities in directory | **129** |
| New outreach targets (not in the existing CPR target list) | **114** |
| Already in existing target list (flagged `already_contacted=yes`, incl. the 3 already emailed Oct 27) | 15 |
| Rows with a **verified public email** | **11** |
| Phone-only rows (`route=phone`) | 118 |
| Licensed centers | 122 |
| Certified family child care homes | 7 |

## Verified public emails (11 rows — every one read off the business's own website; none guessed)

**New targets:**
1. Foundations Whole Child Development — admin@foundationslouisville.com
2. Ridgewood Child Development Center (Director April Baker) — april@ridgewoodlouisville.org
3. Talk Childcare 2 Me (E Indian Trail) — info@talkchildcaretome.com
4. Talk Childcare To Me – Cane Run — info@talkchildcaretome.com
5. Talk Childcare – Poplar Level — info@talkchildcaretome.com
6. Talk Childcare Extended Learning Center — info@talkchildcaretome.com
7. Kids R Us Daycare & Preschool – Location I (Crums Ln) — kidsrus40203@yahoo.com
8. Kids R Us Daycare & Preschool – Location II (Crums Ln, Shively) — kidsrus40203@yahoo.com
9. Ready To Learn Child Care (E Burnett Ave) — swarfiel@bellsouth.net

**Already contacted / in the existing program:**
10. Southside Christian Child Care — info@southsidechristianchildcare.com (emailed Oct 27)
11. Home of the Innocents — info@homeoftheinnocents.org (emailed Oct 27)

Distinct new email addresses: **5** (Talk Childcare's one address covers 4 locations; Kids R Us's covers 2). Email verification source URLs are in the CSV's `email_source_url` column.

## Sources used

- **Official registry (identified, not enumerable from this session):** Kentucky CHFS "Find Child Care" page — https://www.chfs.ky.gov/agencies/dcbs/dcc/pages/find-care.aspx — which points to the **kynect Public Child Care Search**: https://kynect.ky.gov/benefits/s/childcareprovider (lists only licensed Type I / Type II centers and certified family child care homes; shows license type, address, inspection reports, KY All STARS level).
- Facility name/address/phone coverage was assembled from public business listings (Google Places-style place cards surfaced in web search, Daycare.com, Care.com, Winnie) and cross-checked against operators' own location pages where available (KinderCare, Young Kids Academy, Bluegrass Academy, Kids Academy, Kids R Us, Talk Childcare).
- Emails were verified **only** on each center's own website (contact/home pages), per the no-guessing rule.

## Gaps and limits — read before outreach

1. **The kynect registry could not be enumerated here.** The portal returned HTTP 403 to text fetching and its search is an interactive JavaScript app (Salesforce Lightning). A complete registry pull (Jefferson County likely has ~300+ regulated providers including ~150+ certified homes) needs a live-browser session on kynect.ky.gov/benefits/s/childcareprovider — recommended as the parent agent's next step to close the gap and to confirm each row's exact license type.
2. **License type is therefore approximate.** Rows are marked "Licensed center (verify in kynect)" unless the operator's own site states licensing (e.g., Ridgewood CDC, Lively Children). Certified-home classification rests on residential setting / directory "Home-Based" tags. The certified-home sector is **undercounted** (7 rows) — most homes have no web presence and only the kynect search surfaces them.
3. **Phone/address are from public listings, not the registry.** A minority of rows lack a phone (not published in listings checked — flagged in notes, e.g., Beth Haven CDC, Wee-Care, Learning Ladder, Joy-Ti) or a confirmed zip. Same-address collisions exist (517 W Breckinridge ×3 programs; 3845 and 3930 Cane Run ×2 each; 5057 Poplar Level ×2; 5313 Hames Trace ×2) — each is flagged in notes; verify the current license holder in kynect before calling.
4. **Chains publish no center emails.** KinderCare (8 Louisville centers), La Petite (2), Primrose (2), Bright Horizons — contact forms and chain phone lines only, so they are phone-route despite their size.
5. **A few listed websites were unusable:** Smiling Faces CDC and Loving Care Inc (fetch failed), Harbor House (bot check), Leaps & Bounds (domain parked), International Kids Academy (listed domain resolves to a Fort Worth TX business — flagged, do not use), Sunnyside (site under reconstruction). Those rows are phone-only.
6. Two known Louisville chains were seen in listings without verifiable contacts and were **left out rather than padded in**: Kiddie Academy of Louisville-East, The Gardner School of Louisville, Butterfly Garden Academy, Westport Early Childhood Center, First Kids Early Childhood.
7. Nothing in this directory has been contacted. Outreach copy must follow Derrick's rule: **no prices in outreach** — written quote per group by headcount.

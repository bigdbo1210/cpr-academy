# Don't Be Ordinary CPR Academy — Business & Technology Blueprint

*As shared by Derrick on 2026-10-20 (drafted with ChatGPT assistance; mermaid
diagram CSS from the original paste omitted). This is the founding planning
document for the Academy project. Debo's synthesis note is at the bottom.*

---

**Don't Be Ordinary CPR Academy**
**Business & Technology Blueprint | October 2026**

Business: Don't Be Ordinary CPR, AED & First Aid Training, LLC
Proposed product: Don't Be Ordinary CPR Academy
Primary market: Louisville, Kentucky, with mobile and group training expansion
Business objective: Automate customer enrollment, payments, training access,
hands-on scheduling, credential tracking, and renewal reminders.

Recommendation: build a branded online CPR and First Aid Training Academy that
allows customers to register, pay, complete approved online coursework,
schedule their hands-on skills assessments, and receive their official
certification after successfully meeting the requirements. Turn the existing
training experience into a system that serves customers without the owner
personally handling every registration, payment, scheduling request, and
follow-up.

## 1. The certification requirement we must get right

For American Heart Association (AHA) CPR courses requiring practical skills,
completing the online training does not automatically make someone certified.
Students complete the approved online component and receive an online course
completion certificate. They must also successfully complete their hands-on
skills session before receiving the official AHA course completion eCard.

The app recognizes two separate milestones:

1. **Online learning completed** — student receives proof of completing the
   online coursework, not an official BLS provider card.
2. **Hands-on skills passed** — authorized instructor verifies competency and
   the official eCard is issued through the appropriate certification provider.

This protects the business's reputation, meets certification requirements,
and ensures employers can trust the credentials students receive.

## 2. The proposed app experience

**DON'T BE ORDINARY — CPR & FIRST AID ACADEMY**
*Learn Online. Practice In Person. Save a Life.*

- Explore Our CPR Courses
- My Courses — view learning and completion status
- Book Skills Test — choose an available appointment
- My Credentials — access completion records and eCard links
- Group Training — request on-site employee training

Mobile-first web application. Customers use it on phones or computers without
installing anything from an app store.

## 3. Master development blueprint (v1.0)

### A. Core operating model
The Academy functions as a branded registration and training-management
platform supporting approved blended-learning CPR and first aid programs.
The system manages the customer's experience while authorized education
providers and affiliated training centers remain responsible for their
official curricula, evaluations, and credentials.

Five core services:
1. Course selection and secure online registration.
2. Online payment and authorized course access.
3. Verification of online coursework completion.
4. Scheduling and documentation of hands-on skills assessments.
5. Official credential tracking, customer support, and renewal reminders.

### B. Initial course catalog
| Course | Target | Pricing |
|---|---|---|
| BLS Provider — blended learning | Healthcare professionals and students | $130 reference; confirm what is included |
| BLS hands-on skills assessment only | Students with completed, accepted online coursework | $80 reference |
| Heartsaver First Aid CPR AED | Workplace employees and general public | Set after calculating course costs |
| Heartsaver Pediatric First Aid CPR AED | Childcare and youth program workers | Set after calculating course costs |
| Group and mobile CPR training | Employers, churches, schools, organizations | Customized group quote |

Only list courses the business is authorized and equipped to provide. Identify
the credential issuer and the exact course version on each listing. Each
course page must explain the total price, whether the online portion is
included, expected format, skills requirements, rescheduling policies, and
which credential the customer may receive.

### C. Customer journey
1. **Find a course** — visit the Academy, select profession/purpose, get
   relevant course choices.
2. **Register and pay** — full legal name, email, phone, enrollment details,
   accept policies, secure checkout.
3. **Start approved online coursework** — after confirmed payment, system
   supplies an authorized access code or directs the customer to the approved
   learning provider. Students with previously completed accepted coursework
   may select skills-only service instead.
4. **Verify online completion** — student submits official online completion
   record; system marks it pending verification until authenticity confirmed.
5. **Schedule skills assessment** — eligible students select an available
   in-person appointment at the training office or another approved location.
   Tentative slots may be reserved earlier, subject to timely verification.
6. **Complete practical assessment** — instructor conducts and documents
   required hands-on instruction, practice, testing, remediation per course
   requirements.
7. **Receive official credential** — successful records routed through the
   affiliated training center's authorized credential process; Academy records
   issuance status and provides claiming instructions/link.
8. **Receive renewal reminders** — with consent, reminders before the
   documented certification expiration date.

### D. Customer application pages
Home; Course Catalog; Checkout; My Learning; My Appointments; My
Credentials; Corporate Training; Help Center.

### E. Owner and instructor dashboard
Enrollment and payment records; student contact details and course info;
online completion verification queue; skills session appointments, instructor
assignments, capacity limits; skills assessment results and remediation;
official eCard issuance tracking; refund/cancellation/rescheduling history;
gross revenue, costs, conversion rates, uncompleted enrollments; group
training inquiries and follow-ups. Instructors access only records necessary
for their assigned sessions.

### F. Essential automation
1. Payment confirmation and receipt. 2. Authorized course-access instructions
after checkout. 3. Reminder when online coursework remains incomplete.
4. Notification when a completion record needs verification. 5. Scheduling
invitation after verification. 6. Appointment confirmation and reminders.
7. Follow-up for missed appointments or remediation. 8. Credential claiming
instructions once officially issued. 9. Renewal reminders at 90/60/30 days
before expiration. Automation must never mark skills passed or claim an
official credential issued without an authorized record confirming it.

### G. Rules, safety, and quality control
- Confirm the business's current AHA Training Center affiliation and
  authorization before enabling AHA-specific enrollment or distribution.
- Obtain and distribute online course licenses only through permitted channels.
- Do not copy proprietary curriculum videos, materials, tests, or logos
  without authorization.
- Distinguish online learning completion from full provider certification.
- Require hands-on competency assessment before credential issuance.
- Never generate a substitute official AHA eCard.
- Use a compliant hosted payment provider; never store card details.
- Protect student information: access controls, secure storage, retention,
  documented privacy practices.
- Accessible mobile pages, transparent terms, clear support procedures.
- Block unavailable instructor hours; prevent overbooking.

### H. Technical blueprint
Branded mobile-responsive web app, initially powered by established payment
and scheduling tools; custom system when enrollment volume justifies.
Stack: responsive web app / PWA; Python Flask backend; PostgreSQL database;
Stripe Checkout or Square payments; integrated booking; transactional email;
SMS with consent; role-based dashboards; managed cloud hosting; official
provider verification workflows.
Key records: Students, Courses, Orders, Enrollments, Online Completions,
Skills Sessions, Assessments, Instructor Assignments, Credentials,
Communications.

### I. Development and launch phases
- **Phase 1 — Validate and launch the storefront:** branded website, approved
  courses published, secure payment, online learning instructions, limited
  skills-assessment calendar.
- **Phase 2 — Customer and instructor management:** student status tracking,
  document submission, verification workflows, credential records, reminders,
  reporting.
- **Phase 3 — Expand:** employer dashboards, group registration,
  multi-instructor scheduling, bulk purchases, group invoices, client renewal
  tracking, additional approved locations.

### J. Business performance measures
Course inquiries and paid registrations; completed skills assessments; gross
revenue by course; net contribution after direct costs; no-show/cancellation
rates; admin time per student; percentage of eligible learners credentialed
without avoidable delays; group contracts and returning customers.
**Initial pilot goal: 10 paying students through the full
training-to-credential workflow.**

### K. Success definition
Customers can independently register, pay, access authorized coursework,
schedule training, and track completion status — and the business manages
them accurately without excessive administrative work. Long-term: a
repeatable training operation serving individuals, employers, and
organizations across a wider service area.

## 5. Platform spending comparison (as drafted)

| Approach | Pricing noted | Recommendation in draft |
|---|---|---|
| Square Appointments Plus | $49/mo per location + processing | Launch with this |
| Thinkific Start | $109/mo | Consider for own supplementary courses |
| Custom Python web app | Varies | Build after validating demand |

## 6. First 30 days (checklist as drafted)

- **Week 1 — Certification and business rules:** confirm Training Center
  permissions, eLearning distribution, official eCard workflow; finalize
  course selection, actual prices, package contents.
- **Week 2 — Build storefront:** branded mobile-friendly landing page and
  course catalog; configure secure checkout and skills sessions.
- **Week 3 — Test the complete process:** payment, course access, proof
  verification, booking; reminders, cancellations, skills outcomes, credential
  tracking.
- **Week 4 — Launch pilot:** open enrollment to existing CPR leads and
  referral partners; run first paid cohort; measure profitability and admin
  time.

Markets to prioritize: healthcare students and professionals; childcare
providers; employers purchasing group training. Protect the teaching schedule
by offering skills assessments only in designated training blocks.

## 7. The determining question (as posed in the draft)

Are you currently operating through an American Heart Association Training
Center that allows you to distribute HeartCode/Heartsaver online course
access to your own customers, or are you only authorized to conduct and
submit the hands-on training? That distinction determines how the online
course purchase and official credential workflows should be built.

---

## Debo's synthesis (2026-10-20)

- This blueprint and Debo's proposal are the same plan: blended model,
  two milestones, management platform around authorized content.
- Pushback on Section 5: renting Square + Thinkific ($49/mo + $109/mo) is the
  cost trap Derrick feared. Build and OWN the management layer (storefront,
  registration, verification queue, skills calendar, credential tracking,
  renewal reminders) on his proven Flask stack; use a payment provider only
  as the pipe. We don't build the classroom (AHA's content stays AHA's);
  we build the front office.
- The catalog can launch with his full real menu from dontbeordinarycpr.com
  (BLS $130, Skills Check-Off $80, Heartsaver $155, Pediatric $155, First Aid
  $95, AED $95, Babysitter/Nanny $155, Shaken Baby $70, OSHA $80, Instructor
  $600), not just the two reference rows.
- Awaiting Derrick's answer on Training Center distribution rights — it
  decides how course access and eCard workflow get built.
- **Price decisions (Derrick to Debo, 2026-10-20):** BLS stays **$130**
  (a pasted third-party analysis claiming the site listed $120 was wrong —
  Debo's same-day audit of the live site verified $130). Shaken Baby
  Syndrome increases **$70 → $95**. All other Academy prices = published
  site prices. The $95 site edit was sent to the UENI editor 2026-10-20.
- **Affiliation status (Derrick, 2026-10-20):** "Independent / not sure."
  Open fact-finding: what credential do his students receive today, and who
  issues it? AHA eCards cannot be issued off an instructor's own videos —
  the online portion must be AHA's product, or the full course taught in
  person by a Training-Center-aligned instructor.

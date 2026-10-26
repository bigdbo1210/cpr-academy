"""
Don't Be Ordinary CPR, AED & First Aid Training, LLC — course platform.

Students enroll, learn online, pass a quiz, and receive an ONLINE COURSE
COMPLETION certificate with a public verification code. That is milestone
one, and it is NOT a certification card. Milestone two is the in-person
hands-on skills session: only the instructor can mark skills passed,
after which the student's record shows skills verified by the instructor.
Official credentials are issued by Don't Be Ordinary CPR through its
normal business process — this demo never fabricates a credential.

Run:  flask --app app run   (or: python app.py)
Instructor login: username ddennis; password set via ACADEMY_INSTRUCTOR_PASSWORD.
"""
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
import secrets
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/New_York")  # Derrick's business runs on Louisville time

# --- Instructor availability for session booking -------------------------
# Set by Derrick 2026-10-25/26. He teaches 7th grade Mon–Thu (JCPS), so on
# school days only the evening block is offered; Fridays add the morning;
# Saturdays are a full class day (9–3); Sundays are by appointment only
# (phone) and never appear in the picker. On JCPS school-out days his
# daytime opens up, so all three blocks are offered. School-out dates are
# the verified JCPS 2026–27 calendar (see jcps-2026-27-school-out-days.md).
BLOCK_MORNING = "Morning (9:00–11:00 AM)"
BLOCK_AFTERNOON = "Afternoon (1:00–3:00 PM)"
BLOCK_EVENING = "Evening (5:00–7:00 PM)"
ALL_BLOCKS = [BLOCK_MORNING, BLOCK_AFTERNOON, BLOCK_EVENING]


def _expand_range(a, b):
    d = datetime.fromisoformat(a).date()
    end = datetime.fromisoformat(b).date()
    while d <= end:
        yield d.isoformat()
        d += timedelta(days=1)


SCHOOL_OUT_DAYS = set()
for _a, _b in [
    ("2026-08-04", "2026-08-04"),  # Non-Flex In-Service
    ("2026-09-07", "2026-09-07"),  # Labor Day
    ("2026-09-23", "2026-09-23"),  # Family-Teacher Conferences
    ("2026-09-28", "2026-10-02"),  # Fall Break
    ("2026-11-02", "2026-11-03"),  # Gold Day + Election Day
    ("2026-11-25", "2026-11-27"),  # Thanksgiving Break
    ("2026-12-21", "2027-01-01"),  # Winter/Christmas Break
    ("2027-01-18", "2027-01-18"),  # MLK Jr. Day
    ("2027-02-15", "2027-02-16"),  # Gold Day + Conferences
    ("2027-03-26", "2027-03-26"),  # PD Flex Day
    ("2027-03-29", "2027-04-02"),  # Spring Break
    ("2027-04-30", "2027-04-30"),  # Oaks Day
    ("2027-05-18", "2027-05-18"),  # Primary Election Day
]:
    SCHOOL_OUT_DAYS.update(_expand_range(_a, _b))


def blocks_for_date(d):
    """Time blocks offered on a given date (a datetime.date)."""
    if d.weekday() == 6:  # Sunday — by appointment only, call ahead
        return []
    if d.weekday() == 5:  # Saturday — classes 9 AM to 3 PM
        return [BLOCK_MORNING, BLOCK_AFTERNOON]
    if d.isoformat() in SCHOOL_OUT_DAYS:  # school is out — daytime opens
        return list(ALL_BLOCKS)
    if d.weekday() == 4:  # Friday — 8–11 AM and 4–9 PM
        return [BLOCK_MORNING, BLOCK_EVENING]
    return [BLOCK_EVENING]  # Mon–Thu school days — 4–9 PM window

app = Flask(__name__)
app.secret_key = os.environ.get("ACADEMY_SECRET_KEY", "academy-dev-secret-key")

# Payments: "off" (default) | "test" | "live". Live mode is never enabled
# by code alone — Derrick approves the switch and supplies live keys via
# the hosting environment. Stripe secrets live ONLY in environment vars.
PAYMENTS_MODE = os.environ.get("ACADEMY_PAYMENTS", "off")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

def _stripe():
    import stripe  # lazy import: the app runs fine without the package in off mode
    stripe.api_key = STRIPE_SECRET_KEY
    return stripe

INSTRUCTOR_USER = "ddennis"
INSTRUCTOR_PASSWORD = os.environ.get("ACADEMY_INSTRUCTOR_PASSWORD", "academy123")  # set ACADEMY_INSTRUCTOR_PASSWORD in production

# -----------------------------
# Course catalog (Derrick's real menu + locked prices, 2026-10-20)
# -----------------------------

COURSES = [
    {"id": "bls", "name": "BLS for Healthcare Providers", "price": 150, "bank": "cpr", "workflow": "aha_blended",
     "tag": "Official AHA blended — HeartCode online + in-person skills session",
     "blurb": "The complete official package: your HeartCode BLS online course license, an in-person skills training and evaluation session with Derrick, and your official AHA BLS Provider eCard on successful completion — all included in the $150 price, no extra charge for the skills session or eCard."},
    {"id": "bls-skills", "name": "BLS Skills Check-Off", "price": 80, "bank": "cpr", "workflow": "skills_only",
     "tag": "Skills session only",
     "blurb": "Already finished your online BLS coursework? Book the hands-on skills check-off and finish the job."},
    {"id": "bls-instructor-led", "name": "BLS Instructor-Led (Full Course, In Person)", "price": 150, "bank": "cpr", "workflow": "instructor_led",
     "tag": "Instructor-led — full course in person, no online portion",
     "blurb": "Prefer to learn it all in the room? The complete BLS course taught in person by Derrick — instruction, written examination, and skills testing — ending with the official AHA BLS Provider eCard through the authorized pathway."},
    {"id": "heartsaver-cpr-aed", "name": "Heartsaver CPR AED", "price": 155, "bank": "cpr", "workflow": "blended",
     "tag": "Blended: online + skills session",
     "blurb": "Adult, child, and infant CPR with AED — the workplace and community flagship course."},
    {"id": "pediatric", "name": "Heartsaver Pediatric First Aid CPR AED", "price": 155, "bank": "cpr", "workflow": "blended",
     "tag": "Blended: online + skills session",
     "blurb": "For childcare providers and parents: pediatric first aid, CPR, and AED with an emphasis on childhood emergencies."},
    {"id": "first-aid", "name": "Heartsaver First Aid Training", "price": 95, "bank": "knowledge", "workflow": "blended",
     "tag": "Blended: online + skills session",
     "blurb": "Recognize and respond to the emergencies you are most likely to meet: bleeding, burns, choking, allergic reactions, and more."},
    {"id": "aed", "name": "AED Training", "price": 95, "bank": "cpr", "workflow": "blended",
     "tag": "Blended: online + skills session",
     "blurb": "Focused AED training: pad placement, safety, special situations, and confident, fast response."},
    {"id": "babysitter", "name": "Babysitters & Nanny Training", "price": 155, "bank": "knowledge", "workflow": "blended",
     "tag": "Blended: online + skills session",
     "blurb": "Safety, first aid, and emergency confidence for the people families trust with their children."},
    {"id": "shaken-baby", "name": "Shaken Baby Syndrome / Abusive Head Trauma", "price": 95, "bank": "knowledge",
     "workflow": "online_only",
     "tag": "Online course — no skills session",
     "blurb": "Recognize, prevent, and respond to abusive head trauma — required knowledge for childcare professionals."},
    {"id": "osha", "name": "OSHA Bloodborne Pathogens", "price": 80, "bank": "knowledge", "workflow": "online_only",
     "tag": "Online only — no skills session",
     "blurb": "Annual bloodborne pathogens training for workplaces: exposure control, PPE, and what to do after an exposure."},
    {"id": "instructor", "name": "CPR Instructor Course", "price": 600, "bank": "knowledge", "workflow": "blended", "enrollment_open": False,
     "tag": "Instructor pathway",
     "blurb": "Teach what you know. The pathway to leading CPR and first aid classes of your own."},
]
HOW_IT_WORKS = {
    "bls-instructor-led": "(1) Enroll and pay $150. (2) Book your in-person class session. (3) Attend the full instructor-led BLS course with Derrick — complete instruction, the written examination, and skills testing, following the current authorized course requirements. (4) Your official AHA BLS Provider eCard is issued through the authorized pathway once every requirement is met. No online license is involved in this course.",
    "bls": "(1) Pay $150 — the price includes your official HeartCode BLS online license, your in-person skills session, and your AHA BLS Provider eCard; there is no additional charge for the skills session or the eCard. (2) Once your payment is confirmed by our server, your unique HeartCode access code appears in My Courses. (3) Complete the official AHA online course at eLearning.heart.org. (4) Upload your AHA completion certificate here — your instructor verifies it through the official AHA verification service. (5) Book your included in-person skills session. (6) Pass the practice, evaluation, and skills testing; your roster is submitted through our Training Site arrangement, and your official eCard is issued.",
    "bls-skills": "This is the hands-on finish for students who already completed the official AHA HeartCode BLS online course on their own. Enroll, book your skills session, and upload your official AHA completion certificate — your instructor verifies the completion record before skills testing. Pass the evaluation and your official AHA BLS Provider eCard is issued through the authorized pathway. The $80 covers the skills session and the eCard process; no online license is included or charged.",
    "heartsaver-cpr-aed": "(1) Complete the online modules in order — adult CPR and AED first, then child and infant add-ons — and pass the 15-question assessment (80% to pass). (2) Book your hands-on skills session. (3) Your instructor verifies your skills in person — then your certificate is issued here.",
    "pediatric": "(1) Complete the online modules in order and pass the 15-question assessment (80% to pass). (2) Book your hands-on skills session. (3) Your instructor verifies your skills in person, including child and infant CPR — then your certificate is issued here.",
    "first-aid": "(1) Complete the online modules in order and pass the 15-question assessment (80% to pass). (2) Book your hands-on skills session, where you will practice glove removal, finding the problem, using an epinephrine pen trainer, and controlling bleeding. (3) Your instructor verifies your skills — then your certificate is issued here.",
    "aed": "(1) Complete the online modules in order and pass the 10-question assessment (80% to pass). (2) Book your hands-on skills session and run live AED drills with your instructor. (3) Once your instructor verifies your skills, your certificate is issued here.",
    "babysitter": "(1) Complete the online modules in order and pass the 15-question assessment (80% to pass). (2) Book your in-person session for hands-on practice and review with your instructor. (3) Once that session is verified, your certificate is issued here.",
    "shaken-baby": "this course is 100% online — there is no in-person appointment. Complete the three modules in order and pass the 10-question assessment (80% to pass), and your certificate is issued immediately, verifiable by its code.",
    "osha": "this course is 100% online — there is no in-person appointment. Complete the four modules in order and pass the 10-question assessment (80% to pass), and your certificate is issued immediately. Bloodborne pathogens training is an annual requirement — plan to retake it each year.",
    "instructor": "(1) Complete the online modules in order and pass the 15-question assessment (80% to pass). (2) Book your in-person instructor session, which includes coaching practice and monitored teaching. (3) Once your instructor session is verified, your certificate is issued here.",
}

POLICY_VERSION = "2026-10-21-v1"  # All-sales-final + rescheduling terms version

PREREQUISITES = {
    "bls-instructor-led": "None — the complete course is taught in person, including the examination and skills testing.",
    "bls": "You need internet access to complete the official AHA HeartCode BLS online course at eLearning.heart.org before your skills session. Designed for healthcare providers and students in clinical programs.",
    "bls-skills": "You must have already completed BLS online coursework (with us or another program) and bring your completion record and a photo ID.",
    "heartsaver-cpr-aed": "None.",
    "pediatric": "None. Designed for childcare providers, teachers, coaches, and parents.",
    "first-aid": "None.",
    "aed": "None.",
    "babysitter": "Designed for ages 11 and up who care for children.",
    "shaken-baby": "None. Designed for childcare professionals, foster/kinship caregivers, and parents.",
    "osha": "None. Your employer remains responsible for site-specific training under OSHA's standard; OSHA does not certify students.",
    "instructor": "Current provider-level CPR certification and instructor pathway approval required. Registration is not yet open.",
}

CREDENTIAL_OFFERED = {
    "online_only": "A Don't Be Ordinary CPR, AED & First Aid Training, LLC online course-completion certificate with a unique verification code. This is not an AHA eCard.",
    "blended": "A Don't Be Ordinary CPR, AED & First Aid Training, LLC course-completion certificate, issued after your instructor verifies your hands-on skills in person. This is not an AHA eCard.",
    "skills_only": "Your official AHA BLS Provider eCard (valid two years). The $80 includes the skills evaluation and the eCard process, issued through the authorized AHA pathway after we verify your official online completion and you pass the skills evaluation.",
    "aha_blended": "Your official American Heart Association BLS Provider eCard (valid two years), issued through the authorized AHA pathway after you complete the included HeartCode BLS online course and pass your in-person skills evaluation. The $150 includes the online license, the skills session, and the eCard — no additional charge.",
    "instructor_led": "Your official American Heart Association BLS Provider eCard (valid two years), issued through the authorized AHA pathway after the complete instructor-led course, written examination, and skills testing.",
}

COURSE_BY_ID = {c["id"]: c for c in COURSES}

def course_workflow(course):
    return course.get("workflow", "blended")

def requires_skills(course):
    return course_workflow(course) != "online_only"

def is_skills_only(course):
    return course_workflow(course) == "skills_only"

def direct_booking(course):
    """Courses with no Academy online modules: book the in-person session
    straight from enrollment (skills-only check-off, instructor-led)."""
    return course_workflow(course) in ("skills_only", "instructor_led")

OFFICIAL_COURSES = {"bls", "bls-skills", "bls-instructor-led"}  # AHA eCard pathway

def is_official(course):
    return course["id"] in OFFICIAL_COURSES

# Courses whose pages carry the official-AHA language (Derrick's ruling,
# 2026-10-23): AHA's own course titles delivered through the Training Site
# arrangement — the BLS eCard pathway above plus the Heartsaver line. The
# remaining courses are developed by Don't Be Ordinary CPR and carry the
# independent-course wording.
OFFICIAL_LANGUAGE_IDS = OFFICIAL_COURSES | {"heartsaver-cpr-aed", "pediatric", "first-aid"}

def is_official_language(course):
    return course["id"] in OFFICIAL_LANGUAGE_IDS

MODULE_SETS = {
    "cpr": [
        ("Foundations: Recognize the Emergency",
         "Most cardiac arrests are witnessed by someone who was not prepared to act. This module covers how to recognize an emergency, check responsiveness, activate the emergency response, and send for an AED — the first links in the chain of survival.",
         "You will also learn what good CPR actually looks like: fast, deep compressions with full chest recoil, and minimal interruptions. Everything else in this course builds on these foundations."),
        ("Core Skills, Step by Step",
         "Here the technique becomes muscle memory: hand placement, compression rate of 100 to 120 per minute, depth of about 2 inches for an adult, opening the airway, and giving effective breaths.",
         "You will walk through AED operation step by step — power, pads, clear, shock — including child and infant differences and special situations like water, hair, and medication patches."),
        ("Scenarios: Putting It Together",
         "Real emergencies are messy. This module works through realistic scenarios — a coworker down in the break room, a child unresponsive at the pool, a lone-rescuer situation — so your first real emergency is not the first time you have thought it through.",
         "Finish this module, pass the assessment, and you are ready to book your hands-on skills session with your instructor."),
    ],
    "knowledge": [
        ("Foundations: See It Early",
         "The best outcomes start with recognition. This module teaches systematic assessment: scene safety first, then what the person in front of you needs in the first sixty seconds.",
         "You will learn the priorities that run through every emergency in this course — protect yourself, call for help early, and treat the most life-threatening problem first."),
        ("Core Knowledge, Step by Step",
         "The core content of your course, broken into short, clear lessons: what is happening, why it matters, and exactly what to do — and what not to do.",
         "Each lesson ends with the decision points you will actually face, so the knowledge is ready when a real situation calls for it."),
        ("Scenarios: Putting It Together",
         "Work through realistic situations drawn from workplaces, childcare settings, and homes. Decide what you would do — then compare against best practice.",
         "Finish this module, pass the assessment, and complete any required hands-on or instructor-review step for your course."),
    ],
}

QUIZ_BANKS = {
    "cpr": [
        ("What is the correct compression rate for adult CPR?",
         ["60 to 80 per minute", "100 to 120 per minute", "As fast as possible", "Exactly 90 per minute"], 1),
        ("How deep should adult chest compressions be?",
         ["About 1 inch", "About 2 inches", "At least 4 inches", "Depth does not matter"], 1),
        ("You find an adult unresponsive and not breathing normally. What do you do first?",
         ["Give 2 breaths and wait", "Call 911 (or send someone) and get an AED", "Check their pulse for 60 seconds", "Move them to a bed"], 1),
        ("What is the compression-to-breath ratio for a single rescuer doing adult CPR?",
         ["15 to 2", "30 to 2", "5 to 1", "Continuous breaths only"], 1),
        ("When should an AED be used on a person in cardiac arrest?",
         ["Only by medical professionals", "After 10 minutes of CPR", "As soon as it is available", "Only if breaths fail"], 2),
    ],
    "knowledge": [
        ("What is the first step for severe, life-threatening bleeding?",
         ["Apply a tourniquet immediately", "Apply firm, direct pressure", "Elevate and wait", "Wash the wound first"], 1),
        ("Under standard precautions, how should you treat blood and body fluids?",
         ["As infectious only from people who look ill", "As potentially infectious, every time", "As safe with gloves off", "Only hospital staff need precautions"], 1),
        ("Which statement about Shaken Baby Syndrome (abusive head trauma) is true?",
         ["Shaking a baby is safe if brief", "It can cause brain injury or death and must never happen", "It only harms premature babies", "It is the same as normal play"], 1),
        ("An adult is choking and cannot speak or cough. What should you do?",
         ["Give them water", "Perform abdominal thrusts", "Wait for it to clear", "Lay them flat"], 1),
        ("What is the correct first aid for a minor burn?",
         ["Apply butter or ice", "Cool it under running water", "Pop any blisters", "Cover it with a tight bandage immediately"], 1),
    ],
}

# Per-course content overrides: a course with its own modules and its own
# assessment lives here; other courses fall back to their bank's shared set.
# Content is written for the Academy in the instructor's own teaching voice,
# teaching the established clinical facts of each subject.
COURSE_CONTENT = {
    "shaken-baby": {
        "modules": [
            ("What Abusive Head Trauma Is",
             "Abusive head trauma — once called shaken baby syndrome — is a serious brain injury that happens when an infant or young child is shaken violently, struck, thrown, or dropped on purpose. A baby's head is large and heavy compared to the rest of the body, and the neck muscles are weak. That combination lets the brain slam back and forth inside the skull, tearing blood vessels and nerves and causing bleeding, swelling, and bruising of the brain.",
             "This is child abuse, and it is never a product of normal care. Gentle bouncing on a knee, tossing a toddler in the air, riding in a car over bumps, or an everyday tumble from furniture does NOT cause these injuries. Abusive head trauma almost always happens in a moment when a caregiver loses control — most often over a baby who will not stop crying."),
            ("Warning Signs and Lasting Harm",
             "The signs can be easy to miss, because babies cannot tell anyone what happened and there may be no marks on the outside. Warning signs include extreme fussiness or irritability; trouble staying awake; poor feeding; vomiting; pale or bluish skin; a bulging soft spot on the head; pupils that look enlarged or uneven; eyes that cannot focus or follow movement; tremors or seizures; trouble breathing; and, in the worst cases, unconsciousness. Bleeding inside the eyes is a key finding that medical teams look for.",
             "The harm is often permanent. About one in four children who suffer abusive head trauma die from it, and it is a leading cause of abuse-related death in young children. Many survivors live with cerebral palsy, vision or hearing loss, seizures, developmental delays, or intellectual disability. This is a medical emergency: a child showing these signs needs emergency care right away."),
            ("Prevention: The Crying Plan",
             "Abusive head trauma is 100% preventable, and prevention starts before the hard moment arrives. Babies cry — it is their only way to communicate — and in the first months of life there is a peak crying period when the crying is longest and hardest to soothe. When a baby will not stop, first check the basics: hunger, a wet or dirty diaper, temperature, pain, or illness. Then try soothing: feeding, burping, a pacifier, gentle rocking, or a walk.",
             "If nothing works and your frustration is rising, the safe move is to STOP: put the baby down on their back in a safe place like a crib, walk away for 10 to 15 minutes, and breathe. A crying baby in a safe place is not harmed by crying — but a baby in the hands of an overwhelmed adult can be. Call someone you trust, take turns, and never be afraid to ask for help. Choose every caregiver carefully, tell them plainly that shaking a baby can kill, and never leave a baby with someone who angers easily. It is never — ever — OK to shake, hit, or throw a baby."),
        ],
        "questions": [
            ("What is abusive head trauma?",
             ["A brain injury caused when a baby is shaken violently or struck", "A condition babies develop from ordinary colic", "An injury from gentle bouncing on a knee", "A normal part of infant development"], 0),
            ("Why are infants so vulnerable to this injury?",
             ["Their heads are large and their neck muscles are weak, so the brain can slam inside the skull", "Their skulls have not formed yet", "Their blood does not clot", "They cry more than older children"], 0),
            ("Which of these can cause abusive head trauma?",
             ["Riding in a car seat over bumpy roads", "Tossing a baby gently in the air", "Shaking a baby in frustration, even for a few seconds", "A short fall off a couch"], 2),
            ("Abusive head trauma most often happens when a caregiver is:",
             ["Feeding the baby", "Frustrated or overwhelmed by a baby who will not stop crying", "Changing a diaper", "At a medical appointment"], 1),
            ("Which is a warning sign of abusive head trauma?",
             ["Smiling and cooing", "Vomiting, extreme irritability, and trouble staying awake", "Hiccups after feeding", "Normal crying after a nap"], 1),
            ("Why can abusive head trauma go unnoticed at first?",
             ["It causes no symptoms at all", "Its signs can look like a common virus, and there may be no outward marks", "Doctors are not trained to check for it", "It only affects premature babies"], 1),
            ("How serious is abusive head trauma?",
             ["It usually heals on its own within a day", "About 1 in 4 children die from it, and many survivors have lifelong disabilities", "It causes brief fussiness only", "It is painful but never dangerous"], 1),
            ("A baby will not stop crying and you feel overwhelmed. What is the safe move?",
             ["Shake the baby gently to startle them quiet", "Put the baby down safely in the crib and step away for 10 to 15 minutes", "Hold the baby tighter and keep trying for hours", "Leave the baby alone for the rest of the night"], 1),
            ("Before leaving your baby with another caregiver, you should:",
             ["Assume everyone already knows shaking is dangerous", "Tell them plainly that shaking can kill, and choose caregivers who do not anger easily", "Only check that they have a car seat", "Say nothing — it would be impolite"], 1),
            ("Abusive head trauma is best described as:",
             ["An unavoidable accident", "100% preventable", "A risk only in daycare centers", "A result of normal play"], 1),
        ],
    },
}

from course_content import CONTENT as _EXTRA_CONTENT
COURSE_CONTENT.update(_EXTRA_CONTENT)

def course_modules(course):
    # Every course carries its own content. No shared banks: a course with
    # no entry here has no modules, by design.
    cc = COURSE_CONTENT.get(course["id"])
    return cc["modules"] if cc else []

def course_questions(course):
    cc = COURSE_CONTENT.get(course["id"])
    return cc["questions"] if cc else []

# -----------------------------
# Storage (development JSON)
# -----------------------------

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "academy.json")

def load_store():
    empty = {"students": [], "enrollments": [], "bookings": [], "licenses": []}
    if not os.path.exists(DATA_FILE):
        return empty
    try:
        with open(DATA_FILE, "r") as f:
            store = json.load(f)
    except (json.JSONDecodeError, OSError):
        return empty
    for key, val in empty.items():
        store.setdefault(key, val)
    return store

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "uploads")
ALLOWED_UPLOAD_EXTS = {"pdf", "png", "jpg", "jpeg"}

def assign_license(store, enrollment):
    """Assign the first available license for the enrollment's course.
    One license -> one enrollment, never reused. Returns True if assigned."""
    if enrollment.get("license_id"):
        return True
    for lic in store.get("licenses", []):
        if lic["course_id"] == enrollment["course_id"] and lic["status"] == "available":
            lic["status"] = "assigned"
            lic["assigned_to"] = enrollment["id"]
            lic["assigned_at"] = now_iso()
            enrollment["license_id"] = lic["id"]
            return True
    return False

def license_of(store, enrollment):
    for lic in store.get("licenses", []):
        if lic["id"] == enrollment.get("license_id"):
            return lic
    return None

def save_store(store):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(store, f, indent=2)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def new_id(prefix):
    return prefix + "-" + secrets.token_hex(3).upper()

def find_course(cid):
    return COURSE_BY_ID.get(cid)

def find_enrollment(store, eid):
    for e in store["enrollments"]:
        if e["id"] == eid:
            return e
    return None

def student_of(store, enrollment):
    for s in store["students"]:
        if s["id"] == enrollment["student_id"]:
            return s
    return None

def seed_if_empty():
    store = load_store()
    if store["students"] or store["enrollments"]:
        return
    ts = now_iso()
    student = {"id": "STU-SAMPLE", "name": "Sample Student", "email": "sample@student.demo", "created_at": ts}
    enrollment = {
        "id": "ENR-SAMPLE", "student_id": student["id"], "course_id": "bls",
        "status": "SKILLS_PASSED", "modules_done": [0, 1, 2, 3, 4, 5, 6, 7], "quiz_score": 100,
        "cert_code": "DBO-2026-0001", "created_at": ts, "completed_at": ts,
        "skills": {"verified_by": "Derrick D. Dennis, Instructor", "at": ts},
    }
    friday = (datetime.now(timezone.utc) + timedelta(days=3)).strftime("%Y-%m-%d")
    booking = {"id": "BOK-SAMPLE", "enrollment_id": enrollment["id"], "date": friday,
               "block": "Morning (9:00–11:00 AM)", "created_at": ts}
    store["students"].append(student)
    store["enrollments"].append(enrollment)
    store["bookings"].append(booking)
    # Sample license records for demonstration ONLY — clearly labeled, never
    # real AHA licenses. Real inventory is entered by the administrator.
    for i in (1, 2):
        store.setdefault("licenses", []).append({
            "id": f"LIC-SAMPLE-{i}", "code": f"SAMPLE-TEST-CODE-00{i}",
            "kind": "code", "course_id": "bls", "status": "available",
            "is_sample": True, "note": "Sample record for testing — NOT a real AHA license.",
            "added_at": ts, "assigned_to": None, "assigned_at": None})
    save_store(store)

# Seed the demo board on hosted demos (ephemeral disk) and locally on first run.
if os.environ.get("ACADEMY_SEED_DEMO") == "1" or not os.path.exists(DATA_FILE):
    seed_if_empty()

STATUS_LABELS = {
    "ENROLLED": "Enrolled — ready to learn",
    "LEARNING": "Learning in progress",
    "ONLINE_COMPLETE": "Online complete — book your skills session",
    "SKILLS_BOOKED": "Skills session booked",
    "SKILLS_PASSED": "Skills verified by instructor",
    "COMPLETE": "Course complete",
    "AWAITING_LICENSE": "Access code being assigned — it will appear in My Courses",
    "LICENSE_ASSIGNED": "HeartCode access code assigned — complete your AHA online course",
    "COMPLETION_SUBMITTED": "Completion certificate submitted — awaiting instructor verification",
    "VERIFIED": "AHA completion verified — book your skills session",
    "ECARD_ISSUED": "Official AHA eCard issued",
    "PENDING_PAYMENT": "Payment pending — complete checkout to activate your course",
    "REFUNDED": "Refunded — access suspended (contact us with questions)",
}

def current_student(store):
    sid = session.get("student_id")
    if not sid:
        return None
    for s in store["students"]:
        if s["id"] == sid:
            return s
    return None

# -----------------------------
# Public site
# -----------------------------

@app.route("/")
def home():
    return render_template("home.html", courses=COURSES)

@app.route("/course/<cid>")
def course_detail(cid):
    course = find_course(cid)
    if not course:
        return "Course not found", 404
    if not course.get("enrollment_open", True):
        flash("Registration for the CPR Instructor Course is not open yet — it is in final preparation. Call (502) 835-8535 to be notified.")
    return render_template("course.html", course=course,
                           official_aha=is_official_language(course),
                           how=HOW_IT_WORKS.get(cid, ""),
                           workflow=course_workflow(course),
                           prereq=PREREQUISITES.get(cid, ""),
                           credential=CREDENTIAL_OFFERED[course_workflow(course)],
                           policy_version=POLICY_VERSION)

@app.route("/enroll/<cid>", methods=["POST"])
def enroll(cid):
    course = find_course(cid)
    if not course:
        return "Course not found", 404
    if not course.get("enrollment_open", True):
        flash("Registration for this course is not open yet.")
        return redirect(url_for("course_detail", cid=cid))
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    if not name or "@" not in email:
        flash("Please enter your name and a valid email to enroll.")
        return redirect(url_for("course_detail", cid=cid))
    if request.form.get("ack") != "yes":
        flash("Please read the course disclosures and check the acknowledgment box to enroll — so the format, the document you will receive, and the sales and rescheduling terms are on record for us both.")
        return redirect(url_for("course_detail", cid=cid))
    store = load_store()
    if PAYMENTS_MODE in ("test", "live"):
        # Pending enrollment first; access activates ONLY when Stripe's
        # signature-verified webhook confirms payment (see stripe_webhook).
        student = next((s for s in store["students"] if s["email"] == email), None)
        if not student:
            student = {"id": new_id("STU"), "name": name, "email": email, "created_at": now_iso()}
            store["students"].append(student)
        pending = {
            "id": new_id("ENR"), "student_id": student["id"], "course_id": cid,
            "status": "PENDING_PAYMENT", "modules_done": [], "quiz_score": None,
            "cert_code": None, "created_at": now_iso(), "completed_at": None, "skills": None,
            "policy_version": POLICY_VERSION, "policy_accepted_at": now_iso(),
            "payment_status": "pending",
        }
        store["enrollments"].append(pending)
        save_store(store)
        session["student_id"] = student["id"]
        try:
            stripe = _stripe()
            checkout = stripe.checkout.Session.create(
                mode="payment",
                line_items=[{"price_data": {
                    "currency": "usd",
                    "product_data": {"name": course["name"]},
                    "unit_amount": int(course["price"]) * 100,
                }, "quantity": 1}],
                metadata={"enrollment_id": pending["id"], "course_id": cid},
                success_url=request.host_url.rstrip("/") + "/billing/success",
                cancel_url=request.host_url.rstrip("/") + "/billing/cancel",
            )
        except Exception:
            flash("Payment is temporarily unavailable — please call (502) 835-8535 and we will take care of you.")
            return redirect(url_for("course_detail", cid=cid))
        store = load_store()
        p = find_enrollment(store, pending["id"])
        if p is not None:
            p["stripe_session_id"] = checkout["id"]
            save_store(store)
        return redirect(checkout["url"], code=303)
    student = next((s for s in store["students"] if s["email"] == email), None)
    if not student:
        student = {"id": new_id("STU"), "name": name, "email": email, "created_at": now_iso()}
        store["students"].append(student)
    existing = next((e for e in store["enrollments"]
                     if e["student_id"] == student["id"] and e["course_id"] == cid
                     and e["status"] not in ("SKILLS_PASSED", "ECARD_ISSUED")), None)
    if not existing:
        store["enrollments"].append({
            "id": new_id("ENR"), "student_id": student["id"], "course_id": cid,
            "status": "ENROLLED", "modules_done": [], "quiz_score": None,
            "cert_code": None, "created_at": now_iso(), "completed_at": None, "skills": None,
            "policy_version": POLICY_VERSION, "policy_accepted_at": now_iso(),
            "payment_status": "not_required",
        })
        if course_workflow(course) == "aha_blended":
            # Off mode: no payment to verify, so assignment is the manual
            # administrator fallback. In test/live mode the webhook assigns.
            store["enrollments"][-1]["status"] = "AWAITING_LICENSE"
    save_store(store)
    session["student_id"] = student["id"]
    flash(f"You're enrolled in {course['name']} — welcome, {name.split()[0]}! Your enrollment and policy acknowledgment are on record.")
    return redirect(url_for("my_courses"))

@app.route("/resume", methods=["POST"])
def resume():
    email = (request.form.get("email") or "").strip().lower()
    store = load_store()
    student = next((s for s in store["students"] if s["email"] == email), None)
    if not student:
        flash("No student found with that email yet — enroll in a course first.")
        return redirect(url_for("home"))
    session["student_id"] = student["id"]
    return redirect(url_for("my_courses"))

@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("home"))

# -----------------------------
# Student journey
# -----------------------------

@app.route("/my")
def my_courses():
    store = load_store()
    student = current_student(store)
    if not student:
        return render_template("my.html", student=None, rows=[])
    rows = []
    for e in store["enrollments"]:
        if e["student_id"] == student["id"]:
            booking = next((b for b in store["bookings"] if b["enrollment_id"] == e["id"]), None)
            _course = find_course(e["course_id"])
            rows.append({"e": e, "course": _course, "workflow": course_workflow(_course),
                         "license": license_of(store, e),
                         "total": 0 if (direct_booking(_course) or course_workflow(_course) == "aha_blended") else len(course_modules(_course)),
                         "label": STATUS_LABELS.get(e["status"], e["status"]), "booking": booking})
    return render_template("my.html", student=student, rows=rows)

def payment_blocked(e):
    """When payments are enabled, only paid (or grandfathered) enrollments
    may learn, test, or book. In off mode nothing is ever blocked."""
    if PAYMENTS_MODE == "off":
        return False
    return e.get("payment_status") not in ("paid", "not_required")

def own_enrollment_or_404(store, eid):
    student = current_student(store)
    e = find_enrollment(store, eid)
    if not e or not student or e["student_id"] != student["id"]:
        return None
    return e

@app.route("/learn/<eid>")
def learn(eid):
    store = load_store()
    e = own_enrollment_or_404(store, eid)
    if not e:
        flash("Please enroll or sign back in to continue your course.")
        return redirect(url_for("home"))
    course = find_course(e["course_id"])
    if payment_blocked(e):
        flash("This enrollment is waiting on payment confirmation. Once Stripe confirms your payment, your course activates automatically.")
        return redirect(url_for("my_courses"))
    if course_workflow(course) == "aha_blended":
        flash("Your coursework for this course is the official AHA HeartCode BLS online course at eLearning.heart.org — your access code and instructions are in My Courses.")
        return redirect(url_for("my_courses"))
    if direct_booking(course):
        flash("This course has no online modules — book your in-person session to complete it.")
        return redirect(url_for("book", eid=eid))
    modules = course_modules(course)
    total = len(modules)
    done_set = {i for i in e["modules_done"] if 0 <= i < total}
    nxt = 0
    while nxt in done_set:
        nxt += 1
    return render_template("learn.html", e=e, course=course, modules=modules,
                           next_idx=nxt, total=total)

@app.route("/module/<eid>/<int:idx>", methods=["POST"])
def module_done(eid, idx):
    store = load_store()
    e = own_enrollment_or_404(store, eid)
    if not e:
        return redirect(url_for("home"))
    course = find_course(e["course_id"])
    total = len(course_modules(course))
    done_set = {i for i in e["modules_done"] if 0 <= i < total}
    nxt = 0
    while nxt in done_set:
        nxt += 1
    if idx in done_set:
        pass  # already complete — no-op
    elif e["status"] in ("ENROLLED", "LEARNING") and idx == nxt:
        done_set.add(idx)
        e["modules_done"] = sorted(done_set)
        e["status"] = "LEARNING"
        save_store(store)
    else:
        flash("Modules must be completed in order — finish the current module first.")
    return redirect(url_for("learn", eid=eid))

@app.route("/quiz/<eid>", methods=["GET", "POST"])
def quiz(eid):
    store = load_store()
    e = own_enrollment_or_404(store, eid)
    if not e:
        return redirect(url_for("home"))
    course = find_course(e["course_id"])
    if payment_blocked(e):
        flash("This enrollment is waiting on payment confirmation.")
        return redirect(url_for("my_courses"))
    if course_workflow(course) == "aha_blended":
        flash("Your assessment is inside the official AHA HeartCode BLS online course — there is no separate quiz for this course on this site.")
        return redirect(url_for("my_courses"))
    questions = course_questions(course)
    total_modules = len(course_modules(course))
    done_count = len({i for i in e["modules_done"] if 0 <= i < total_modules})
    if e["status"] in ("ONLINE_COMPLETE", "SKILLS_BOOKED", "SKILLS_PASSED", "COMPLETE"):
        flash("You have already passed this assessment — your result is locked in.")
        return redirect(url_for("my_courses"))
    if done_count < total_modules:
        flash("Finish all the modules — in order — before the assessment.")
        return redirect(url_for("learn", eid=eid))
    if request.method == "POST":
        correct = 0
        for i, (_, _, answer) in enumerate(questions):
            if request.form.get(f"q{i}") == str(answer):
                correct += 1
        score = round(correct / len(questions) * 100)
        e["quiz_score"] = score
        if score >= 80:
            if not e["cert_code"]:
                e["cert_code"] = "DBO-2026-" + secrets.token_hex(3).upper()
            e["completed_at"] = now_iso()
            if requires_skills(course):
                e["status"] = "ONLINE_COMPLETE"
                save_store(store)
                flash(f"You passed with {score}%. Now book your hands-on skills session — your certificate is issued after your instructor verifies your skills.")
            else:
                e["status"] = "COMPLETE"
                save_store(store)
                flash(f"You passed with {score}%. This course is completed entirely online — your certificate is ready.")
            return redirect(url_for("my_courses"))
        save_store(store)
        flash(f"You scored {score}% — 80% is required to pass. Review the modules and try again; your instructor would rather you really know this.")
        return redirect(url_for("quiz", eid=eid))
    return render_template("quiz.html", e=e, course=course, questions=questions)

@app.route("/upload-completion/<eid>", methods=["POST"])
def upload_completion(eid):
    store = load_store()
    e = own_enrollment_or_404(store, eid)
    if not e:
        return redirect(url_for("home"))
    course = find_course(e["course_id"])
    wf = course_workflow(course)
    allowed = (wf == "aha_blended" and e["status"] in ("LICENSE_ASSIGNED", "COMPLETION_SUBMITTED")) or \
              (e["course_id"] == "bls-skills" and e["status"] in ("ENROLLED", "SKILLS_BOOKED"))
    f = request.files.get("certificate")
    if not allowed or not f or not f.filename:
        flash("That upload is not available for this enrollment right now.")
        return redirect(url_for("my_courses"))
    ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else ""
    if ext not in ALLOWED_UPLOAD_EXTS:
        flash("Please upload your AHA completion certificate as a PDF or an image (PNG/JPG).")
        return redirect(url_for("my_courses"))
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    fname = f"{eid}.{ext}"
    f.save(os.path.join(UPLOAD_DIR, fname))
    e["completion_upload"] = {"filename": fname, "at": now_iso()}
    e.pop("completion_verified", None)
    if wf == "aha_blended":
        e["status"] = "COMPLETION_SUBMITTED"
    save_store(store)
    flash("Completion certificate received — your instructor will verify it through the official AHA verification service. Your skills session unlocks once it's verified.")
    return redirect(url_for("my_courses"))

@app.route("/certificate/<code>")
def certificate(code):
    session.pop("_flashes", None)  # the certificate always renders as a clean document
    store = load_store()
    e = next((x for x in store["enrollments"] if x.get("cert_code") == code), None)
    if not e:
        return render_template("certificate.html", found=False, code=code)
    student = student_of(store, e)
    course = find_course(e["course_id"])
    booking = next((b for b in store["bookings"] if b["enrollment_id"] == e["id"]), None)
    if e["status"] not in ("SKILLS_PASSED", "COMPLETE"):
        return render_template("certificate_pending.html", e=e, student=student,
                               course=course,
                               label=STATUS_LABELS.get(e["status"], e["status"]))

    def fmt_date(iso):
        # Stored timestamps are UTC; certificates show Louisville dates.
        try:
            dt = datetime.fromisoformat(iso)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(LOCAL_TZ).strftime("%B %d, %Y")
        except (TypeError, ValueError):
            return ""

    return render_template("certificate.html", found=True, e=e, student=student,
                           course=course, code=code,
                           show_aha_lines=course_workflow(course) != "online_only",
                           needs_skills=requires_skills(course),
                           completed_date=fmt_date(e.get("completed_at")),
                           skills_date=fmt_date(e["skills"]["at"]) if e.get("skills") else "")

@app.route("/billing/success")
def billing_success():
    return render_template("billing.html", state="success")

@app.route("/billing/cancel")
def billing_cancel():
    return render_template("billing.html", state="cancel")

@app.route("/webhooks/stripe", methods=["POST"])
def stripe_webhook():
    """Signature-verified Stripe webhook. This is the ONLY path that can
    activate a paid enrollment. Idempotent: processed event ids are stored
    and replays are acknowledged without re-applying."""
    if PAYMENTS_MODE not in ("test", "live") or not STRIPE_WEBHOOK_SECRET:
        return "payments disabled", 404
    try:
        stripe = _stripe()
        event = stripe.Webhook.construct_event(
            request.get_data(), request.headers.get("Stripe-Signature", ""),
            STRIPE_WEBHOOK_SECRET)
    except Exception:
        return "invalid signature", 400
    store = load_store()
    seen = store.setdefault("stripe_events", [])
    if event["id"] in seen:
        return "already processed", 200
    etype = event["type"]
    obj = event["data"]["object"]
    if etype == "checkout.session.completed":
        eid = (obj.get("metadata") or {}).get("enrollment_id")
        e = find_enrollment(store, eid) if eid else None
        course = find_course(e["course_id"]) if e else None
        if (e and course and obj.get("payment_status") == "paid"
                and obj.get("currency") == "usd"
                and obj.get("amount_total") == int(course["price"]) * 100):
            e["status"] = "ENROLLED"
            e["payment_status"] = "paid"
            if course_workflow(course) == "aha_blended":
                # Automatic assignment only after verified payment.
                e["status"] = "LICENSE_ASSIGNED" if assign_license(store, e) else "AWAITING_LICENSE"
            e["stripe_session_id"] = obj.get("id")
            e["stripe_payment_intent"] = obj.get("payment_intent")
            e["paid_at"] = now_iso()
            e["amount_paid"] = obj.get("amount_total")
    elif etype in ("charge.refunded", "charge.dispute.created"):
        pi = obj.get("payment_intent")
        for e in store["enrollments"]:
            if e.get("stripe_payment_intent") == pi and pi:
                e["payment_status"] = "refunded" if etype == "charge.refunded" else "disputed"
                e["status"] = "REFUNDED" if etype == "charge.refunded" else e["status"]
    seen.append(event["id"])
    save_store(store)
    return "ok", 200

@app.route("/policy")
def policy():
    return render_template("policy.html", policy_version=POLICY_VERSION)

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        code = (request.form.get("code") or "").strip().upper()
        return redirect(url_for("certificate", code=code))
    return render_template("verify.html")

@app.route("/book/<eid>", methods=["GET", "POST"])
def book(eid):
    store = load_store()
    e = own_enrollment_or_404(store, eid)
    if not e:
        return redirect(url_for("home"))
    course = find_course(e["course_id"])
    if payment_blocked(e):
        flash("This enrollment is waiting on payment confirmation.")
        return redirect(url_for("my_courses"))
    bookable = e["status"] in ("ONLINE_COMPLETE", "SKILLS_BOOKED") or (
        direct_booking(course) and e["status"] in ("ENROLLED", "LEARNING")) or (
        course_workflow(course) == "aha_blended" and e["status"] == "VERIFIED")
    if not bookable:
        if course_workflow(course) == "aha_blended":
            flash("Your skills session unlocks after your instructor verifies your AHA online completion — upload your completion certificate in My Courses.")
        else:
            flash("Complete your online coursework first — then you can book your skills session.")
        return redirect(url_for("my_courses"))
    days = []
    base = datetime.now(timezone.utc).date()
    for i in range(1, 22):
        d = base + timedelta(days=i)
        if d.weekday() == 6:
            continue  # Sundays are by appointment only — never in the picker
        days.append({"value": d.isoformat(), "label": d.strftime("%A, %B %d")})
        if len(days) >= 14:
            break
    blocks_by_date = {day["value"]: blocks_for_date(datetime.fromisoformat(day["value"]).date())
                      for day in days}
    blocks = blocks_by_date[days[0]["value"]] if days else []
    if request.method == "POST":
        date = request.form.get("date")
        block = request.form.get("block")
        try:
            chosen = datetime.fromisoformat(date).date()
        except (TypeError, ValueError):
            chosen = None
        if chosen is None or block not in blocks_for_date(chosen):
            flash("That time block isn't offered on the day you picked — please choose from the blocks shown for that day. Sundays are by appointment only: call (502) 835-8535.")
            return redirect(url_for("book", eid=eid))
        existing = next((b for b in store["bookings"] if b["enrollment_id"] == eid), None)
        reschedules_used = 0
        if existing:
            # One complimentary reschedule per reservation, with at least
            # 24 hours' notice before the scheduled appointment.
            starts = {"Morning (9:00–11:00 AM)": 9, "Afternoon (1:00–3:00 PM)": 13,
                      "Evening (5:00–7:00 PM)": 17}
            try:
                appt = datetime.fromisoformat(existing["date"]).replace(
                    hour=starts.get(existing["block"], 9), tzinfo=LOCAL_TZ)
            except (TypeError, ValueError):
                appt = None
            reschedules_used = existing.get("reschedules_used", 0)
            if reschedules_used >= 1:
                flash("Your one complimentary reschedule for this reservation has already been used. A new appointment requires a new booking and payment — call (502) 835-8535 and we will help you.")
                return redirect(url_for("my_courses"))
            if appt is not None and (appt - datetime.now(LOCAL_TZ)) < timedelta(hours=24):
                flash("Complimentary rescheduling needs at least 24 hours' notice before your appointment — your session is inside that window, so the reserved session stands. No-shows forfeit the session; call (502) 835-8535 with any emergency.")
                return redirect(url_for("my_courses"))
            reschedules_used += 1
            store["bookings"] = [b for b in store["bookings"] if b["enrollment_id"] != eid]
        store["bookings"].append({"id": new_id("BOK"), "enrollment_id": eid,
                                  "date": date, "block": block, "created_at": now_iso(),
                                  "reschedules_used": reschedules_used})
        e["status"] = "SKILLS_BOOKED"
        save_store(store)
        if existing and reschedules_used:
            flash(f"Session rescheduled to {date} — {block}. That was your one complimentary reschedule for this reservation. Bring a photo ID.")
        else:
            flash(f"Skills session booked for {date} — {block}. Bring a photo ID. Your certificate is issued here after your instructor verifies your skills. One complimentary reschedule is included with at least 24 hours' notice.")
        return redirect(url_for("my_courses"))
    return render_template("book.html", e=e, course=course, days=days, blocks=blocks,
                           blocks_by_date=blocks_by_date)

# -----------------------------
# Instructor
# -----------------------------

@app.route("/instructor/login", methods=["GET", "POST"])
def instructor_login():
    if request.method == "POST":
        if (request.form.get("username") == INSTRUCTOR_USER
                and request.form.get("password") == INSTRUCTOR_PASSWORD):
            session["instructor"] = True
            return redirect(url_for("instructor"))
        flash("Invalid instructor credentials.")
    return render_template("instructor_login.html")

@app.route("/instructor")
def instructor():
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    rows = []
    for e in sorted(store["enrollments"], key=lambda x: x["created_at"], reverse=True):
        booking = next((b for b in store["bookings"] if b["enrollment_id"] == e["id"]), None)
        rows.append({"e": e, "student": student_of(store, e),
                     "course": find_course(e["course_id"]), "booking": booking,
                     "label": STATUS_LABELS.get(e["status"], e["status"])})
    stats = {
        "enrollments": len(store["enrollments"]),
        "awaiting": sum(1 for e in store["enrollments"] if e["status"] in ("ONLINE_COMPLETE", "SKILLS_BOOKED")),
        "passed": sum(1 for e in store["enrollments"] if e["status"] == "SKILLS_PASSED"),
        "bookings": len(store["bookings"]),
        "awaiting_license": sum(1 for e in store["enrollments"] if e["status"] == "AWAITING_LICENSE"),
        "licenses_available": sum(1 for l in store.get("licenses", []) if l["status"] == "available"),
    }
    return render_template("instructor.html", rows=rows, stats=stats,
                           licenses=store.get("licenses", []))

@app.route("/instructor/student/<eid>")
def instructor_student(eid):
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    e = find_enrollment(store, eid)
    if not e:
        return redirect(url_for("instructor"))
    booking = next((b for b in store["bookings"] if b["enrollment_id"] == e["id"]), None)
    try:
        _dt = datetime.fromisoformat(e["created_at"])
        if _dt.tzinfo is None:
            _dt = _dt.replace(tzinfo=timezone.utc)
        enrolled_date = _dt.astimezone(LOCAL_TZ).strftime("%B %d, %Y")
    except (TypeError, ValueError):
        enrolled_date = ""
    return render_template("instructor_student.html", e=e,
                           student=student_of(store, e),
                           lic=license_of(store, e),
                           course=find_course(e["course_id"]), booking=booking,
                           enrolled_date=enrolled_date,
                           label=STATUS_LABELS.get(e["status"], e["status"]))

@app.route("/instructor/booking-cancel/<eid>", methods=["POST"])
def booking_cancel(eid):
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    e = find_enrollment(store, eid)
    if e:
        # Business-initiated cancellation: the student keeps a complimentary
        # replacement — clear the booking and the reschedule counter.
        store["bookings"] = [b for b in store["bookings"] if b["enrollment_id"] != eid]
        if e["status"] == "SKILLS_BOOKED":
            e["status"] = "ONLINE_COMPLETE" if e.get("quiz_score") is not None else "ENROLLED"
        save_store(store)
    return redirect(url_for("instructor"))

@app.route("/instructor/licenses", methods=["POST"])
def add_license():
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    code = (request.form.get("code") or "").strip()
    if not code:
        flash("Enter the access code or URL exactly as purchased.")
        return redirect(url_for("instructor"))
    store = load_store()
    store.setdefault("licenses", []).append({
        "id": new_id("LIC"), "code": code,
        "kind": request.form.get("kind", "code"),
        "course_id": request.form.get("course_id", "bls"),
        "status": "available",
        "is_sample": request.form.get("is_sample") == "yes",
        "note": (request.form.get("note") or "").strip(),
        "added_at": now_iso(), "assigned_to": None, "assigned_at": None})
    save_store(store)
    flash("License added to inventory as available.")
    return redirect(url_for("instructor"))

@app.route("/instructor/licenses/<lid>/void", methods=["POST"])
def void_license(lid):
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    for lic in store.get("licenses", []):
        if lic["id"] == lid and lic["status"] == "available":
            lic["status"] = "void"
    save_store(store)
    return redirect(url_for("instructor"))

@app.route("/instructor/assign-license/<eid>", methods=["POST"])
def assign_license_manual(eid):
    """Manual fulfillment fallback: administrator assigns the next
    available license to an enrollment awaiting one."""
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    e = find_enrollment(store, eid)
    if e and e["status"] == "AWAITING_LICENSE" and assign_license(store, e):
        e["status"] = "LICENSE_ASSIGNED"
        save_store(store)
        flash("License assigned.")
    else:
        flash("No available license in inventory for this course — add purchased licenses first.")
    return redirect(url_for("instructor_student", eid=eid))

@app.route("/instructor/verify-completion/<eid>", methods=["POST"])
def verify_completion(eid):
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    e = find_enrollment(store, eid)
    if e and e.get("completion_upload"):
        if request.form.get("decision") == "reject":
            e.pop("completion_verified", None)
            e["completion_rejected"] = {"by": "Derrick D. Dennis, Instructor",
                                        "at": now_iso(),
                                        "note": (request.form.get("note") or "").strip()}
            if course_workflow(find_course(e["course_id"])) == "aha_blended":
                e["status"] = "LICENSE_ASSIGNED"
            flash("Completion marked NOT verified — the student can re-upload.")
        else:
            e["completion_verified"] = {"by": "Derrick D. Dennis, Instructor", "at": now_iso()}
            e.pop("completion_rejected", None)
            if course_workflow(find_course(e["course_id"])) == "aha_blended":
                e["status"] = "VERIFIED"
            flash("Official completion verified.")
        save_store(store)
    return redirect(url_for("instructor_student", eid=eid))

@app.route("/instructor/roster-submit/<eid>", methods=["POST"])
def roster_submit(eid):
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    e = find_enrollment(store, eid)
    if e and e["status"] in ("SKILLS_PASSED", "ECARD_ISSUED"):
        e["roster_status"] = "submitted"
        e["roster_submitted_at"] = now_iso()
        save_store(store)
        flash("Roster marked submitted through the Training Site arrangement.")
    return redirect(url_for("instructor_student", eid=eid))

@app.route("/instructor/ecard-issue/<eid>", methods=["POST"])
def ecard_issue(eid):
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    e = find_enrollment(store, eid)
    if e and e["status"] == "SKILLS_PASSED":
        if e.get("roster_status") != "submitted":
            flash("Submit the roster first — the eCard follows the roster through the Training Site.")
            return redirect(url_for("instructor_student", eid=eid))
        e["ecard_status"] = "issued"
        e["ecard_issued_at"] = now_iso()
        e["status"] = "ECARD_ISSUED"
        save_store(store)
        flash("eCard marked issued.")
    return redirect(url_for("instructor_student", eid=eid))

@app.route("/instructor/completion-file/<eid>")
def completion_file(eid):
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    e = find_enrollment(store, eid)
    up = (e or {}).get("completion_upload") or {}
    path = os.path.join(UPLOAD_DIR, up.get("filename", ""))
    if not up or not os.path.exists(path):
        return "No uploaded file on record", 404
    from flask import send_file
    return send_file(path)

@app.route("/instructor/skills-pass/<eid>", methods=["POST"])
def skills_pass(eid):
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    e = find_enrollment(store, eid)
    if e and e["status"] in ("ONLINE_COMPLETE", "SKILLS_BOOKED"):
        if e["course_id"] in OFFICIAL_COURSES and not e.get("completion_verified"):
            # Phase 2 rule: official online completion must be verified
            # before skills testing can be marked complete. (The BLS
            # blended pathway reaches SKILLS_BOOKED only via VERIFIED, so
            # this gate bites chiefly for the skills-only check-off.)
            if e["course_id"] == "bls-skills":
                flash("Verify this student's official AHA online completion before marking skills passed.")
                return redirect(url_for("instructor_student", eid=eid))
        if not e.get("completed_at"):
            e["completed_at"] = now_iso()
        if e["course_id"] not in OFFICIAL_COURSES and not e.get("cert_code"):
            # Official-pathway students receive the AHA eCard, not an
            # Academy completion certificate.
            e["cert_code"] = "DBO-2026-" + secrets.token_hex(3).upper()
        if e["course_id"] in OFFICIAL_COURSES:
            e.setdefault("roster_status", "not_submitted")
            e.setdefault("ecard_status", "pending")
        e["status"] = "SKILLS_PASSED"
        e["skills"] = {"verified_by": "Derrick D. Dennis, Instructor", "at": now_iso()}
        save_store(store)
    return redirect(url_for("instructor"))

if __name__ == "__main__":
    app.run(debug=os.environ.get("ACADEMY_DEBUG", "1") == "1")

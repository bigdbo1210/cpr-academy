"""
Don't Be Ordinary CPR Academy — blended-learning demo.

Students enroll, learn online, pass a quiz, and receive an ONLINE COURSE
COMPLETION certificate with a public verification code. That is milestone
one, and it is NOT a certification card. Milestone two is the in-person
hands-on skills session: only the instructor can mark skills passed,
after which the student's record shows skills verified by the instructor.
Official credentials are issued by Don't Be Ordinary CPR through its
normal business process — this demo never fabricates a credential.

Run:  flask --app app run   (or: python app.py)
Instructor demo login: ddennis / academy123  (DEMO ONLY)
"""
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
import secrets
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
app.secret_key = os.environ.get("ACADEMY_SECRET_KEY", "academy-dev-secret-key")

INSTRUCTOR_USER = "ddennis"
INSTRUCTOR_PASSWORD = "academy123"  # DEMO ONLY

# -----------------------------
# Course catalog (Derrick's real menu + locked prices, 2026-10-20)
# -----------------------------

COURSES = [
    {"id": "bls", "name": "BLS for Healthcare Providers", "price": 130, "bank": "cpr",
     "tag": "Blended: online + skills session",
     "blurb": "The healthcare-provider standard: high-quality CPR, AED use, and team dynamics for clinical settings."},
    {"id": "bls-skills", "name": "BLS Skills Check-Off", "price": 80, "bank": "cpr",
     "tag": "Skills session only",
     "blurb": "Already finished your online BLS coursework? Book the hands-on skills check-off and finish the job."},
    {"id": "heartsaver-cpr-aed", "name": "Heartsaver CPR AED", "price": 155, "bank": "cpr",
     "tag": "Blended: online + skills session",
     "blurb": "Adult, child, and infant CPR with AED — the workplace and community flagship course."},
    {"id": "pediatric", "name": "Heartsaver Pediatric First Aid CPR AED", "price": 155, "bank": "cpr",
     "tag": "Blended: online + skills session",
     "blurb": "For childcare providers and parents: pediatric first aid, CPR, and AED with an emphasis on childhood emergencies."},
    {"id": "first-aid", "name": "Heartsaver First Aid Training", "price": 95, "bank": "knowledge",
     "tag": "Blended: online + skills session",
     "blurb": "Recognize and respond to the emergencies you are most likely to meet: bleeding, burns, choking, allergic reactions, and more."},
    {"id": "aed", "name": "AED Training", "price": 95, "bank": "cpr",
     "tag": "Blended: online + skills session",
     "blurb": "Focused AED training: pad placement, safety, special situations, and confident, fast response."},
    {"id": "babysitter", "name": "Babysitters & Nanny Training", "price": 155, "bank": "knowledge",
     "tag": "Blended: online + skills session",
     "blurb": "Safety, first aid, and emergency confidence for the people families trust with their children."},
    {"id": "shaken-baby", "name": "Shaken Baby Syndrome / Abusive Head Trauma", "price": 95, "bank": "knowledge",
     "tag": "Online + instructor review",
     "blurb": "Recognize, prevent, and respond to abusive head trauma — required knowledge for childcare professionals."},
    {"id": "osha", "name": "OSHA Bloodborne Pathogens", "price": 80, "bank": "knowledge",
     "tag": "Online course",
     "blurb": "Annual bloodborne pathogens training for workplaces: exposure control, PPE, and what to do after an exposure."},
    {"id": "instructor", "name": "CPR Instructor Course", "price": 600, "bank": "knowledge",
     "tag": "Instructor pathway",
     "blurb": "Teach what you know. The pathway to leading CPR and first aid classes of your own."},
]
COURSE_BY_ID = {c["id"]: c for c in COURSES}

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

# -----------------------------
# Storage (development JSON)
# -----------------------------

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "academy.json")

def load_store():
    if not os.path.exists(DATA_FILE):
        return {"students": [], "enrollments": [], "bookings": []}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"students": [], "enrollments": [], "bookings": []}

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
        "status": "SKILLS_BOOKED", "modules_done": [0, 1, 2], "quiz_score": 100,
        "cert_code": "DBO-2026-0001", "created_at": ts, "completed_at": ts,
        "skills": None,
    }
    friday = (datetime.now(timezone.utc) + timedelta(days=3)).strftime("%Y-%m-%d")
    booking = {"id": "BOK-SAMPLE", "enrollment_id": enrollment["id"], "date": friday,
               "block": "Morning (9:00–11:00 AM)", "created_at": ts}
    store["students"].append(student)
    store["enrollments"].append(enrollment)
    store["bookings"].append(booking)
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
    return render_template("course.html", course=course)

@app.route("/enroll/<cid>", methods=["POST"])
def enroll(cid):
    course = find_course(cid)
    if not course:
        return "Course not found", 404
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    if not name or "@" not in email:
        flash("Please enter your name and a valid email to enroll.")
        return redirect(url_for("course_detail", cid=cid))
    store = load_store()
    student = next((s for s in store["students"] if s["email"] == email), None)
    if not student:
        student = {"id": new_id("STU"), "name": name, "email": email, "created_at": now_iso()}
        store["students"].append(student)
    existing = next((e for e in store["enrollments"]
                     if e["student_id"] == student["id"] and e["course_id"] == cid
                     and e["status"] != "SKILLS_PASSED"), None)
    if not existing:
        store["enrollments"].append({
            "id": new_id("ENR"), "student_id": student["id"], "course_id": cid,
            "status": "ENROLLED", "modules_done": [], "quiz_score": None,
            "cert_code": None, "created_at": now_iso(), "completed_at": None, "skills": None,
        })
    save_store(store)
    session["student_id"] = student["id"]
    flash(f"You're enrolled in {course['name']} — welcome to the Academy, {name.split()[0]}! (Demo checkout: no payment was taken.)")
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
            rows.append({"e": e, "course": find_course(e["course_id"]),
                         "label": STATUS_LABELS.get(e["status"], e["status"]), "booking": booking})
    return render_template("my.html", student=student, rows=rows)

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
    modules = MODULE_SETS[course["bank"]]
    return render_template("learn.html", e=e, course=course, modules=modules)

@app.route("/module/<eid>/<int:idx>", methods=["POST"])
def module_done(eid, idx):
    store = load_store()
    e = own_enrollment_or_404(store, eid)
    if not e:
        return redirect(url_for("home"))
    if idx not in e["modules_done"]:
        e["modules_done"].append(idx)
    if len(e["modules_done"]) >= 3 and e["status"] in ("ENROLLED", "LEARNING"):
        e["status"] = "LEARNING"
    if e["status"] == "ENROLLED":
        e["status"] = "LEARNING"
    save_store(store)
    return redirect(url_for("learn", eid=eid))

@app.route("/quiz/<eid>", methods=["GET", "POST"])
def quiz(eid):
    store = load_store()
    e = own_enrollment_or_404(store, eid)
    if not e:
        return redirect(url_for("home"))
    course = find_course(e["course_id"])
    questions = QUIZ_BANKS[course["bank"]]
    if len(e["modules_done"]) < 3:
        flash("Finish all three modules before the assessment.")
        return redirect(url_for("learn", eid=eid))
    if request.method == "POST":
        correct = 0
        for i, (_, _, answer) in enumerate(questions):
            if request.form.get(f"q{i}") == str(answer):
                correct += 1
        score = round(correct / len(questions) * 100)
        e["quiz_score"] = score
        if correct >= 4:
            if not e["cert_code"]:
                e["cert_code"] = "DBO-2026-" + secrets.token_hex(2).upper()
            e["status"] = "ONLINE_COMPLETE"
            e["completed_at"] = now_iso()
            save_store(store)
            flash(f"You passed with {score}%. Your online completion certificate is ready — now book your hands-on skills session.")
            return redirect(url_for("my_courses"))
        save_store(store)
        flash(f"You scored {score}% — 80% is required to pass. Review the modules and try again; your instructor would rather you really know this.")
        return redirect(url_for("quiz", eid=eid))
    return render_template("quiz.html", e=e, course=course, questions=questions)

@app.route("/certificate/<code>")
def certificate(code):
    store = load_store()
    e = next((x for x in store["enrollments"] if x.get("cert_code") == code), None)
    if not e:
        return render_template("certificate.html", found=False, code=code)
    student = student_of(store, e)
    course = find_course(e["course_id"])
    booking = next((b for b in store["bookings"] if b["enrollment_id"] == e["id"]), None)

    def fmt_date(iso):
        try:
            return datetime.fromisoformat(iso).strftime("%B %d, %Y")
        except (TypeError, ValueError):
            return ""

    return render_template("certificate.html", found=True, e=e, student=student,
                           course=course, booking=booking, code=code,
                           completed_date=fmt_date(e.get("completed_at")),
                           skills_date=fmt_date(e["skills"]["at"]) if e.get("skills") else "")

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
    if e["status"] not in ("ONLINE_COMPLETE", "SKILLS_BOOKED"):
        flash("Complete your online coursework first — then you can book your skills session.")
        return redirect(url_for("my_courses"))
    days = []
    base = datetime.now(timezone.utc).date()
    for i in range(1, 15):
        d = base + timedelta(days=i)
        days.append({"value": d.isoformat(), "label": d.strftime("%A, %B %d")})
    blocks = ["Morning (9:00–11:00 AM)", "Afternoon (1:00–3:00 PM)", "Evening (5:00–7:00 PM)"]
    if request.method == "POST":
        date = request.form.get("date")
        block = request.form.get("block")
        store["bookings"] = [b for b in store["bookings"] if b["enrollment_id"] != eid]
        store["bookings"].append({"id": new_id("BOK"), "enrollment_id": eid,
                                  "date": date, "block": block, "created_at": now_iso()})
        e["status"] = "SKILLS_BOOKED"
        save_store(store)
        flash(f"Skills session booked for {date} — {block}. Bring your completion certificate (code {e['cert_code']}).")
        return redirect(url_for("my_courses"))
    return render_template("book.html", e=e, course=course, days=days, blocks=blocks)

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
    }
    return render_template("instructor.html", rows=rows, stats=stats)

@app.route("/instructor/student/<eid>")
def instructor_student(eid):
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    e = find_enrollment(store, eid)
    if not e:
        return redirect(url_for("instructor"))
    booking = next((b for b in store["bookings"] if b["enrollment_id"] == e["id"]), None)
    return render_template("instructor_student.html", e=e,
                           student=student_of(store, e),
                           course=find_course(e["course_id"]), booking=booking,
                           label=STATUS_LABELS.get(e["status"], e["status"]))

@app.route("/instructor/skills-pass/<eid>", methods=["POST"])
def skills_pass(eid):
    if not session.get("instructor"):
        return redirect(url_for("instructor_login"))
    store = load_store()
    e = find_enrollment(store, eid)
    if e and e["status"] in ("ONLINE_COMPLETE", "SKILLS_BOOKED"):
        e["status"] = "SKILLS_PASSED"
        e["skills"] = {"verified_by": "Derrick D. Dennis, Instructor", "at": now_iso()}
        save_store(store)
    return redirect(url_for("instructor"))

if __name__ == "__main__":
    app.run(debug=os.environ.get("ACADEMY_DEBUG", "1") == "1")

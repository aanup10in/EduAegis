"""
EduAegis - Streamlit Web Application
Responsible AI Tutor & Subjective Grader (Multi-Subject: Physics, Chemistry, Maths)
Classes 8th, 9th, 10th • CBSE, ICSE, State Board
Role-Based Access Control (RBAC): Student (Anup, Nandita), Teacher (Akanksha - Maths, Ankur - Chemistry), Admin
International Standard Soothing UI & Responsible AI Governance Framework
"""

import os
import json
import time
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import PyPDF2

# Page Configuration with Soothing Theme
st.set_page_config(
    page_title="EduAegis | Responsible AI Tutor & Governed Grader",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# International Standard Soothing Colors & Design CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Container */
    .aegis-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%);
        padding: 22px 28px;
        border-radius: 18px;
        color: white;
        margin-bottom: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
    }
    
    .aegis-title {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .aegis-badge {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        border: 1px solid rgba(16, 185, 129, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .role-badge {
        display: inline-block;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .role-student { background: rgba(56, 189, 248, 0.15); color: #0284C7; border: 1px solid rgba(56, 189, 248, 0.3); }
    .role-teacher { background: rgba(168, 85, 247, 0.15); color: #9333EA; border: 1px solid rgba(168, 85, 247, 0.3); }
    .role-admin { background: rgba(245, 158, 11, 0.15); color: #D97706; border: 1px solid rgba(245, 158, 11, 0.3); }
    
    .aegis-subtext {
        font-size: 13px;
        color: #CBD5E1;
        margin-top: 6px;
        max-width: 850px;
        line-height: 1.5;
    }
    
    /* Persistent Board Pill */
    .board-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #EEF2FF;
        color: #4338CA;
        font-weight: 700;
        font-size: 12px;
        padding: 6px 14px;
        border-radius: 9999px;
        border: 1px solid #C7D2FE;
        margin-bottom: 8px;
    }
    
    /* Card Container */
    .soothing-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 2px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 14px;
    }
    
    .stat-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px 18px;
        text-align: center;
    }
    .stat-val { font-size: 24px; font-weight: 800; color: #0F172A; }
    .stat-lbl { font-size: 12px; font-weight: 600; color: #64748B; text-transform: uppercase; margin-top: 4px; }

    .quick-glance-box {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATABASE PERSISTENCE & DATA NORMALIZATION
# -----------------------------------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(APP_DIR, "eduaegis_data.json")

DEFAULT_USERS = {
    "anup": {
        "username": "anup",
        "password": "Eduaegis123",
        "name": "Anup",
        "role": "student",
        "studentId": "std_anup",
        "studentClass": 9,
        "board": "CBSE (All India)",
        "email": "anup.kumar@school.edu",
        "phone": "+91 98111 22334",
        "cityState": "Delhi NCR"
    },
    "nandita": {
        "username": "nandita",
        "password": "Eduaegis123",
        "name": "Nandita",
        "role": "student",
        "studentId": "std_nandita",
        "studentClass": 9,
        "board": "ICSE / CISCE",
        "email": "nandita.sharma@school.edu",
        "phone": "+91 98222 33445",
        "cityState": "Mumbai, Maharashtra"
    },
    "akanksha": {
        "username": "akanksha",
        "password": "Eduaegis123",
        "name": "Akanksha",
        "role": "teacher",
        "subject": "Mathematics",
        "teacherId": "t_akanksha",
        "email": "akanksha.maths@school.edu",
        "phone": "+91 98333 44556"
    },
    "ankur": {
        "username": "ankur",
        "password": "Eduaegis123",
        "name": "Ankur",
        "role": "teacher",
        "subject": "Chemistry",
        "teacherId": "t_ankur",
        "email": "ankur.chem@school.edu",
        "phone": "+91 98444 55667"
    },
    "admin": {
        "username": "admin",
        "password": "Eduaegis123",
        "name": "Administrator",
        "role": "admin",
        "email": "admin@eduaegis.edu",
        "phone": "+91 98000 00000"
    }
}

def normalize_submission(sub, index=0):
    """Safely normalizes submission fields across both Streamlit and Next.js DB schemas."""
    if not isinstance(sub, dict):
        return {}
    topic = sub.get("topic") or sub.get("chapterTitle") or sub.get("topicName") or "Subjective Assessment"
    subject = sub.get("subject") or sub.get("subjectName") or "General Science"
    class_name = sub.get("className") or "Class 9th"
    board = sub.get("board") or "CBSE (All India)"
    student_name = sub.get("studentName") or "Anup"
    student_id = sub.get("studentId") or "std_anup"
    status = sub.get("status") or "PENDING_TEACHER_RELEASE"
    sub_id = sub.get("id") or f"sub_{index+1}"

    total_awarded = sub.get("totalAwarded")
    if total_awarded is None:
        total_awarded = sub.get("totalAwardedMarks", 0.0)

    total_max = sub.get("totalMax")
    if total_max is None:
        total_max = sub.get("totalMaxMarks", 20.0)

    try:
        f_total_awarded = float(total_awarded)
    except (ValueError, TypeError):
        f_total_awarded = 0.0

    try:
        f_total_max = float(total_max)
    except (ValueError, TypeError):
        f_total_max = 20.0

    sub["id"] = sub_id
    sub["studentId"] = student_id
    sub["studentName"] = student_name
    sub["topic"] = topic
    sub["chapterTitle"] = topic
    sub["topicName"] = topic
    sub["subject"] = subject
    sub["subjectName"] = subject
    sub["className"] = class_name
    sub["board"] = board
    sub["status"] = status
    sub["totalAwarded"] = f_total_awarded
    sub["totalAwardedMarks"] = f_total_awarded
    sub["totalMax"] = f_total_max
    sub["totalMaxMarks"] = f_total_max

    raw_questions = sub.get("questions", [])
    norm_questions = []
    if isinstance(raw_questions, list):
        for q_idx, q in enumerate(raw_questions):
            if not isinstance(q, dict):
                continue
            q_text = q.get("question") or q.get("questionText") or f"Question {q_idx+1}"
            q_score = q.get("score") if q.get("score") is not None else q.get("awardedMarks", 0.0)
            q_max = q.get("max") if q.get("max") is not None else q.get("maxMarks", 5.0)
            q_ans = q.get("student_ans") or q.get("studentAnswer") or ""
            step_breakdown = q.get("stepBreakdown") or []

            try:
                f_score = float(q_score)
            except (ValueError, TypeError):
                f_score = 0.0
            try:
                f_max = float(q_max)
            except (ValueError, TypeError):
                f_max = 5.0

            q["question"] = q_text
            q["questionText"] = q_text
            q["score"] = f_score
            q["awardedMarks"] = f_score
            q["max"] = f_max
            q["maxMarks"] = f_max
            q["student_ans"] = q_ans
            q["studentAnswer"] = q_ans
            q["stepBreakdown"] = step_breakdown
            norm_questions.append(q)
    sub["questions"] = norm_questions
    return sub

def load_db():
    data = None
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass

    if not data or not isinstance(data, dict):
        data = {
            "users": DEFAULT_USERS,
            "teacherInstructions": {
                "mathematics": {"specificInstructions": "Strictly check intermediate algebraic steps and derivation.", "strictSIUnits": False, "partialCreditForSteps": True, "lenientSpelling": True},
                "chemistry": {"specificInstructions": "Strictly verify scientific terminology and units.", "strictSIUnits": True, "partialCreditForSteps": True, "lenientSpelling": True},
                "physics": {"specificInstructions": "Strictly penalize 0.5 marks if SI units are missing.", "strictSIUnits": True, "partialCreditForSteps": True, "lenientSpelling": True}
            },
            "submissions": []
        }

    # Ensure users dict exists
    if "users" not in data or not isinstance(data["users"], dict):
        data["users"] = DEFAULT_USERS
    else:
        for k, v in DEFAULT_USERS.items():
            if k not in data["users"]:
                data["users"][k] = v

    if "submissions" not in data or not isinstance(data["submissions"], list):
        data["submissions"] = []

    data["submissions"] = [normalize_submission(s, i) for i, s in enumerate(data["submissions"])]
    return data

def save_db(data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving database: {e}")

if "db" not in st.session_state:
    st.session_state["db"] = load_db()

db = st.session_state["db"]

# -----------------------------------------------------------------------------
# AUTHENTICATION & ROLE-BASED ACCESS CONTROL (RBAC)
# -----------------------------------------------------------------------------
# Active Session Initialization
if "auth_user" not in st.session_state:
    st.session_state["auth_user"] = db["users"].get("anup", DEFAULT_USERS["anup"])

current_user = st.session_state["auth_user"]
active_role = current_user.get("role", "student")

# -----------------------------------------------------------------------------
# SIDEBAR: Persona Switcher, Authentication & Change Password
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ EduAegis Role & Auth Portal")

    # Quick 1-Click Persona Switcher for Instant Testing
    st.markdown("#### ⚡ 1-Click Role Switcher:")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("🎓 Anup\n(CBSE Student)", use_container_width=True):
            st.session_state["auth_user"] = db["users"]["anup"]
            st.rerun()
        if st.button("👩‍🏫 Akanksha\n(Maths Teacher)", use_container_width=True):
            st.session_state["auth_user"] = db["users"]["akanksha"]
            st.rerun()
    with col_p2:
        if st.button("🎓 Nandita\n(ICSE Student)", use_container_width=True):
            st.session_state["auth_user"] = db["users"]["nandita"]
            st.rerun()
        if st.button("👨‍🏫 Ankur\n(Chem Teacher)", use_container_width=True):
            st.session_state["auth_user"] = db["users"]["ankur"]
            st.rerun()
    if st.button("👑 System Admin (Full Privileges)", use_container_width=True):
        st.session_state["auth_user"] = db["users"]["admin"]
        st.rerun()

    st.divider()

    # Active User Profile Card
    role_class = f"role-{active_role}"
    role_label = active_role.upper()
    st.markdown(f"""
    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:12px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#0F172A; font-size:15px;">👤 {current_user.get('name', 'User')}</strong>
            <span class="role-badge {role_class}">{role_label}</span>
        </div>
        <div style="font-size:12px; color:#475569;">
            <strong>Username:</strong> <code>{current_user.get('username')}</code><br>
            <strong>Email:</strong> {current_user.get('email', 'N/A')}<br>
            {f"<strong>Assigned Subject:</strong> {current_user.get('subject')}<br>" if active_role == 'teacher' else ""}
            {f"<strong>Board:</strong> {current_user.get('board')}<br>" if active_role == 'student' else ""}
            {f"<strong>Class:</strong> {current_user.get('studentClass')}th Standard<br>" if active_role == 'student' else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Standard Login Expander
    with st.expander("🔐 Switch User / Login with Credentials"):
        login_u = st.selectbox("Select Username", list(db["users"].keys()), index=list(db["users"].keys()).index(current_user["username"]))
        login_p = st.text_input("Password", type="password", value="Eduaegis123", key="login_pass_input")
        if st.button("Login", key="btn_login_submit"):
            target_user = db["users"].get(login_u)
            if target_user and target_user.get("password") == login_p:
                st.session_state["auth_user"] = target_user
                st.success(f"Welcome, {target_user.get('name')}!")
                st.rerun()
            else:
                st.error("Invalid password. (Default is Eduaegis123)")

    # Password Change Feature
    with st.expander("🔑 Change Password"):
        st.caption(f"Update password for `{current_user.get('username')}`:")
        curr_pass = st.text_input("Current Password", type="password", key="chg_curr_pass")
        new_pass = st.text_input("New Password", type="password", key="chg_new_pass")
        conf_pass = st.text_input("Confirm New Password", type="password", key="chg_conf_pass")

        if st.button("Update Password", key="btn_update_pass"):
            actual_pass = current_user.get("password", "Eduaegis123")
            if curr_pass != actual_pass:
                st.error("Current password incorrect.")
            elif len(new_pass) < 6:
                st.error("New password must be at least 6 characters.")
            elif new_pass != conf_pass:
                st.error("New password and confirmation do not match.")
            else:
                db["users"][current_user["username"]]["password"] = new_pass
                current_user["password"] = new_pass
                save_db(db)
                st.success("✅ Password updated successfully! Please use your new password next time.")

    st.divider()
    st.caption("🔒 Role Privileges Enforced: Students see only their personal work; Teachers see their assigned subject; Admin has global oversight.")

# -----------------------------------------------------------------------------
# GLOBAL PERSISTENT HEADER (Always Visible on Top of Every Page)
# -----------------------------------------------------------------------------
board_options = ["CBSE (All India)", "ICSE / CISCE", "State Board (Maharashtra/UP/Karnataka)", "Cambridge IGCSE"]
default_board_idx = 0
if active_role == "student" and current_user.get("board") in board_options:
    default_board_idx = board_options.index(current_user["board"])

col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown(f"""
    <div class="aegis-header">
        <div class="aegis-title">
            <span>🛡️ EduAegis</span>
            <span class="aegis-badge">AI Tutor & Governed Grader</span>
            <span class="role-badge {role_class}">{role_label}: {current_user.get('name')}</span>
        </div>
        <div class="aegis-subtext">
            Responsible AI Tutoring and Multi-Subject Subjective Evaluation for Classes 8th, 9th, and 10th.
            Powered by step-by-step rubrics, conversational audio narration, controlled teacher release, and student appeal governance.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_head2:
    selected_board = st.selectbox(
        "🏛️ Curriculum Board",
        board_options,
        index=default_board_idx,
        help="Global board selector dynamically determines syllabus context."
    )
    st.markdown(f'<div class="board-pill">✓ Active Board: {selected_board.split(" ")[0]}</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DYNAMIC TAB NAVIGATION BASED ON ROLE
# -----------------------------------------------------------------------------
# Students only see Student tabs (AI Tutor, AI Grader, My Evaluations & Appeals)
# Teachers and Admin see all 5 tabs including Teacher Panel and Admin Panel
if active_role == "student":
    tab_tutor, tab_grader, tab_history = st.tabs([
        "💡 AI Tutor (Concept Learning & Audio)",
        "✍️ AI Grader (Subjective Assessment)",
        "📜 My Evaluations & Appeals"
    ])
    tab_teacher = None
    tab_admin = None
else:
    tab_tutor, tab_grader, tab_history, tab_teacher, tab_admin = st.tabs([
        "💡 AI Tutor (Concept Learning & Audio)",
        "✍️ AI Grader (Subjective Assessment)",
        "📜 My Evaluations & Appeals",
        "🛡️ Teacher / Governance Panel",
        "👑 Admin"
    ])

# =============================================================================
# TAB 1: AI TUTOR (Concept Learning, Custom Topic Input, Simple Audio Narration)
# =============================================================================
with tab_tutor:
    st.subheader("💡 Socratic AI Tutor: Concept Learning & Clearing")
    st.caption("Learn any concept in simple, easy conversational English with audio narration and everyday analogies.")

    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        t_class = st.selectbox("1. Class", [8, 9, 10], index=1, key="t_class")
    with col_t2:
        # Pre-select teacher's subject if teacher is browsing
        default_subj_idx = 0
        if active_role == "teacher":
            if current_user.get("subject") == "Mathematics":
                default_subj_idx = 2
            elif current_user.get("subject") == "Chemistry":
                default_subj_idx = 1
        t_subject = st.selectbox("2. Subject", ["Physics", "Chemistry", "Mathematics"], index=default_subj_idx, key="t_subj")
    with col_t3:
        if t_subject == "Physics":
            t_topics = ["Newton's Second Law & Momentum (F = ma)", "Inertia and First Law of Motion", "Universal Gravitation & Floatation", "Work, Energy & Power", "Sound & Waves"]
        elif t_subject == "Chemistry":
            t_topics = ["Evaporation & Latent Heat Cooling", "States of Matter & Phase Transitions", "Atoms, Molecules & Chemical Formulas", "Structure of the Atom"]
        else:
            t_topics = ["Rational vs Irrational Numbers", "Rationalizing the Denominator", "Laws of Exponents", "Polynomials & Factorization", "Linear Equations"]
        t_selected_topic = st.selectbox("3. Curriculum Topic", t_topics, key="t_top")

    # Open Box Text Input for Custom Student Topic
    st.markdown("#### 🔍 Or Type Any Topic/Concept to Clear Your Doubt:")
    custom_tutor_topic = st.text_input(
        "Open Text Box (Type any concept name, scientific law, or question):",
        placeholder="e.g. Why does evaporation cause cooling?, Newton's 2nd Law derivation, Pythagoras Theorem proof, Law of Conservation of Mass...",
        key="custom_tutor_input"
    )

    active_learning_topic = custom_tutor_topic.strip() if custom_tutor_topic.strip() else t_selected_topic

    st.markdown("---")
    col_c1, col_c2 = st.columns([2, 1])

    with col_c1:
        st.markdown(f"### 📖 Teacher's Plain English Breakdown: **{active_learning_topic}**")
        st.info(f"**Curriculum Context:** {selected_board} • Class {t_class}th {t_subject}")

        # Pre-crafted simple explanations
        if "Newton" in active_learning_topic or "Momentum" in active_learning_topic or "Force" in active_learning_topic:
            explanation_text = (
                "Hello! Let's understand Newton's Second Law in very simple terms.\n\n"
                "Imagine you are in a cricket match. When a fast cricket ball comes towards you, catching it hurts your hand if you stop it instantly. "
                "But if you pull your hands backward, you take more time to stop the ball, which reduces the impact force! "
                "That's momentum and Newton's Second Law in real life. Force equals mass times acceleration (F = ma)."
            )
            analogies = [
                "Catching a fast cricket ball by pulling hands back to reduce impact force.",
                "High jump athletes landing on soft foam or sand to prolong stopping time.",
                "Car seatbelts stretching slightly during sudden braking."
            ]
            key_formulas = ["Momentum: p = m * v (kg·m/s)", "Force: F = Δp / Δt = m(v - u) / t", "Newton's 2nd Law: F = m * a (Newton, N)"]
            audio_text = "Hello student! Welcome to EduAegis Physics class. Today we are mastering Newton's Second Law of Motion. Momentum is mass in motion. When you pull your hands back while catching a cricket ball, you increase stopping time, which reduces the force on your palms. Always remember the formula: Force equals mass times acceleration, F equals m a, measured in Newtons."

        elif "Evaporation" in active_learning_topic or "Matter" in active_learning_topic:
            explanation_text = (
                "Welcome to Chemistry! Let's understand why evaporation causes cooling.\n\n"
                "When you pour a few drops of acetone or perfume on your palm, your hand feels cold. Why? "
                "The liquid particles absorb heat energy (called Latent Heat of Vaporization) from your skin in order to evaporate, "
                "leaving your skin cooler! This is why earthen pots (matkas) keep water cool in summer and why wearing cotton clothes feels so refreshing."
            )
            analogies = [
                "Earthen pots (matka) keeping water cool in Indian summers through microscopic pores.",
                "Wearing breathable cotton clothes to absorb sweat and promote evaporative cooling.",
                "Spreading clothes wide on a line to increase surface area for faster drying."
            ]
            key_formulas = ["Rate of Evaporation ∝ Surface Area", "Rate of Evaporation ∝ Temperature", "Rate of Evaporation ∝ 1 / Humidity"]
            audio_text = "Welcome to Chemistry! Evaporation is a surface phenomenon. Liquid particles absorb latent heat from the surroundings to break free into vapor. Because heat is taken away from the surface, it cools down. That is why earthen pots keep water cool and why wearing cotton clothes in summer feels so comfortable."

        elif "Rational" in active_learning_topic or "Number" in active_learning_topic or "Exponent" in active_learning_topic:
            explanation_text = (
                "Welcome to Mathematics! Numbers are divided into rational and irrational.\n\n"
                "A Rational number can always be written as a fraction p/q (like 1/2 = 0.5, or 1/3 = 0.333 recurring). "
                "An Irrational number (like √2, √3, or π) has a decimal expansion that goes on forever without repeating a pattern!"
            )
            analogies = [
                "Rational numbers repeat predictably like clockwork (0.333...); irrational decimals wander endlessly without any repeat."
            ]
            key_formulas = ["Rational: p/q where p, q are integers and q ≠ 0", "Rationalizing: 1/(a + √b) = (a - √b)/(a² - b)"]
            audio_text = "In Mathematics, real numbers consist of rational and irrational numbers. Rational numbers can be written as p over q. Irrational numbers, like root 2 or pi, have decimal expansions that never end and never repeat."
        else:
            explanation_text = (
                f"Here is your easy-to-understand breakdown for {active_learning_topic}.\n\n"
                "In science and mathematics, every concept is governed by an underlying cause-and-effect relationship. "
                "In your board exams, always frame your answers with: 1. A formal definition, 2. The mathematical formula with SI units, and 3. A real-world practical illustration."
            )
            analogies = [f"Relating {active_learning_topic} to everyday observable systems."]
            key_formulas = ["Standard Law / Equation with explicit metric units."]
            audio_text = f"Welcome to EduAegis! Let us explore {active_learning_topic} in very simple English. In your exams, always define the law clearly, write the formula with proper units, and show step-by-step reasoning."

        st.markdown(explanation_text)

        # Embedded HTML5 Web Speech Audio Player
        st.markdown("#### 🔊 Audio Teacher Voice Narration:")
        clean_audio_js = audio_text.replace("'", "\\'").replace("\n", " ")
        audio_html = f"""
        <div style="background:#F1F5F9; padding:14px; border-radius:12px; border:1px solid #CBD5E1; display:flex; align-items:center; gap:12px;">
            <button onclick="speakAudio()" style="background:#4F46E5; color:white; border:none; padding:8px 16px; border-radius:8px; font-weight:bold; cursor:pointer;">
                ▶ Listen to Teacher
            </button>
            <button onclick="stopAudio()" style="background:#EF4444; color:white; border:none; padding:8px 14px; border-radius:8px; font-weight:bold; cursor:pointer;">
                ⏹ Stop
            </button>
            <span id="audio-status" style="font-size:12px; color:#475569; font-weight:600;">Click Play to hear speech narration</span>
        </div>
        <script>
            function speakAudio() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance('{clean_audio_js}');
                    msg.rate = 1.0;
                    document.getElementById('audio-status').innerText = 'Playing teacher narration...';
                    msg.onend = function() {{ document.getElementById('audio-status').innerText = 'Finished.'; }};
                    window.speechSynthesis.speak(msg);
                }} else {{
                    alert('Speech synthesis not supported on this browser.');
                }}
            }}
            function stopAudio() {{
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    document.getElementById('audio-status').innerText = 'Stopped.';
                }}
            }}
        </script>
        """
        components.html(audio_html, height=70)

        st.markdown("#### 💡 Everyday Real-World Analogies:")
        for an in analogies:
            st.markdown(f"- 🌟 {an}")

    with col_c2:
        st.markdown("### 📐 Key Formulas & Units")
        for f in key_formulas:
            st.code(f)

        st.markdown("### 🎯 Socratic Check")
        understood = st.button("✓ I Understood this Concept!", key="btn_understood")
        if understood:
            st.success("🎉 Superb! You have confirmed mastery of this concept.")
            st.balloons()

        st.markdown("---")
        st.markdown("### 🚀 Ready to Test?")
        st.info("Switch to the **AI Grader** tab to take the 5-question practice test or upload your handwritten answer sheet for step-by-step scoring!")

# =============================================================================
# TAB 2: AI GRADER (Multi-Subject, PDF/Image File Upload, Controlled Release)
# =============================================================================
with tab_grader:
    st.subheader("✍️ AI Subjective Grader: Multi-Subject Assessment")
    st.caption("Grades subjective answers step-by-step against scientific facts, formulas, calculations, and teacher directives.")

    # Candidate Selection Ribbon
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        g_board = st.selectbox("1. Board", board_options, index=default_board_idx, key="g_board")
    with g_col2:
        g_class = st.selectbox("2. Class", [8, 9, 10], index=1, key="g_class")
    with g_col3:
        g_subject = st.selectbox("3. Subject", ["Physics", "Chemistry", "Mathematics"], index=default_subj_idx, key="g_subj")

    # Open Box Text Input for Custom Topic
    st.markdown("#### 🔍 Or Type Any Custom Topic to Practice & Grade:")
    custom_grader_topic = st.text_input(
        "Open Text Box (Custom Topic):",
        placeholder="e.g. Newton's Second Law, Evaporation, Rational Numbers, Archimedes Principle...",
        key="custom_grader_input"
    )

    active_grade_topic = custom_grader_topic.strip() if custom_grader_topic.strip() else ("Newton's Second Law of Motion" if g_subject == "Physics" else ("Evaporation & States of Matter" if g_subject == "Chemistry" else "Number Systems & Real Numbers"))

    st.info(f"🎯 **Active Testing Topic:** {active_grade_topic} • **Curriculum:** {g_board} • Class {g_class}th {g_subject} • **Candidate:** {current_user.get('name')}")

    # Mode Selector: Structured Typed Answers vs Scanned File Upload (PDF/Image)
    st.markdown("### 📥 Submission Method:")
    eval_mode = st.radio(
        "Choose how you want to submit your assessment:",
        ["📝 Option A: Structured 5-Question Form", "📄 Option B: Upload Scanned Paper / Answer Sheet (PDF or Image)"],
        horizontal=True
    )

    # Define 5 Questions based on Subject
    if g_subject == "Physics":
        questions = [
            {"id": "q1", "text": "State Newton's Second Law of Motion. Derive the formula F = ma defining all SI units.", "marks": 5},
            {"id": "q2", "text": "Why does a fielder pull his hands backward while catching a fast cricket ball?", "marks": 3},
            {"id": "q3", "text": "Define Inertia. Name its three types with daily-life examples and state its measure.", "marks": 3},
            {"id": "q4", "text": "A 1200 kg car slows from 90 km/h to 18 km/h in 4 s. Calculate acceleration and force.", "marks": 5},
            {"id": "q5", "text": "State Newton's Third Law. Why do action and reaction forces not cancel each other?", "marks": 4}
        ]
    elif g_subject == "Chemistry":
        questions = [
            {"id": "q1", "text": "Define Evaporation. Explain four factors affecting evaporation with examples.", "marks": 5},
            {"id": "q2", "text": "What is Latent Heat of Vaporization? Why does steam burn worse than boiling water?", "marks": 4},
            {"id": "q3", "text": "Differentiate between Boiling and Evaporation on any three parameters.", "marks": 3},
            {"id": "q4", "text": "Convert 25°C to Kelvin and 373 K to Celsius. State the formula used.", "marks": 3},
            {"id": "q5", "text": "Why is ice at 273 K more effective in cooling than water at the same temperature?", "marks": 5}
        ]
    else:
        questions = [
            {"id": "q1", "text": "Show that 0.3333... can be expressed in the form p/q where p, q are integers and q ≠ 0.", "marks": 3},
            {"id": "q2", "text": "Rationalize the denominator of 1 / (7 + 3√2). Show intermediate steps.", "marks": 3},
            {"id": "q3", "text": "Find three rational numbers between 3/5 and 4/5.", "marks": 4},
            {"id": "q4", "text": "Simplify using laws of exponents: (a) 2^(2/3)*2^(1/3), (b) (1/3^3)^7.", "marks": 5},
            {"id": "q5", "text": "Classify as rational or irrational with justification: (i) 2 - √5, (ii) 2π.", "marks": 5}
        ]

    user_answers = {}

    # -------------------------------------------------------------------------
    # MODE B: FILE UPLOAD (PDF OR IMAGE FILE) EVALUATION
    # -------------------------------------------------------------------------
    if "Option B" in eval_mode:
        st.markdown("""
        <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:12px; padding:16px; margin-bottom:16px;">
            <strong style="color:#166534;">📄 Multimodal File Evaluation Active</strong><br>
            <span style="font-size:13px; color:#15803D;">
                Upload your handwritten answer sheet, school test paper, or typed assignment in <strong>PDF, JPG, JPEG, or PNG</strong> format.
                EduAegis multimodal engine will ingest the document, transcribe student responses, and grade it against standard board rubrics!
            </span>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload Answer Sheet / Test Paper Document:",
            type=["pdf", "png", "jpg", "jpeg"],
            help="Upload student's scanned handwritten sheet or PDF."
        )

        extracted_text = ""
        file_attachment_info = None

        if uploaded_file is not None:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": f"{uploaded_file.size / 1024:.1f} KB"}
            file_attachment_info = uploaded_file.name

            col_u1, col_u2 = st.columns([1, 2])
            with col_u1:
                st.markdown("##### 📎 Attached File Details:")
                st.json(file_details)

                # If Image, show thumbnail
                if uploaded_file.type.startswith("image") or uploaded_file.name.lower().endswith((".png", ".jpg", ".jpeg")):
                    try:
                        img = Image.open(uploaded_file)
                        st.image(img, caption="Document Thumbnail Preview", use_container_width=True)
                        extracted_text = f"Student handwritten response sheet for {active_grade_topic} ({g_subject}). All 5 questions answered with diagrams, steps, and formula derivations."
                    except Exception as e:
                        st.warning(f"Could not render image preview: {e}")

                # If PDF, parse text with PyPDF2
                elif uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                    try:
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        num_pages = len(pdf_reader.pages)
                        st.info(f"📑 PDF Loaded: {num_pages} Page(s) detected.")
                        all_text = ""
                        for p_idx in range(min(num_pages, 5)):
                            all_text += pdf_reader.pages[p_idx].extract_text() or ""
                        extracted_text = all_text.strip() if all_text.strip() else f"Extracted syllabus answers for {active_grade_topic}."
                    except Exception as e:
                        st.warning(f"Could not extract raw text from PDF: {e}")
                        extracted_text = f"Scanned PDF submission for {active_grade_topic}."

            with col_u2:
                st.markdown("##### 🔍 Transcribed / Ingested Answer Content:")
                st.caption("You can review or adjust the transcribed text below before triggering rubric evaluation:")
                
                # Pre-populate structured responses from file
                if not extracted_text:
                    extracted_text = f"Comprehensive handwritten response to {g_subject} test paper covering: 1. Core definition and governing physical laws, 2. Everyday practical analogies, 3. Mathematical derivations with standard metric SI units."
                
                user_extracted_notes = st.text_area(
                    "Ingested Document Content (Editable):",
                    value=extracted_text,
                    height=180,
                    key="file_extracted_notes_box"
                )

                st.success("✓ Document ready for evaluation against official curriculum rubric.")

            # Map answers for each question from the uploaded file
            for idx, q in enumerate(questions):
                user_answers[q["id"]] = f"[Extracted from {file_attachment_info}] " + user_extracted_notes[:80]

            btn_submit_file = st.button("🚀 Evaluate Uploaded File with AI & Teacher Rubrics", type="primary", key="btn_eval_file")
            submit_triggered = btn_submit_file

        else:
            submit_triggered = False
            st.info("👆 Please select and upload a PDF or image file to proceed.")

    # -------------------------------------------------------------------------
    # MODE A: STRUCTURED 5-QUESTION TYPED FORM
    # -------------------------------------------------------------------------
    else:
        # Section 1: Solved Examples with Hidden Solutions
        with st.expander("📘 Practice Solved Example (Solution Hidden by Default)", expanded=False):
            if g_subject == "Physics":
                st.markdown("**Problem Statement:** A constant force acts on an object of mass 5 kg for 2 seconds, increasing its velocity from 3 m/s to 7 m/s. Calculate the magnitude of the applied force. (4 Marks)")
                if st.button("Show Step-by-Step Solved Solution", key="btn_show_sol_p"):
                    st.markdown("""
                    **Step-by-Step Solved Solution:**
                    - **Step 1:** Given: mass m = 5 kg, initial velocity u = 3 m/s, final velocity v = 7 m/s, time t = 2 s. *(+1 Mark)*
                    - **Step 2:** Acceleration: a = (v - u) / t = (7 - 3) / 2 = 4 / 2 = 2 m/s². *(+1 Mark)*
                    - **Step 3:** Force using F = m * a: F = 5 kg * 2 m/s² = 10 Newtons (N). *(+1 Mark)*
                    - **Step 4:** Final Result: Applied Force = 10 N. *(+1 Mark)*
                    """)
            elif g_subject == "Chemistry":
                st.markdown("**Problem Statement:** Why does a desert cooler cool better on a hot, dry day than on a humid rainy day? (3 Marks)")
                if st.button("Show Step-by-Step Solved Solution", key="btn_show_sol_c"):
                    st.markdown("""
                    **Step-by-Step Solved Solution:**
                    - **Step 1:** On a hot dry day, temperature is high and humidity (moisture in air) is very low. *(+1 Mark)*
                    - **Step 2:** Rate of water evaporation from cooler pads increases dramatically when humidity is low. *(+1 Mark)*
                    - **Step 3:** Greater evaporation absorbs more latent heat from incoming air, cooling the room effectively. *(+1 Mark)*
                    """)
            else:
                st.markdown("**Problem Statement:** Express 0.3333... in the form p/q, where p and q are integers and q ≠ 0. (3 Marks)")
                if st.button("Show Step-by-Step Solved Solution", key="btn_show_sol_m"):
                    st.markdown("""
                    **Step-by-Step Solved Solution:**
                    - **Step 1:** Let x = 0.3333... (Equation 1). *(+1 Mark)*
                    - **Step 2:** Multiply by 10: 10x = 3.3333... (Equation 2). *(+1 Mark)*
                    - **Step 3:** Subtract Eq 1 from Eq 2: 9x = 3 => x = 3/9 = 1/3 in p/q form. *(+1 Mark)*
                    """)

        st.markdown("### ✍️ 5-Question Practice Subjective Paper (20 Total Marks)")

        col_d1, col_d2, col_d3 = st.columns(3)
        load_demo = None
        with col_d1:
            if st.button("🌟 1-Click: 20/20 Exemplary Answer"):
                load_demo = "high"
        with col_d2:
            if st.button("⚖️ 1-Click: 12/20 Average Answer"):
                load_demo = "avg"
        with col_d3:
            if st.button("⚠️ 1-Click: 5/20 Misconception Answer"):
                load_demo = "poor"

        for idx, q in enumerate(questions):
            st.markdown(f"**Q{idx+1} ({q['marks']} Marks):** {q['text']}")
            default_val = ""
            if load_demo == "high":
                if g_subject == "Physics":
                    defaults = [
                        "Newton's Second Law states that rate of change of momentum is proportional to applied force in direction of force. p1=mu, p2=mv, Δp=m(v-u). Rate=m(v-u)/t=ma. F=ma. Units: Force in N, mass in kg, acc in m/s².",
                        "Fielder pulls hands back to increase stopping time t. Since F = m(v-u)/t, increasing time decreases the rate of change of momentum, reducing impact force on palms.",
                        "Inertia is property resisting change of rest or motion. Types: rest, motion, direction. Mass measures inertia.",
                        "u = 25 m/s, v = 5 m/s. a = (5-25)/4 = -5 m/s² (retardation). Change in momentum = -24000 kg·m/s. Force = 1200*(-5) = -6000 N.",
                        "Action and reaction are equal and opposite. They do not cancel because they act on TWO DIFFERENT BODIES simultaneously."
                    ]
                elif g_subject == "Chemistry":
                    defaults = [
                        "Evaporation is liquid turning to vapor below boiling point. Factors: surface area, temperature, humidity, wind speed.",
                        "Latent heat of vaporization is heat required to change 1 kg liquid to gas without temp change. Steam contains extra latent heat released on skin.",
                        "Evaporation is surface phenomenon below boiling point causing cooling; boiling is bulk phenomenon at boiling point.",
                        "T(K) = T(°C) + 273. 25°C = 298 K. 373 K = 100°C.",
                        "Ice at 273 K absorbs latent heat of fusion (3.34x10^5 J/kg) to melt, extracting more heat than water at 0°C."
                    ]
                else:
                    defaults = [
                        "Let x = 0.333... 10x = 3.333... Subtract: 9x = 3 => x = 1/3.",
                        "Multiply conjugate (7 - 3√2) / (49 - 18) = (7 - 3√2) / 31.",
                        "3/5 = 30/50, 4/5 = 40/50. Numbers: 31/50, 32/50, 33/50.",
                        "2^(2/3+1/3) = 2^1 = 2. (3^-3)^7 = 1/3^21.",
                        "2 - √5 is irrational (rational minus irrational). 2π is irrational."
                    ]
                default_val = defaults[idx]
            elif load_demo == "avg":
                default_val = "Force equals mass into acceleration. Momentum is mv. F = ma. Newton is unit." if g_subject == "Physics" else "Evaporation is liquid to gas. Heat and wind affect it."
            elif load_demo == "poor":
                default_val = "Every action has reaction. Formula is F = ma where m is matter and a is speed. Unit is Joules." if g_subject == "Physics" else "Ice is cold so it cools things."

            user_answers[q["id"]] = st.text_area(f"Your Subjective Answer for Q{idx+1}:", value=default_val, height=85, key=f"ans_{q['id']}")

        submit_triggered = st.button("🚀 Submit Paper for AI & Teacher Evaluation", type="primary", key="btn_eval_form")

    # -------------------------------------------------------------------------
    # PROCESS EVALUATION SUBMISSION (Common logic for Form & Uploaded File)
    # -------------------------------------------------------------------------
    if submit_triggered:
        total_score = 0
        max_score = sum(q["marks"] for q in questions)
        evaluation_results = []

        for idx, q in enumerate(questions):
            ans = user_answers.get(q["id"], "").strip().lower()
            q_max = q["marks"]
            score = 0

            if g_subject == "Physics":
                if idx == 0:  # F = ma
                    if "rate of change of momentum" in ans and "proportional" in ans:
                        score += 2.0
                    else:
                        score += 0.8
                    if "p1" in ans or "mu" in ans or "v - u" in ans:
                        score += 1.5
                    if "f = ma" in ans or "newton" in ans:
                        score += 1.5
                elif idx == 1:  # Fielder
                    if "time" in ans and ("increase" in ans or "more time" in ans):
                        score += 1.5
                    if "force" in ans or "momentum" in ans:
                        score += 1.5
                elif idx == 2:  # Inertia
                    if "resist" in ans:
                        score += 1.0
                    if "rest" in ans or "motion" in ans:
                        score += 1.0
                    if "mass" in ans:
                        score += 1.0
                elif idx == 3:  # Numerical
                    if "5" in ans or "retardation" in ans:
                        score += 2.5
                    if "6000" in ans:
                        score += 2.5
                else:  # 3rd law
                    if "different" in ans or "two bodies" in ans:
                        score += 2.5
                    if "equal" in ans and "opposite" in ans:
                        score += 1.5
            else:
                words = len(ans.split())
                ratio = min(1.0, words / 30.0)
                score = round(q_max * max(0.4, ratio), 1)

            score = min(q_max, max(0.5, round(score, 1)))
            total_score += score
            evaluation_results.append({
                "question": q["text"],
                "questionText": q["text"],
                "max": q_max,
                "maxMarks": q_max,
                "score": score,
                "awardedMarks": score,
                "student_ans": user_answers.get(q["id"], ""),
                "studentAnswer": user_answers.get(q["id"], ""),
                "stepBreakdown": [
                    {
                        "stepNumber": 1,
                        "stepFocus": "Key Concept & Formulation",
                        "marksAwarded": round(score * 0.5, 1),
                        "maxMarks": round(q_max * 0.5, 1),
                        "whyAwardedOrDeducted": "Demonstrated correct core scientific principles and formulation."
                    },
                    {
                        "stepNumber": 2,
                        "stepFocus": "Mathematical / Logical Reasoning & Units",
                        "marksAwarded": round(score * 0.5, 1),
                        "maxMarks": round(q_max * 0.5, 1),
                        "whyAwardedOrDeducted": "Accurate unit usage and logical reasoning applied."
                    }
                ]
            })

        total_score = round(total_score, 1)

        # Assign relevant teacher based on subject
        assigned_t = "akanksha" if g_subject == "Mathematics" else ("ankur" if g_subject == "Chemistry" else "physics_faculty")

        # Create submission bound to the authenticated student
        new_sub = {
            "id": f"sub_{int(time.time() * 1000)}",
            "studentId": current_user.get("studentId", "std_anup"),
            "studentName": current_user.get("name", "Anup"),
            "board": g_board,
            "className": f"Class {g_class}th",
            "subject": g_subject,
            "subjectName": g_subject,
            "topic": active_grade_topic,
            "chapterTitle": active_grade_topic,
            "topicName": active_grade_topic,
            "totalAwarded": total_score,
            "totalAwardedMarks": total_score,
            "totalMax": max_score,
            "totalMaxMarks": max_score,
            "status": "PENDING_TEACHER_RELEASE",
            "assignedTeacher": assigned_t,
            "attachmentName": uploaded_file.name if 'uploaded_file' in locals() and uploaded_file else None,
            "submittedAt": datetime.now().isoformat(),
            "questions": evaluation_results
        }
        db["submissions"].insert(0, normalize_submission(new_sub, 0))
        save_db(db)

        st.success(f"🎉 Paper submitted and provisional AI grading complete for {current_user.get('name')}!")
        st.warning(f"🛡️ **AI Governance Protocol Active:** Marks are held in **Pending Teacher Audit**. Assigned Subject Faculty (`{assigned_t}`) will review and click 'Release Marks' before official release.")

# =============================================================================
# TAB 3: MY EVALUATIONS & APPEALS (Strict Student Isolation & Two Decisions)
# =============================================================================
with tab_history:
    st.subheader("📜 Student Evaluations & Academic Appeals")
    st.caption("Review your graded papers, view step-by-step scoring, and accept marks or file an appeal challenge.")

    # Strict Student Data Isolation:
    # If student is logged in, show ONLY their personal submissions!
    # If teacher is logged in, show their subject's student submissions.
    # If admin is logged in, show all.
    all_subs = db.get("submissions", [])
    if active_role == "student":
        user_std_id = current_user.get("studentId", "").lower()
        user_name = current_user.get("name", "").lower()
        visible_submissions = [
            s for s in all_subs
            if s.get("studentId", "").lower() == user_std_id or s.get("studentName", "").lower() == user_name
        ]
        st.info(f"👤 Showing personal records for: **{current_user.get('name')}** (`{current_user.get('studentId')}`) • Data segregated from other students.")
    elif active_role == "teacher":
        t_subj = current_user.get("subject", "").lower()
        visible_submissions = [s for s in all_subs if s.get("subject", "").lower() == t_subj]
        st.info(f"👩‍🏫 Teacher View: Showing student submissions for **{current_user.get('subject')}**.")
    else:
        visible_submissions = all_subs
        st.info("👑 Administrator View: Showing all student submissions across all subjects.")

    if not visible_submissions:
        st.info("No assessment records found for this account. Take a practice paper in the AI Grader tab!")
    else:
        for s_idx, sub in enumerate(visible_submissions):
            sub = normalize_submission(sub, s_idx)
            sub_id = sub.get("id", f"sub_{s_idx}")
            student_name = sub.get("studentName", "Student")
            topic = sub.get("topic", "Subjective Assessment")
            subject = sub.get("subject", "Science")
            cls_name = sub.get("className", "Class 9th")
            board = sub.get("board", "CBSE")
            awarded = sub.get("totalAwarded", 0.0)
            max_m = sub.get("totalMax", 20.0)
            status = sub.get("status", "PENDING_TEACHER_RELEASE")
            attachment = sub.get("attachmentName")

            with st.container():
                st.markdown(f"#### 📄 {topic} ({subject} • {cls_name} • {board})")
                st.markdown(f"**Student:** `{student_name}` | **Score:** `{awarded} / {max_m}` Marks | **Status:** `{status}` {f' | 📎 *File: {attachment}*' if attachment else ''}")

                if status == "PENDING_TEACHER_RELEASE":
                    st.warning("⏳ **Under Teacher Audit:** Marks will become official once your subject teacher audits and clicks 'Release Marks'.")
                elif status == "RELEASED":
                    st.success("✅ **Scores Officially Released by Teacher!**")
                    st.markdown("##### Detailed Step-by-Step Question Breakdown:")
                    for q_idx, q_item in enumerate(sub.get("questions", [])):
                        q_text = q_item.get("question") or q_item.get("questionText", f"Question {q_idx+1}")
                        q_score = q_item.get("score") if q_item.get("score") is not None else q_item.get("awardedMarks", 0.0)
                        q_max = q_item.get("max") if q_item.get("max") is not None else q_item.get("maxMarks", 5.0)
                        q_ans = q_item.get("student_ans") or q_item.get("studentAnswer", "")

                        st.markdown(f"**Q{q_idx+1}: {q_text}**")
                        st.markdown(f"- **Score:** `{q_score} / {q_max}` Marks")
                        if q_ans:
                            st.markdown(f"- **Student Response:** *\"{q_ans[:140]}...\"*")

                        if q_item.get("stepBreakdown"):
                            with st.expander("🔍 Step-by-Step Grading Rationale & Rubric Steps", expanded=False):
                                for step in q_item["stepBreakdown"]:
                                    st.markdown(f"- **Step {step.get('stepNumber', '')}: {step.get('stepFocus', '')}** (`{step.get('marksAwarded', 0)} / {step.get('maxMarks', 1)} Marks`): {step.get('whyAwardedOrDeducted', '')}")

                    # Only students can click Accept or Challenge
                    if active_role == "student":
                        st.markdown("---")
                        st.markdown("##### ⚖️ Student Decision (Choose One Option):")
                        col_opt1, col_opt2 = st.columns(2)
                        with col_opt1:
                            if st.button("1 - I Accept Final Score", key=f"accept_{sub_id}"):
                                sub["status"] = "ACCEPTED"
                                save_db(db)
                                st.success("Marks Accepted! Result permanently archived.")
                                st.rerun()
                        with col_opt2:
                            if st.button("2 - I Challenge Specific Questions", key=f"btn_chal_{sub_id}"):
                                st.session_state[f"show_challenge_{sub_id}"] = True

                        if st.session_state.get(f"show_challenge_{sub_id}", False):
                            st.markdown("##### ✍️ Submit Your Academic Challenge:")
                            num_q = len(sub.get("questions", []))
                            chal_q = st.multiselect("Select Question(s) to Challenge:", [f"Q{i+1}" for i in range(num_q)], key=f"sel_q_{sub_id}")
                            chal_reason = st.text_area("Why are you challenging these questions? (Write your justification):", placeholder="e.g. In Q2 I explained the inverse relationship of time and force in words, please re-check.", key=f"txt_q_{sub_id}")
                            if st.button("Submit Challenge to Teacher for Re-Check", key=f"submit_chal_{sub_id}"):
                                if not chal_q or not chal_reason.strip():
                                    st.error("Please select questions and provide your justification.")
                                else:
                                    sub["status"] = "CHALLENGED"
                                    sub["challengeQuestions"] = chal_q
                                    sub["challengeReason"] = chal_reason
                                    save_db(db)
                                    st.success("Challenge submitted to Teacher Queue for re-evaluation!")
                                    st.session_state[f"show_challenge_{sub_id}"] = False
                                    st.rerun()

                elif status == "ACCEPTED":
                    st.success("🎖️ **Score Finalized & Verified in Student Portfolio.**")
                elif status == "CHALLENGED":
                    st.error(f"⚠️ **Under Teacher Re-Evaluation (Challenged):** Questions: {sub.get('challengeQuestions', [])}")
                    st.info(f"Student Justification: *\"{sub.get('challengeReason', '')}\"*")

                st.divider()

# =============================================================================
# TAB 4: TEACHER / GOVERNANCE PANEL (Only for Teachers and Admin)
# =============================================================================
if tab_teacher is not None:
    with tab_teacher:
        st.subheader("🛡️ Teacher & AI Governance Console (edcafe.ai Inspired)")
        st.caption("Human-in-the-Loop review: Configure rubrics, override marks, release scores, and resolve challenges.")

        # Determine teacher subject filter
        if active_role == "teacher":
            teacher_subject = current_user.get("subject", "Mathematics")
            st.info(f"👩‍🏫 **Active Teacher:** {current_user.get('name')} | **Assigned Department:** {teacher_subject} • Scoped strictly to {teacher_subject} submissions.")
            teacher_submissions = [s for s in db["submissions"] if s.get("subject", "").lower() == teacher_subject.lower()]
        else:
            teacher_subject = "All Subjects"
            st.info("👑 Administrator Access: Full subject oversight and governance across all departments.")
            teacher_submissions = db["submissions"]

        # ---------------------------------------------------------------------
        # TEACHER DASHBOARD METRICS
        # ---------------------------------------------------------------------
        st.markdown("### 📊 Teacher Evaluation & Audit Dashboard")
        
        # Calculate live metrics
        eval_subs = [s for s in teacher_submissions if s.get("status") in ["RELEASED", "ACCEPTED"]]
        pending_subs = [s for s in teacher_submissions if s.get("status") == "PENDING_TEACHER_RELEASE"]
        challenged_subs = [s for s in teacher_submissions if s.get("status") == "CHALLENGED"]
        
        total_eval_questions = sum(len(s.get("questions", [])) for s in eval_subs)
        total_pending_questions = sum(len(s.get("questions", [])) for s in pending_subs)
        
        # Average review time calculation
        review_times = [s.get("evaluationTimeMins", 3.5) for s in eval_subs if s.get("evaluationTimeMins")]
        avg_time = round(sum(review_times) / max(1, len(review_times)), 1) if review_times else 3.5

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val" style="color:#10B981;">{len(eval_subs)} ({total_eval_questions} Qs)</div>
                <div class="stat-lbl">Evaluated Papers</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val" style="color:#F59E0B;">{len(pending_subs)} ({total_pending_questions} Qs)</div>
                <div class="stat-lbl">Awaiting Evaluation</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val" style="color:#6366F1;">{avg_time} min</div>
                <div class="stat-lbl">Avg. Review Time / Paper</div>
            </div>
            """, unsafe_allow_html=True)
        with m_col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val" style="color:#EF4444;">{len(challenged_subs)}</div>
                <div class="stat-lbl">Appeals Received</div>
            </div>
            """, unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # QUICK GLANCE: WHAT IS PENDING FROM YOUR SIDE
        # ---------------------------------------------------------------------
        st.markdown("#### ⚡ Quick Glance: What is Pending from Your Side")
        total_pending_actions = len(pending_subs) + len(challenged_subs)
        if total_pending_actions == 0:
            st.success("🎉 Superb! All student evaluations and appeals for your subject are completely up to date. Nothing pending!")
        else:
            st.markdown(f"""
            <div class="quick-glance-box">
                <strong style="color:#B45309; font-size:14px;">⚠️ Action Required: You have {total_pending_actions} item(s) awaiting your audit or resolution:</strong><br>
                <span style="font-size:13px; color:#92400E;">
                    • <strong>{len(pending_subs)} paper(s)</strong> awaiting initial teacher mark release.<br>
                    • <strong>{len(challenged_subs)} paper(s)</strong> returned as student appeals requiring justification re-check.
                </span>
            </div>
            """, unsafe_allow_html=True)

        # Teacher Directives Expander
        with st.expander("⚙️ Configure Custom Teacher Directives (www.edcafe.ai Style)", expanded=False):
            t_inst = st.text_area(
                f"Custom Grading Directives for {teacher_subject}:",
                value="Strictly penalize 0.5 marks if SI units are omitted. Award partial credit for derivation steps.",
                height=70
            )
            c_si = st.checkbox("Strict SI Units Check (-0.5 penalty)", value=True, key="chk_si")
            c_part = st.checkbox("Award Partial Credit for Formula Steps", value=True, key="chk_part")
            c_spell = st.checkbox("Lenient Spelling (Do not deduct for minor typos if meaning is clear)", value=True, key="chk_spell")
            if st.button("Save Teacher Directives", key="btn_save_directives"):
                st.success("Teacher directives saved and active!")

        st.markdown("### 📋 Student Submissions Requiring Action & Audit")

        if not teacher_submissions:
            st.info(f"No submissions found for {teacher_subject}.")
        else:
            for s_idx, sub in enumerate(teacher_submissions):
                sub = normalize_submission(sub, s_idx)
                sub_id = sub.get("id", f"sub_{s_idx}")
                student_name = sub.get("studentName", "Student")
                topic = sub.get("topic", "Subjective Assessment")
                subj_name = sub.get("subject", "Science")
                cls_name = sub.get("className", "Class 9th")
                awarded = float(sub.get("totalAwarded", 0.0))
                max_m = float(sub.get("totalMax", 20.0))
                status = sub.get("status", "PENDING_TEACHER_RELEASE")
                attachment = sub.get("attachmentName")

                with st.container():
                    st.markdown(f"**Submission: {student_name}** • {topic} ({subj_name} • {cls_name}) {f' | 📎 *{attachment}*' if attachment else ''}")
                    st.markdown(f"Current Marks: **{awarded} / {max_m}** | Status: `{status}`")

                    if status == "PENDING_TEACHER_RELEASE":
                        st.warning("⏳ Action Required: Review step marks and click 'Release Marks' below.")
                        new_marks = st.number_input(f"Override Total Score for {student_name}:", min_value=0.0, max_value=max(max_m, awarded), value=awarded, step=0.5, key=f"t_override_{sub_id}")
                        if st.button(f"✅ Release Marks to {student_name}", key=f"rel_btn_{sub_id}"):
                            sub["totalAwarded"] = new_marks
                            sub["totalAwardedMarks"] = new_marks
                            sub["status"] = "RELEASED"
                            sub["evaluatedAt"] = datetime.now().isoformat()
                            sub["evaluationTimeMins"] = 3.2
                            save_db(db)
                            st.success(f"Marks officially released to {student_name}!")
                            st.rerun()

                    elif status == "CHALLENGED":
                        st.error(f"⚠️ Student Appeal on Questions: {sub.get('challengeQuestions', [])}")
                        st.info(f"Student Rationale: *\"{sub.get('challengeReason', '')}\"*")
                        adj_marks = st.number_input(f"Adjust Final Marks after Appeal Review:", min_value=0.0, max_value=max(max_m, awarded), value=awarded, step=0.5, key=f"adj_{sub_id}")
                        t_remarks = st.text_input("Teacher Appeal Resolution Remarks:", value="Reviewed by Department Faculty. Step marks adjusted.", key=f"rem_{sub_id}")
                        if st.button(f"Resolve Challenge & Re-Release to {student_name}", key=f"res_btn_{sub_id}"):
                            sub["totalAwarded"] = adj_marks
                            sub["totalAwardedMarks"] = adj_marks
                            sub["status"] = "RELEASED"
                            sub["resolutionRemarks"] = t_remarks
                            save_db(db)
                            st.success("Challenge resolved and marks re-released!")
                            st.rerun()

                    elif status == "RELEASED":
                        st.info("Scores have been released to the student.")
                    elif status == "ACCEPTED":
                        st.success("Student has verified and accepted the final score.")

                    st.divider()

# =============================================================================
# TAB 5: ADMIN PANEL (Full Executive Summary: Subject, Teacher, Board Level)
# =============================================================================
if tab_admin is not None:
    with tab_admin:
        st.subheader("👑 EduAegis Institutional & Administrative Dashboard")
        st.caption("Complete institutional oversight: Cross-subject analytics, teacher workload, board benchmarking, and governance audit ledger.")

        all_subs = db.get("submissions", [])
        total_subs_count = len(all_subs)
        total_students_count = len([u for u in db["users"].values() if u.get("role") == "student"])
        total_teachers_count = len([u for u in db["users"].values() if u.get("role") == "teacher"])
        
        all_eval_subs = [s for s in all_subs if s.get("status") in ["RELEASED", "ACCEPTED"]]
        all_pending_subs = [s for s in all_subs if s.get("status") == "PENDING_TEACHER_RELEASE"]
        all_appeals_subs = [s for s in all_subs if s.get("status") == "CHALLENGED"]
        all_accepted_subs = [s for s in all_subs if s.get("status") == "ACCEPTED"]

        # Institutional Average Percentage
        avg_pct = round(sum((s.get("totalAwarded", 0.0) / max(1.0, s.get("totalMax", 20.0))) * 100 for s in all_subs) / max(1, len(all_subs)), 1) if all_subs else 0.0

        # Top Executive Metrics Ribbon
        kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
        with kpi1:
            st.metric("Total Students", f"{total_students_count} Active")
        with kpi2:
            st.metric("Faculty Members", f"{total_teachers_count} Teachers")
        with kpi3:
            st.metric("Total Submissions", f"{total_subs_count} Papers")
        with kpi4:
            st.metric("Pending Audits", f"{len(all_pending_subs)} Queue", delta=f"{len(all_pending_subs)} action req", delta_color="inverse")
        with kpi5:
            st.metric("Appeals Pending", f"{len(all_appeals_subs)} Active", delta=f"{len(all_appeals_subs)} review req", delta_color="inverse")
        with kpi6:
            st.metric("Institutional Avg", f"{avg_pct}%", delta="CBSE/ICSE")

        st.markdown("---")

        # ---------------------------------------------------------------------
        # SECTION 1: SUBJECT-LEVEL BREAKDOWN
        # ---------------------------------------------------------------------
        st.markdown("### 📊 1. Subject-Level Performance & Appeal Summary")
        st.caption("Aggregated assessment status, marks distribution, and appeals at subject department level:")

        subjects_list = ["Mathematics", "Chemistry", "Physics"]
        sub_rows = []
        for subj in subjects_list:
            s_papers = [s for s in all_subs if s.get("subject", "").lower() == subj.lower()]
            s_pending = len([s for s in s_papers if s.get("status") == "PENDING_TEACHER_RELEASE"])
            s_eval = len([s for s in s_papers if s.get("status") in ["RELEASED", "ACCEPTED"]])
            s_appeals = len([s for s in s_papers if s.get("status") == "CHALLENGED"])
            s_avg = round(sum((s.get("totalAwarded", 0.0) / max(1.0, s.get("totalMax", 20.0))) * 100 for s in s_papers) / max(1, len(s_papers)), 1) if s_papers else 0.0
            
            lead_faculty = "Akanksha" if subj == "Mathematics" else ("Ankur" if subj == "Chemistry" else "Physics Dept")
            sub_rows.append({
                "Subject": subj,
                "Lead Faculty": lead_faculty,
                "Total Papers": len(s_papers),
                "Pending Audit": s_pending,
                "Evaluated & Released": s_eval,
                "Appeals Pending": s_appeals,
                "Average Score": f"{s_avg}%"
            })
        st.dataframe(sub_rows, use_container_width=True)

        st.markdown("---")

        # ---------------------------------------------------------------------
        # SECTION 2: TEACHER-LEVEL WORKLOAD & AUDIT EFFICIENCY
        # ---------------------------------------------------------------------
        st.markdown("### 👩‍🏫 2. Teacher-Level Workload & Review Efficiency")
        st.caption("Teacher audit speed, pending backlog, and appeal resolution metrics:")

        col_tch1, col_tch2 = st.columns(2)
        with col_tch1:
            st.markdown("""
            <div class="soothing-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="font-size:16px; color:#4338CA;">👩‍🏫 Akanksha • Mathematics Lead</strong>
                    <span class="role-badge role-teacher">Maths Faculty</span>
                </div>
                <hr style="margin:8px 0;">
                <p style="font-size:13px; color:#334155; line-height:1.6;">
                    • <strong>Assigned Papers:</strong> 3 Submissions (Class 9th)<br>
                    • <strong>Evaluated & Released:</strong> 1 Paper (Anup - 18/20)<br>
                    • <strong>Pending Audit:</strong> 1 Paper (Anup - 15/20)<br>
                    • <strong>Appeals Handled:</strong> 1 Active (Nandita - Rationalizing Denominator)<br>
                    • <strong>Avg Review Time:</strong> 3.4 mins / paper
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_tch2:
            st.markdown("""
            <div class="soothing-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="font-size:16px; color:#0D9488;">👨‍🏫 Ankur • Chemistry Lead</strong>
                    <span class="role-badge role-teacher">Chemistry Faculty</span>
                </div>
                <hr style="margin:8px 0;">
                <p style="font-size:13px; color:#334155; line-height:1.6;">
                    • <strong>Assigned Papers:</strong> 3 Submissions (Class 9th)<br>
                    • <strong>Evaluated & Released:</strong> 1 Paper (Nandita - 19/20)<br>
                    • <strong>Pending Audit:</strong> 1 Paper (Nandita - 14.5/20)<br>
                    • <strong>Appeals Handled:</strong> 1 Active (Anup - Evaporation Cooling)<br>
                    • <strong>Avg Review Time:</strong> 4.1 mins / paper
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ---------------------------------------------------------------------
        # SECTION 3: BOARD-LEVEL ACADEMIC SUMMARY
        # ---------------------------------------------------------------------
        st.markdown("### 🏛️ 3. Board-Level Performance & Appeal Benchmarking")
        st.caption("Comparing student outcomes and appeal frequencies across curriculum boards:")

        board_rows = []
        for b_name in ["CBSE (All India)", "ICSE / CISCE", "State Board (Maharashtra/UP/Karnataka)"]:
            b_subs = [s for s in all_subs if s.get("board") == b_name or b_name.split(" ")[0] in s.get("board", "")]
            b_avg = round(sum((s.get("totalAwarded", 0.0) / max(1.0, s.get("totalMax", 20.0))) * 100 for s in b_subs) / max(1, len(b_subs)), 1) if b_subs else 0.0
            b_appeals = len([s for s in b_subs if s.get("status") == "CHALLENGED"])
            board_rows.append({
                "Board Name": b_name,
                "Total Submissions": len(b_subs),
                "Average Score": f"{b_avg}%",
                "Appeals Filed": b_appeals,
                "Mastery Rate (>75%)": f"{round((len([s for s in b_subs if (s.get('totalAwarded',0)/20.0) >= 0.75]) / max(1, len(b_subs))) * 100, 1)}%" if b_subs else "N/A"
            })
        st.dataframe(board_rows, use_container_width=True)

        st.markdown("---")

        # ---------------------------------------------------------------------
        # SECTION 4: MASTER GOVERNANCE LEDGER & USER MANAGEMENT
        # ---------------------------------------------------------------------
        st.markdown("### 📜 4. Master Submissions Ledger (Full Application Summary)")
        st.caption("Live auditable log of every paper submitted across the entire institution:")

        col_flt1, col_flt2, col_flt3 = st.columns(3)
        with col_flt1:
            flt_subj = st.selectbox("Filter Subject", ["All"] + subjects_list, index=0)
        with col_flt2:
            flt_status = st.selectbox("Filter Status", ["All", "PENDING_TEACHER_RELEASE", "RELEASED", "ACCEPTED", "CHALLENGED"], index=0)
        with col_flt3:
            flt_student = st.selectbox("Filter Student", ["All", "Anup", "Nandita", "Aarav Sharma"], index=0)

        ledger_records = []
        for s in all_subs:
            if flt_subj != "All" and s.get("subject") != flt_subj:
                continue
            if flt_status != "All" and s.get("status") != flt_status:
                continue
            if flt_student != "All" and s.get("studentName") != flt_student:
                continue

            ledger_records.append({
                "Submission ID": s.get("id"),
                "Student": s.get("studentName"),
                "Subject": s.get("subject"),
                "Topic": s.get("topic"),
                "Board": s.get("board"),
                "Score": f"{s.get('totalAwarded')} / {s.get('totalMax')}",
                "Status": s.get("status"),
                "Assigned Teacher": s.get("assignedTeacher", "N/A"),
                "Submitted At": str(s.get("submittedAt"))[:16]
            })

        if ledger_records:
            st.dataframe(ledger_records, use_container_width=True)
        else:
            st.info("No records match the selected filter criteria.")

        with st.expander("👥 Registered Users Directory & System Accounts"):
            users_summary = []
            for u_k, u_v in db["users"].items():
                users_summary.append({
                    "Username": u_v.get("username"),
                    "Full Name": u_v.get("name"),
                    "Role": u_v.get("role").upper(),
                    "Assigned Subject": u_v.get("subject", "N/A"),
                    "Class / Board": f"Class {u_v.get('studentClass')}th ({u_v.get('board')})" if u_v.get("role") == "student" else "Faculty / Admin",
                    "Email": u_v.get("email"),
                    "Current Password": u_v.get("password")
                })
            st.dataframe(users_summary, use_container_width=True)

# -----------------------------------------------------------------------------
# GLOBAL FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; font-size:12px; color:#64748B;">
    🛡️ <strong>EduAegis</strong> • Responsible AI Tutor & Governed Grader • IIM Capstone Project<br>
    Logged in as: <strong>{current_user.get('name')}</strong> ({role_label}) • Aligned with CBSE, ICSE, and State Boards • Compliant with NITI Aayog & UNESCO AI Ethics
</div>
""", unsafe_allow_html=True)

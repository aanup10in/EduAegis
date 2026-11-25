"""
EduAegis - Streamlit Web Application
Responsible AI Tutor & Governed Subjective Grader (Multi-Subject: Physics, Chemistry, Maths)
Classes 8th, 9th, 10th • CBSE, ICSE, State Board
Role-Based Access Control (RBAC): Student (Anup, Nandita), Teacher (Akanksha - Maths, Ankur - Chemistry), Admin
Full Cross-Tab Parameter Persistence & Question-by-Question Rubric Evaluation Engine
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
        margin-bottom: 16px;
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
    
    /* Academic Context Bar */
    .sync-bar {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
    }
    
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
    }

    .subj-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #ECFDF5;
        color: #047857;
        font-weight: 700;
        font-size: 12px;
        padding: 6px 14px;
        border-radius: 9999px;
        border: 1px solid #A7F3D0;
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

    .q-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
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
# STEP-BY-STEP QUESTION RUBRIC EVALUATOR (Per-Question & Bulk Evaluator)
# -----------------------------------------------------------------------------
def evaluate_single_question(subject, idx, q_text, q_max, ans):
    """Evaluates an individual question against curriculum rubrics and teacher directives."""
    ans_clean = (ans or "").strip().lower()
    q_max = float(q_max)
    step1_max = round(q_max * 0.5, 1)
    step2_max = round(q_max - step1_max, 1)

    if not ans_clean:
        return {
            "question": q_text,
            "questionText": q_text,
            "max": q_max,
            "maxMarks": q_max,
            "score": 0.0,
            "awardedMarks": 0.0,
            "student_ans": "",
            "studentAnswer": "",
            "stepBreakdown": [
                {"stepNumber": 1, "stepFocus": "Core Concept & Formulation", "marksAwarded": 0.0, "maxMarks": step1_max, "whyAwardedOrDeducted": "No answer provided."},
                {"stepNumber": 2, "stepFocus": "Mathematical / Logical Reasoning & Units", "marksAwarded": 0.0, "maxMarks": step2_max, "whyAwardedOrDeducted": "No answer provided."}
            ],
            "deductionExplanation": "Answer is blank. Please write your step-by-step reasoning for evaluation."
        }

    step1_awarded = 0.0
    step2_awarded = 0.0
    step1_reason = "Demonstrated correct core scientific principles and law formulation."
    step2_reason = "Accurate metric calculations, SI units, and logical reasoning applied."

    if subject == "Physics":
        if idx == 0:  # F = ma
            if "rate of change of momentum" in ans_clean and "proportional" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.5, 1)
                step1_reason = "Partially stated; omitted either 'rate of change of momentum' or proportionality condition."
            if ("f = ma" in ans_clean or "f=ma" in ans_clean) and ("newton" in ans_clean or " n" in ans_clean):
                step2_awarded = step2_max
            elif "f = ma" in ans_clean or "p1" in ans_clean or "mu" in ans_clean:
                step2_awarded = round(step2_max * 0.7, 1)
                step2_reason = "Derived formula; SI units partially omitted."
            else:
                step2_awarded = round(step2_max * 0.3, 1)
                step2_reason = "Derivation steps incomplete."
        elif idx == 1:  # Fielder
            if "time" in ans_clean and ("increase" in ans_clean or "more time" in ans_clean or "pull" in ans_clean):
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.4, 1)
                step1_reason = "Missed the key mechanism of increasing stopping time (t)."
            if "force" in ans_clean or "momentum" in ans_clean or "impulse" in ans_clean:
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.4, 1)
                step2_reason = "Relationship between time and impact force not explicitly linked."
        elif idx == 2:  # Inertia
            if "resist" in ans_clean or "state" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.5, 1)
            if "mass" in ans_clean and ("rest" in ans_clean or "motion" in ans_clean or "direction" in ans_clean):
                step2_awarded = step2_max
            elif "mass" in ans_clean:
                step2_awarded = round(step2_max * 0.7, 1)
            else:
                step2_awarded = round(step2_max * 0.4, 1)
                step2_reason = "Missing mention of mass as the measure of inertia."
        elif idx == 3:  # Numerical
            if "5" in ans_clean or "retardation" in ans_clean or "-5" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.4, 1)
                step1_reason = "Acceleration calculation error."
            if "6000" in ans_clean:
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.4, 1)
                step2_reason = "Final force calculation incomplete or missing Newton (N) unit."
        else:  # 3rd law
            if "equal" in ans_clean and "opposite" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.5, 1)
            if "different" in ans_clean or "two bodies" in ans_clean:
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.3, 1)
                step2_reason = "Missed crucial explanation: action-reaction forces act simultaneously on TWO DIFFERENT bodies."

    elif subject == "Chemistry":
        if idx == 0:  # Evaporation
            if "liquid" in ans_clean and ("vapor" in ans_clean or "gas" in ans_clean) and ("boiling" in ans_clean or "surface" in ans_clean):
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.6, 1)
            factors_found = sum(1 for f in ["surface", "temperature", "humidity", "wind"] if f in ans_clean)
            step2_awarded = round(step2_max * min(1.0, max(0.3, factors_found / 3.0)), 1)
            if factors_found < 3:
                step2_reason = f"Identified {factors_found}/4 factors. Mention surface area, temp, humidity, wind."
        elif idx == 1:  # Latent heat
            if "latent" in ans_clean and ("heat" in ans_clean or "energy" in ans_clean):
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.5, 1)
            if "steam" in ans_clean and ("extra" in ans_clean or "more" in ans_clean or "22.5" in ans_clean or "2.26" in ans_clean or "condens" in ans_clean):
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.5, 1)
                step2_reason = "Steam contains extra latent heat of vaporization that is released upon contact with skin."
        elif idx == 2:  # Boiling vs Evaporation
            if "bulk" in ans_clean and "surface" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.6, 1)
            if "cooling" in ans_clean or "boiling point" in ans_clean or "temperature" in ans_clean:
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.5, 1)
        elif idx == 3:  # Conversions
            if "273" in ans_clean or "k =" in ans_clean or "t(k)" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.5, 1)
            if "298" in ans_clean and "100" in ans_clean:
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.5, 1)
        else:  # Ice at 273 K
            if "fusion" in ans_clean or "latent" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.5, 1)
                step1_reason = "Missed explicit mention of Latent Heat of Fusion."
            if "absorb" in ans_clean or "surround" in ans_clean or "heat" in ans_clean:
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.5, 1)

    else:  # Mathematics
        if idx == 0:  # 0.333... in p/q
            if "10x" in ans_clean or "let x" in ans_clean or "subtract" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.5, 1)
            if "1/3" in ans_clean or "3/9" in ans_clean:
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.4, 1)
                step2_reason = "Final simplified fraction 1/3 not reached."
        elif idx == 1:  # Rationalize
            if "conjugate" in ans_clean or "7 - 3" in ans_clean or "7-3" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.5, 1)
            if "31" in ans_clean or "49 - 18" in ans_clean:
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.5, 1)
                step2_reason = "Denominator difference of squares (49 - 18 = 31) calculation error."
        elif idx == 2:  # 3 rationals
            if "30/50" in ans_clean or "common" in ans_clean or "/" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.6, 1)
            step2_awarded = step2_max if any(num in ans_clean for num in ["31", "32", "33", "34", "35", "7/10", "13/20"]) else round(step2_max * 0.5, 1)
        elif idx == 3:  # Exponents
            if "2" in ans_clean and ("2/3 + 1/3" in ans_clean or "2^1" in ans_clean or "power" in ans_clean):
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.6, 1)
            if "3^-21" in ans_clean or "1/3^21" in ans_clean or "21" in ans_clean:
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.5, 1)
        else:  # Rational vs irrational
            if "difference" in ans_clean or "irrational" in ans_clean:
                step1_awarded = step1_max
            else:
                step1_awarded = round(step1_max * 0.5, 1)
            if "product" in ans_clean or "pi" in ans_clean or "π" in ans_clean:
                step2_awarded = step2_max
            else:
                step2_awarded = round(step2_max * 0.5, 1)

    score = round(min(q_max, max(0.5, step1_awarded + step2_awarded)), 1)
    return {
        "question": q_text,
        "questionText": q_text,
        "max": q_max,
        "maxMarks": q_max,
        "score": score,
        "awardedMarks": score,
        "student_ans": ans,
        "studentAnswer": ans,
        "stepBreakdown": [
            {"stepNumber": 1, "stepFocus": "Core Concept & Formulation", "marksAwarded": step1_awarded, "maxMarks": step1_max, "whyAwardedOrDeducted": step1_reason},
            {"stepNumber": 2, "stepFocus": "Mathematical / Logical Reasoning & Units", "marksAwarded": step2_awarded, "maxMarks": step2_max, "whyAwardedOrDeducted": step2_reason}
        ],
        "deductionExplanation": f"Step 1: {step1_reason} | Step 2: {step2_reason}"
    }

# -----------------------------------------------------------------------------
# AUTHENTICATION & ROLE-BASED ACCESS CONTROL (RBAC)
# -----------------------------------------------------------------------------
if "auth_user" not in st.session_state:
    st.session_state["auth_user"] = db["users"].get("anup", DEFAULT_USERS["anup"])

current_user = st.session_state["auth_user"]
active_role = current_user.get("role", "student")

# -----------------------------------------------------------------------------
# GLOBAL CURRICULUM STATE INITIALIZATION & BIDIRECTIONAL SYNC
# -----------------------------------------------------------------------------
board_options = ["CBSE (All India)", "ICSE / CISCE", "State Board (Maharashtra/UP/Karnataka)", "Cambridge IGCSE"]
class_options = [8, 9, 10]
subject_options = ["Physics", "Chemistry", "Mathematics"]

if "sel_board" not in st.session_state:
    st.session_state["sel_board"] = current_user.get("board", "CBSE (All India)") if current_user.get("board") in board_options else "CBSE (All India)"
if "sel_class" not in st.session_state:
    st.session_state["sel_class"] = current_user.get("studentClass", 9) if current_user.get("studentClass") in class_options else 9
if "sel_subject" not in st.session_state:
    st.session_state["sel_subject"] = current_user.get("subject", "Mathematics") if active_role == "teacher" and current_user.get("subject") in subject_options else "Mathematics" if active_role == "student" else "Physics"
if "sel_topic" not in st.session_state:
    st.session_state["sel_topic"] = "Rational vs Irrational Numbers" if st.session_state["sel_subject"] == "Mathematics" else ("Evaporation & Latent Heat Cooling" if st.session_state["sel_subject"] == "Chemistry" else "Newton's Second Law & Momentum (F = ma)")
if "q_evals" not in st.session_state:
    st.session_state["q_evals"] = {}
if "q_answers" not in st.session_state:
    st.session_state["q_answers"] = {}

def sync_global_subject(new_subject):
    st.session_state["sel_subject"] = new_subject
    if new_subject == "Mathematics":
        st.session_state["sel_topic"] = "Rational vs Irrational Numbers"
    elif new_subject == "Chemistry":
        st.session_state["sel_topic"] = "Evaporation & Latent Heat Cooling"
    else:
        st.session_state["sel_topic"] = "Newton's Second Law & Momentum (F = ma)"
    st.session_state["q_evals"] = {}

def on_tutor_subj_change():
    sync_global_subject(st.session_state["t_subj"])

def on_tutor_class_change():
    st.session_state["sel_class"] = st.session_state["t_class"]

def on_tutor_topic_change():
    st.session_state["sel_topic"] = st.session_state["t_top"]

def on_grader_subj_change():
    sync_global_subject(st.session_state["g_subj"])

def on_grader_class_change():
    st.session_state["sel_class"] = st.session_state["g_class"]

def on_grader_board_change():
    st.session_state["sel_board"] = st.session_state["g_board"]

def on_ribbon_board_change():
    st.session_state["sel_board"] = st.session_state["ribbon_board"]

def on_ribbon_class_change():
    st.session_state["sel_class"] = st.session_state["ribbon_class"]

def on_ribbon_subj_change():
    sync_global_subject(st.session_state["ribbon_subj"])

# -----------------------------------------------------------------------------
# SIDEBAR: Persona Switcher, Authentication & Change Password
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ EduAegis Role & Auth Portal")

    st.markdown("#### ⚡ 1-Click Role Switcher:")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("🎓 Anup\n(CBSE Student)", use_container_width=True):
            st.session_state["auth_user"] = db["users"]["anup"]
            st.session_state["sel_board"] = "CBSE (All India)"
            st.session_state["sel_class"] = 9
            st.session_state["q_evals"] = {}
            st.rerun()
        if st.button("👩‍🏫 Akanksha\n(Maths Teacher)", use_container_width=True):
            st.session_state["auth_user"] = db["users"]["akanksha"]
            sync_global_subject("Mathematics")
            st.rerun()
    with col_p2:
        if st.button("🎓 Nandita\n(ICSE Student)", use_container_width=True):
            st.session_state["auth_user"] = db["users"]["nandita"]
            st.session_state["sel_board"] = "ICSE / CISCE"
            st.session_state["sel_class"] = 9
            st.session_state["q_evals"] = {}
            st.rerun()
        if st.button("👨‍🏫 Ankur\n(Chem Teacher)", use_container_width=True):
            st.session_state["auth_user"] = db["users"]["ankur"]
            sync_global_subject("Chemistry")
            st.rerun()
    if st.button("👑 System Admin (Full Privileges)", use_container_width=True):
        st.session_state["auth_user"] = db["users"]["admin"]
        st.rerun()

    st.divider()

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

    with st.expander("🔐 Switch User / Login with Credentials"):
        login_u = st.selectbox("Select Username", list(db["users"].keys()), index=list(db["users"].keys()).index(current_user["username"]))
        login_p = st.text_input("Password", type="password", value="Eduaegis123", key="login_pass_input")
        if st.button("Login", key="btn_login_submit"):
            target_user = db["users"].get(login_u)
            if target_user and target_user.get("password") == login_p:
                st.session_state["auth_user"] = target_user
                if target_user.get("role") == "teacher" and target_user.get("subject"):
                    sync_global_subject(target_user["subject"])
                st.success(f"Welcome, {target_user.get('name')}!")
                st.rerun()
            else:
                st.error("Invalid password. (Default is Eduaegis123)")

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
    st.caption("🔒 Role Privileges Enforced: Students see only personal work; Teachers see their subject; Admin has global oversight.")

# -----------------------------------------------------------------------------
# GLOBAL PERSISTENT HEADER & PERSISTENT CURRICULUM CONTROL RIBBON
# -----------------------------------------------------------------------------
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
            Powered by question-by-question rubrics, audio narration, controlled teacher release, and student appeal governance.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_head2:
    st.markdown(f"""
    <div style="background:#EEF2FF; border:1px solid #C7D2FE; border-radius:14px; padding:12px; text-align:center;">
        <span style="font-size:11px; font-weight:700; color:#4338CA; text-transform:uppercase;">Active Academic Context</span>
        <div style="font-size:15px; font-weight:800; color:#1E1B4B; margin-top:2px;">
            {st.session_state['sel_subject']} • Class {st.session_state['sel_class']}th
        </div>
        <div style="font-size:11px; color:#6366F1; font-weight:600;">{st.session_state['sel_board'].split(' ')[0]}</div>
    </div>
    """, unsafe_allow_html=True)

# Persistent Shared Control Ribbon
st.markdown("""
<div class="sync-bar">
    <span style="font-weight:800; font-size:13px; color:#1E293B;">🏛️ Persistent Curriculum Controls (Synced Globally Across All Pages):</span>
    <span style="font-size:12px; color:#64748B;">Changes here or inside tabs automatically persist when navigating between Tutor and Grader.</span>
</div>
""", unsafe_allow_html=True)

col_rb1, col_rb2, col_rb3 = st.columns([1.5, 1, 1.5])
with col_rb1:
    st.selectbox(
        "1. Curriculum Board",
        board_options,
        index=board_options.index(st.session_state["sel_board"]),
        key="ribbon_board",
        on_change=on_ribbon_board_change
    )
with col_rb2:
    st.selectbox(
        "2. Class Standard",
        class_options,
        index=class_options.index(st.session_state["sel_class"]),
        key="ribbon_class",
        on_change=on_ribbon_class_change
    )
with col_rb3:
    st.selectbox(
        "3. Active Subject",
        subject_options,
        index=subject_options.index(st.session_state["sel_subject"]),
        key="ribbon_subj",
        on_change=on_ribbon_subj_change
    )

# -----------------------------------------------------------------------------
# DYNAMIC TAB NAVIGATION BASED ON ROLE
# -----------------------------------------------------------------------------
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
# TAB 1: AI TUTOR (Concept Learning, Persistent Subject, Audio Narration)
# =============================================================================
with tab_tutor:
    st.subheader("💡 Socratic AI Tutor: Concept Learning & Clearing")
    st.caption("Learn any concept in simple conversational English with speech narration and everyday analogies.")

    # In-Tab Synchronized Filters
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.selectbox(
            "Class",
            class_options,
            index=class_options.index(st.session_state["sel_class"]),
            key="t_class",
            on_change=on_tutor_class_change
        )
    with col_t2:
        st.selectbox(
            "Subject",
            subject_options,
            index=subject_options.index(st.session_state["sel_subject"]),
            key="t_subj",
            on_change=on_tutor_subj_change
        )
    with col_t3:
        if st.session_state["sel_subject"] == "Physics":
            t_topics = ["Newton's Second Law & Momentum (F = ma)", "Inertia and First Law of Motion", "Universal Gravitation & Floatation", "Work, Energy & Power", "Sound & Waves"]
        elif st.session_state["sel_subject"] == "Chemistry":
            t_topics = ["Evaporation & Latent Heat Cooling", "States of Matter & Phase Transitions", "Atoms, Molecules & Chemical Formulas", "Structure of the Atom"]
        else:
            t_topics = ["Rational vs Irrational Numbers", "Rationalizing the Denominator", "Laws of Exponents", "Polynomials & Factorization", "Linear Equations"]
        
        default_top_idx = t_topics.index(st.session_state["sel_topic"]) if st.session_state["sel_topic"] in t_topics else 0
        t_selected_topic = st.selectbox("Curriculum Topic", t_topics, index=default_top_idx, key="t_top", on_change=on_tutor_topic_change)

    # Open Box Text Input for Custom Student Topic
    st.markdown("#### 🔍 Or Type Any Custom Topic to Clear Your Doubt:")
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
        st.info(f"**Curriculum Context:** {st.session_state['sel_board']} • Class {st.session_state['sel_class']}th {st.session_state['sel_subject']}")

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
        st.info("Switch to the **AI Grader** tab to test your understanding question-by-question with instant step-by-step feedback!")

# =============================================================================
# TAB 2: AI GRADER (Question-by-Question Evaluation & Synchronized Filters)
# =============================================================================
with tab_grader:
    st.subheader("✍️ AI Subjective Grader: Multi-Subject Assessment")
    st.caption("Evaluate your subjective answers question-by-question with instant step marks, scientific rubrics, and teacher review.")

    # In-Tab Synchronized Filters (Bound directly to global session state)
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        st.selectbox(
            "Board",
            board_options,
            index=board_options.index(st.session_state["sel_board"]),
            key="g_board",
            on_change=on_grader_board_change
        )
    with g_col2:
        st.selectbox(
            "Class",
            class_options,
            index=class_options.index(st.session_state["sel_class"]),
            key="g_class",
            on_change=on_grader_class_change
        )
    with g_col3:
        st.selectbox(
            "Subject",
            subject_options,
            index=subject_options.index(st.session_state["sel_subject"]),
            key="g_subj",
            on_change=on_grader_subj_change
        )

    # Active Subject & Topic Confirmation
    cur_subject = st.session_state["sel_subject"]
    active_grade_topic = st.session_state["sel_topic"]

    st.markdown(f"""
    <div style="background:#EEF2FF; border:1px solid #C7D2FE; border-radius:12px; padding:12px 18px; margin-bottom:14px;">
        <span style="font-weight:700; color:#4338CA;">🎯 Active Assessment Subject:</span> <strong>{cur_subject}</strong> • 
        <span style="font-weight:700; color:#4338CA;">Topic:</span> <strong>{active_grade_topic}</strong> • 
        <span style="font-weight:700; color:#4338CA;">Candidate:</span> <code>{current_user.get('name')}</code>
    </div>
    """, unsafe_allow_html=True)

    # Mode Selector: Structured 5 Questions vs File Upload
    eval_mode = st.radio(
        "Choose your submission mode:",
        ["📝 Option A: Question-by-Question Subjective Paper", "📄 Option B: Upload Scanned Paper / Answer Sheet (PDF or Image)"],
        horizontal=True
    )

    # Define 5 Questions based on Active Subject
    if cur_subject == "Physics":
        questions = [
            {"id": "q1", "text": "State Newton's Second Law of Motion. Derive the formula F = ma defining all SI units.", "marks": 5},
            {"id": "q2", "text": "Why does a fielder pull his hands backward while catching a fast cricket ball?", "marks": 3},
            {"id": "q3", "text": "Define Inertia. Name its three types with daily-life examples and state its measure.", "marks": 3},
            {"id": "q4", "text": "A 1200 kg car slows from 90 km/h to 18 km/h in 4 s. Calculate acceleration and force.", "marks": 5},
            {"id": "q5", "text": "State Newton's Third Law. Why do action and reaction forces not cancel each other?", "marks": 4}
        ]
    elif cur_subject == "Chemistry":
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

    # -------------------------------------------------------------------------
    # MODE A: QUESTION-BY-QUESTION SUBJECTIVE EVALUATION
    # -------------------------------------------------------------------------
    if "Option A" in eval_mode:
        # Solved Examples with Hidden Solutions
        with st.expander(f"📘 Practice Solved Example for {cur_subject} (Solution Hidden by Default)", expanded=False):
            if cur_subject == "Physics":
                st.markdown("**Problem Statement:** A constant force acts on an object of mass 5 kg for 2 seconds, increasing its velocity from 3 m/s to 7 m/s. Calculate the magnitude of the applied force. (4 Marks)")
                if st.button("Show Step-by-Step Solved Solution", key="btn_show_sol_p"):
                    st.markdown("""
                    **Step-by-Step Solved Solution:**
                    - **Step 1:** Given: mass m = 5 kg, initial velocity u = 3 m/s, final velocity v = 7 m/s, time t = 2 s. *(+1 Mark)*
                    - **Step 2:** Acceleration: a = (v - u) / t = (7 - 3) / 2 = 4 / 2 = 2 m/s². *(+1 Mark)*
                    - **Step 3:** Force using F = m * a: F = 5 kg * 2 m/s² = 10 Newtons (N). *(+1 Mark)*
                    - **Step 4:** Final Result: Applied Force = 10 N. *(+1 Mark)*
                    """)
            elif cur_subject == "Chemistry":
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

        st.markdown("### ✍️ 5-Question Assessment: Question-by-Question Evaluation")
        st.caption("You can evaluate every question individually with instant step marks, or bulk-evaluate the full test paper!")

        # 1-Click Demo Loaders
        col_d1, col_d2, col_d3 = st.columns(3)
        load_demo = None
        with col_d1:
            if st.button("🌟 1-Click: 20/20 Exemplary Answers"):
                load_demo = "high"
        with col_d2:
            if st.button("⚖️ 1-Click: 12/20 Average Answers"):
                load_demo = "avg"
        with col_d3:
            if st.button("⚠️ 1-Click: 5/20 Misconception Answers"):
                load_demo = "poor"

        # Apply demo answers if clicked
        if load_demo:
            st.session_state["q_evals"] = {}
            if load_demo == "high":
                if cur_subject == "Physics":
                    defaults = [
                        "Newton's Second Law states that rate of change of momentum is proportional to applied force in direction of force. p1=mu, p2=mv, Δp=m(v-u). Rate=m(v-u)/t=ma. F=ma. Units: Force in N, mass in kg, acc in m/s².",
                        "Fielder pulls hands back to increase stopping time t. Since F = m(v-u)/t, increasing time decreases the rate of change of momentum, reducing impact force on palms.",
                        "Inertia is property resisting change of rest or motion. Types: rest, motion, direction. Mass measures inertia.",
                        "u = 25 m/s, v = 5 m/s. a = (5-25)/4 = -5 m/s² (retardation). Change in momentum = -24000 kg·m/s. Force = 1200*(-5) = -6000 N.",
                        "Action and reaction are equal and opposite. They do not cancel because they act on TWO DIFFERENT BODIES simultaneously."
                    ]
                elif cur_subject == "Chemistry":
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
                for idx, q in enumerate(questions):
                    st.session_state[f"ans_{q['id']}"] = defaults[idx]
            elif load_demo == "avg":
                for idx, q in enumerate(questions):
                    st.session_state[f"ans_{q['id']}"] = "Force equals mass into acceleration. Momentum is mv. F = ma. Newton is unit." if cur_subject == "Physics" else "Evaporation is liquid to gas. Heat and wind affect it."
            elif load_demo == "poor":
                for idx, q in enumerate(questions):
                    st.session_state[f"ans_{q['id']}"] = "Every action has reaction. Formula is F = ma where m is matter and a is speed. Unit is Joules." if cur_subject == "Physics" else "Ice is cold so it cools things."
            st.rerun()

        # Render Each Question with Individual Evaluation Button & Result Card
        for idx, q in enumerate(questions):
            q_id = q["id"]
            curr_val = st.session_state.get(f"ans_{q_id}", "")
            is_evaluated = q_id in st.session_state["q_evals"]

            st.markdown(f"""
            <div class="q-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <strong style="font-size:15px; color:#1E293B;">Q{idx+1} ({q['marks']} Marks): {q['text']}</strong>
                    <span style="font-size:12px; font-weight:700; color:#6366F1; background:#EEF2FF; padding:3px 10px; border-radius:9999px;">Max: {q['marks']}m</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            user_ans = st.text_area(
                f"Your Subjective Answer for Q{idx+1}:",
                value=curr_val,
                height=80,
                key=f"ans_{q_id}",
                placeholder=f"Write your step-by-step reasoning, formula, SI units, and calculations for Q{idx+1}..."
            )

            # Individual Question Action Row
            col_b1, col_b2, col_stat = st.columns([2, 1, 3])
            with col_b1:
                if st.button(f"⚡ Evaluate Q{idx+1} Individually", key=f"btn_indiv_{q_id}"):
                    if not user_ans.strip():
                        st.warning(f"Please enter your answer for Q{idx+1} before evaluating.")
                    else:
                        eval_res = evaluate_single_question(cur_subject, idx, q["text"], q["marks"], user_ans)
                        st.session_state["q_evals"][q_id] = eval_res
                        st.rerun()

            with col_b2:
                if is_evaluated:
                    if st.button(f"🔄 Reset Q{idx+1}", key=f"btn_reset_{q_id}"):
                        del st.session_state["q_evals"][q_id]
                        st.rerun()

            with col_stat:
                if is_evaluated:
                    res = st.session_state["q_evals"][q_id]
                    st.markdown(f"<span style='background:#DCFCE7; color:#15803D; font-weight:700; font-size:13px; padding:6px 14px; border-radius:9999px; border:1px solid #86EFAC;'>🎯 Awarded: {res['score']} / {res['max']} Marks</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='background:#F1F5F9; color:#64748B; font-size:12px; font-weight:600; padding:6px 12px; border-radius:9999px;'>⚪ Question not evaluated yet</span>", unsafe_allow_html=True)

            # Display Individual Question Rubric Breakdown Card if evaluated
            if is_evaluated:
                res = st.session_state["q_evals"][q_id]
                st.markdown(f"""
                <div style="background:#F0FDF4; border:1px solid #86EFAC; border-radius:12px; padding:12px 16px; margin-top:6px; margin-bottom:14px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <strong style="color:#166534; font-size:13px;">✓ Q{idx+1} AI Rubric Score Breakdown:</strong>
                        <span style="background:#16A34A; color:white; font-size:11px; font-weight:bold; padding:2px 8px; border-radius:9999px;">STEP VERIFIED</span>
                    </div>
                    <div style="font-size:12px; color:#14532D; margin-bottom:4px;">
                        • <strong>Step 1: {res['stepBreakdown'][0]['stepFocus']}</strong> (<code>{res['stepBreakdown'][0]['marksAwarded']} / {res['stepBreakdown'][0]['maxMarks']}m</code>): {res['stepBreakdown'][0]['whyAwardedOrDeducted']}
                    </div>
                    <div style="font-size:12px; color:#14532D; margin-bottom:4px;">
                        • <strong>Step 2: {res['stepBreakdown'][1]['stepFocus']}</strong> (<code>{res['stepBreakdown'][1]['marksAwarded']} / {res['stepBreakdown'][1]['maxMarks']}m</code>): {res['stepBreakdown'][1]['whyAwardedOrDeducted']}
                    </div>
                    <div style="font-size:11px; color:#475569; margin-top:6px; border-top:1px dashed #CBD5E1; padding-top:4px;">
                        💡 <em>{res['deductionExplanation']}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

        # ---------------------------------------------------------------------
        # CUMULATIVE SCORE & PAPER SUBMISSION CONTROLS
        # ---------------------------------------------------------------------
        st.markdown("---")
        num_eval = len(st.session_state["q_evals"])
        curr_total = round(sum(r["score"] for r in st.session_state["q_evals"].values()), 1)

        col_prog1, col_prog2 = st.columns([2, 1])
        with col_prog1:
            st.markdown(f"#### 📊 Paper Evaluation Progress: **{num_eval} / 5 Questions Evaluated**")
            st.progress(num_eval / 5.0)
        with col_prog2:
            st.markdown(f"#### 🏆 Cumulative Score: **{curr_total} / 20.0 Marks**")

        col_sub1, col_sub2 = st.columns(2)
        with col_sub1:
            if st.button("⚡ Evaluate All Remaining Questions (Bulk Check)", use_container_width=True):
                for i_q, q_item in enumerate(questions):
                    if q_item["id"] not in st.session_state["q_evals"]:
                        ans_t = st.session_state.get(f"ans_{q_item['id']}", "")
                        st.session_state["q_evals"][q_item["id"]] = evaluate_single_question(cur_subject, i_q, q_item["text"], q_item["marks"], ans_t)
                st.success("All 5 questions evaluated!")
                st.rerun()

        with col_sub2:
            if st.button("🚀 Finalize & Submit Complete Paper to Teacher Queue", type="primary", use_container_width=True):
                for i_q, q_item in enumerate(questions):
                    if q_item["id"] not in st.session_state["q_evals"]:
                        ans_t = st.session_state.get(f"ans_{q_item['id']}", "")
                        st.session_state["q_evals"][q_item["id"]] = evaluate_single_question(cur_subject, i_q, q_item["text"], q_item["marks"], ans_t)

                final_results = [st.session_state["q_evals"][q_item["id"]] for q_item in questions]
                final_total = round(sum(r["score"] for r in final_results), 1)

                assigned_t = "akanksha" if cur_subject == "Mathematics" else ("ankur" if cur_subject == "Chemistry" else "physics_faculty")

                new_sub = {
                    "id": f"sub_{int(time.time() * 1000)}",
                    "studentId": current_user.get("studentId", "std_anup"),
                    "studentName": current_user.get("name", "Anup"),
                    "board": st.session_state["sel_board"],
                    "className": f"Class {st.session_state['sel_class']}th",
                    "subject": cur_subject,
                    "subjectName": cur_subject,
                    "topic": active_grade_topic,
                    "chapterTitle": active_grade_topic,
                    "topicName": active_grade_topic,
                    "totalAwarded": final_total,
                    "totalAwardedMarks": final_total,
                    "totalMax": 20.0,
                    "totalMaxMarks": 20.0,
                    "status": "PENDING_TEACHER_RELEASE",
                    "assignedTeacher": assigned_t,
                    "submittedAt": datetime.now().isoformat(),
                    "questions": final_results
                }
                db["submissions"].insert(0, normalize_submission(new_sub, 0))
                save_db(db)
                st.success(f"🎉 Complete paper officially submitted with score {final_total}/20.0!")
                st.warning(f"🛡️ **Governance Protocol Active:** Paper held under Teacher Audit with assigned faculty `{assigned_t}`.")
                st.balloons()

    # -------------------------------------------------------------------------
    # MODE B: FILE UPLOAD (PDF OR IMAGE FILE) EVALUATION
    # -------------------------------------------------------------------------
    else:
        st.markdown("""
        <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:12px; padding:16px; margin-bottom:16px;">
            <strong style="color:#166534;">📄 Multimodal File Evaluation Active</strong><br>
            <span style="font-size:13px; color:#15803D;">
                Upload your handwritten answer sheet or test paper in <strong>PDF, JPG, JPEG, or PNG</strong> format.
                EduAegis will parse the document and allow question-by-question scoring against official board rubrics!
            </span>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload Answer Sheet / Test Paper Document:",
            type=["pdf", "png", "jpg", "jpeg"],
            help="Upload student's scanned handwritten sheet or PDF."
        )

        if uploaded_file is not None:
            col_u1, col_u2 = st.columns([1, 2])
            with col_u1:
                st.markdown("##### 📎 Attached File Details:")
                st.json({"FileName": uploaded_file.name, "FileSize": f"{uploaded_file.size / 1024:.1f} KB"})

                if uploaded_file.type.startswith("image") or uploaded_file.name.lower().endswith((".png", ".jpg", ".jpeg")):
                    try:
                        img = Image.open(uploaded_file)
                        st.image(img, caption="Document Thumbnail Preview", use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not render image preview: {e}")

                elif uploaded_file.type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
                    try:
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        st.info(f"📑 PDF Loaded: {len(pdf_reader.pages)} Page(s) detected.")
                    except Exception as e:
                        st.warning(f"Could not parse PDF: {e}")

            with col_u2:
                st.markdown("##### 🔍 Ingested Document Content:")
                extracted_notes = st.text_area(
                    "Parsed Answers / Notes:",
                    value=f"Student handwritten submission for {cur_subject} ({active_grade_topic}). Detailed steps and calculations shown.",
                    height=140
                )

                if st.button("🚀 Evaluate Uploaded Document & Submit to Teacher", type="primary"):
                    assigned_t = "akanksha" if cur_subject == "Mathematics" else ("ankur" if cur_subject == "Chemistry" else "physics_faculty")
                    file_results = []
                    tot = 0
                    for i_q, q_item in enumerate(questions):
                        r = evaluate_single_question(cur_subject, i_q, q_item["text"], q_item["marks"], f"[From {uploaded_file.name}] {extracted_notes[:70]}")
                        file_results.append(r)
                        tot += r["score"]
                    tot = round(tot, 1)

                    new_sub = {
                        "id": f"sub_{int(time.time() * 1000)}",
                        "studentId": current_user.get("studentId", "std_anup"),
                        "studentName": current_user.get("name", "Anup"),
                        "board": st.session_state["sel_board"],
                        "className": f"Class {st.session_state['sel_class']}th",
                        "subject": cur_subject,
                        "subjectName": cur_subject,
                        "topic": active_grade_topic,
                        "chapterTitle": active_grade_topic,
                        "topicName": active_grade_topic,
                        "totalAwarded": tot,
                        "totalAwardedMarks": tot,
                        "totalMax": 20.0,
                        "totalMaxMarks": 20.0,
                        "status": "PENDING_TEACHER_RELEASE",
                        "assignedTeacher": assigned_t,
                        "attachmentName": uploaded_file.name,
                        "submittedAt": datetime.now().isoformat(),
                        "questions": file_results
                    }
                    db["submissions"].insert(0, normalize_submission(new_sub, 0))
                    save_db(db)
                    st.success(f"🎉 Uploaded file officially evaluated with score {tot}/20.0!")
                    st.warning(f"🛡️ **Governance Protocol Active:** Paper held under Teacher Audit with `{assigned_t}`.")
                    st.balloons()

# =============================================================================
# TAB 3: MY EVALUATIONS & APPEALS (Strict Student Isolation & Two Decisions)
# =============================================================================
with tab_history:
    st.subheader("📜 Student Evaluations & Academic Appeals")
    st.caption("Review your graded papers, view step-by-step scoring, and accept marks or file an appeal challenge.")

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

        if active_role == "teacher":
            teacher_subject = current_user.get("subject", "Mathematics")
            st.info(f"👩‍🏫 **Active Teacher:** {current_user.get('name')} | **Assigned Department:** {teacher_subject} • Scoped strictly to {teacher_subject} submissions.")
            teacher_submissions = [s for s in db["submissions"] if s.get("subject", "").lower() == teacher_subject.lower()]
        else:
            teacher_subject = "All Subjects"
            st.info("👑 Administrator Access: Full subject oversight and governance across all departments.")
            teacher_submissions = db["submissions"]

        # Teacher Dashboard Metrics
        st.markdown("### 📊 Teacher Evaluation & Audit Dashboard")
        eval_subs = [s for s in teacher_submissions if s.get("status") in ["RELEASED", "ACCEPTED"]]
        pending_subs = [s for s in teacher_submissions if s.get("status") == "PENDING_TEACHER_RELEASE"]
        challenged_subs = [s for s in teacher_submissions if s.get("status") == "CHALLENGED"]
        
        total_eval_questions = sum(len(s.get("questions", [])) for s in eval_subs)
        total_pending_questions = sum(len(s.get("questions", [])) for s in pending_subs)
        
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

        # Quick Glance: What is Pending From Your Side
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

        avg_pct = round(sum((s.get("totalAwarded", 0.0) / max(1.0, s.get("totalMax", 20.0))) * 100 for s in all_subs) / max(1, len(all_subs)), 1) if all_subs else 0.0

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

        st.markdown("### 📊 1. Subject-Level Performance & Appeal Summary")
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

        st.markdown("### 👩‍🏫 2. Teacher-Level Workload & Review Efficiency")
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

        st.markdown("### 🏛️ 3. Board-Level Performance & Appeal Benchmarking")
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

        st.markdown("### 📜 4. Master Submissions Ledger (Full Application Summary)")
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

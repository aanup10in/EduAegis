# 🛡️ EduAegis: Responsible AI Tutor & Subjective Grader (Class 9)

**EduAegis** is a fullstack AI tutoring and governed subjective evaluation platform tailored for secondary education (**Class 9th core**, with expansion to Classes 8 & 10). It benchmarks against modern platforms like [www.edcafe.ai](https://www.edcafe.ai) while introducing an end-to-end **AI Governance Framework** featuring **Human-in-the-Loop audit, controlled teacher mark release, and a student/parent challenge appeal system**.

> **Capstone Project for IIM Faculty Presentation**  
> **Deployment Ready:** 1-Click Vercel Deployment & Local Laptop Server with zero cloud lock-in.

---

## 🌟 Key Functional Highlights

### 1. Seamless Onboarding & Local Laptop Storage
- **First-Time User Experience**: Requests student details: **Full Name, Class (8/9/10), Academic Board (CBSE, ICSE, State Board), Email, Phone, and City/State**.
- **Persistent Local Database**: Stores student profiles, teacher instructions, submissions, and appeals in `eduaegis_data.json` on your laptop server.
- **1-Click Account Switcher**: Easily switch between saved student profiles (e.g. Aarav Sharma, Priya Patel).

### 2. Persistent Board Selection
- **Global Context Header**: The Board selector pill (`CBSE (All India)`, `ICSE`, `State Board`, `Cambridge`) is **permanently visible on top of every page**, dynamically tailoring curriculum standards.

### 3. Module 1: AI Subjective Tutor
- **Granular Curriculum Hierarchy**: Select Class ➔ Select Subject (Physics, Chemistry, Biology, Mathematics) ➔ Select Chapter ➔ Select Concept.
- **Plain English Pedagogy**: Explains complex physical mechanisms in simple, engaging English using everyday analogies (cricket ball impact, karate brick breaking, inertia of a moving bus).
- **Conversational Audio Narration**: Built-in speech synthesis teacher voice with play, pause, and speed controls (0.85x, 1.0x, 1.2x).
- **Multi-Modal Document & Video Ingestion**:
  - Ingests **PDF / Word study notes**.
  - Ingests **YouTube educational video links**, translating them into Class 9 concepts.
- **Socratic Mastery Check**: Interactive progressive example loop where students can confirm *"I Understood!"* or request *"Explain with another real-life example"*.
- **Direct Gateway to Grader**: 1-click button taking the student directly to the Grader with the chosen chapter pre-loaded.

### 4. Module 2: AI Subjective Grader
- **Pre-practice Solved Examples with Hidden Solutions**: Practice problems where detailed solutions are concealed by default and revealed only on-demand.
- **5-Question Subjective Paper**: Balanced 20-mark diagnostic test covering definitions, conceptual reasoning, and mathematical derivations.
- **1-Click Demo Buttons for Fast IIM Presentation**:
  - 🌟 **20/20 Exemplary Answer**
  - ⚖️ **12/20 Average Answer**
  - ⚠️ **5/20 Misconception Answer**
- **Verified References**: Every question links to authentic NCERT portals (`ncert.nic.in`), Khan Academy, and HyperPhysics.

### 5. The AI Governance Framework (The "Aegis" Shield)
1. **Teacher Directives (edcafe.ai Inspired)**: Teachers configure custom instructions (strict SI unit penalties, partial step credit, spelling tolerance).
2. **Controlled Release**: AI scores are initially placed in `PENDING_TEACHER_RELEASE`. Marks cannot be published without manual teacher approval.
3. **Teacher Mark Overrides & Comments**: Teachers can edit marks up or down, add custom feedback, and click **"Release Marks to Student"**.
4. **Student & Parent Appeal System**:
   - Once released, the student page presents two options:
     - **1 - I Accept**: Locks marks as final and archives them in the student's academic record.
     - **2 - I Challenge**: Allows student to check specific questions, write their detailed justification, and submit an appeal to the teacher's re-evaluation queue.

---

## 💻 Running EduAegis on Your Laptop (Local Server)

Your laptop acts as the primary web and database server:

```powershell
cd C:\Users\ADMIN\.gemini\antigravity\scratch\eduaegis
npm run dev
```

*Or simply double-click [`run_eduaegis.bat`](run_eduaegis.bat) on Windows.*

Open your browser at: **`http://localhost:3000`**

---

## 🚀 How to Deploy / Publish on Vercel

EduAegis is built with standard Next.js 16 and includes [`vercel.json`](vercel.json):

1. **Push to GitHub**:
   ```bash
   cd C:\Users\ADMIN\.gemini\antigravity\scratch\eduaegis
   git init
   git add .
   git commit -m "EduAegis Initial Commit"
   git remote add origin https://github.com/<your-username>/eduaegis.git
   git branch -M main
   git push -u origin main
   ```
2. **Deploy on Vercel**:
   - Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
   - Select your GitHub repository `eduaegis`.
   - Vercel automatically detects Next.js.
   - Click **"Deploy"**!
   - Your application will be live at `https://eduaegis.vercel.app` in under 60 seconds.

---

## 📊 IIM Faculty PowerPoint Presentation Deck

A PowerPoint deck (`.pptx`) has been generated in the project root:

📄 **File Location**:  
[`EduAegis_IIM_Capstone_Presentation.pptx`](EduAegis_IIM_Capstone_Presentation.pptx)

### Slide Deck Outline (11 Widescreen Slides):
- **Slide 1**: Title Slide (EduAegis: Responsible AI Tutor & Grader).
- **Slide 2**: Problem Statement in Indian K-12 (Cognitive fatigue, black-box AI risks).
- **Slide 3**: Product Vision & edcafe.ai Benchmarking.
- **Slide 4**: Module 1 — Socratic AI Tutor with Conversational Narration.
- **Slide 5**: Module 2 — Rigorous Step-by-Step Subjective Grader.
- **Slide 6**: The 4-Pillar AI Governance Framework.
- **Slide 7**: End-to-End System Workflow Architecture.
- **Slide 8**: Technology Stack & Hybrid Deployment Model (Vercel + Laptop Server).
- **Slide 9**: Strategic B2B Business Model & School Scalability.
- **Slide 10**: Live Prototype Walkthrough & Impact Metrics (82% time reduction).
- **Slide 11**: Ethical Alignment (NITI Aayog / UNESCO AI Ethics) & Q&A.

*(To regenerate the slides at any time, run: `python generate_eduaegis_presentation.py`)*

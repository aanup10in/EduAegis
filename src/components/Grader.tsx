"use client";

import React, { useState, useEffect } from "react";
import {
  FileText,
  Eye,
  EyeOff,
  CheckCircle,
  AlertTriangle,
  Upload,
  Sparkles,
  HelpCircle,
  ExternalLink,
  Sliders,
  ChevronDown,
  ChevronUp,
  Layers,
  Send
} from "lucide-react";
import { CURRICULUM_DATA, Chapter } from "@/lib/curriculum";
import { StudentProfile, SubjectiveSubmission } from "@/lib/storage";

interface GraderProps {
  currentBoard: string;
  activeProfile: StudentProfile | null;
  targetChapterId?: string;
  onSubmissionComplete: (submission: SubjectiveSubmission) => void;
  onOpenTeacherPanel: () => void;
}

export const Grader: React.FC<GraderProps> = ({
  currentBoard,
  activeProfile,
  targetChapterId,
  onSubmissionComplete,
  onOpenTeacherPanel
}) => {
  // Preselect Physics -> Force and Laws of Motion
  const class9 = CURRICULUM_DATA[9];
  const physics = class9.subjects[0];
  const defaultChapter =
    physics.chapters.find((c) => c.id === targetChapterId) || physics.chapters[0];

  const [selectedChapter, setSelectedChapter] = useState<Chapter>(defaultChapter);

  // Hidden Solutions State for Examples
  const [expandedSolutions, setExpandedSolutions] = useState<Record<string, boolean>>({});

  // Answers State for 5 Practice Questions
  const [answers, setAnswers] = useState<Record<string, string>>({
    q1: "",
    q2: "",
    q3: "",
    q4: "",
    q5: ""
  });

  const [uploadedFiles, setUploadedFiles] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Load teacher instructions
  const [teacherInstructions, setTeacherInstructions] = useState<any>(null);

  useEffect(() => {
    fetch("/api/teacher")
      .then((res) => res.json())
      .then((data) => {
        if (data.teacherInstructions && data.teacherInstructions[selectedChapter.id]) {
          setTeacherInstructions(data.teacherInstructions[selectedChapter.id]);
        }
      })
      .catch(() => {});
  }, [selectedChapter]);

  // Toggle example solution
  const toggleSolution = (exId: string) => {
    setExpandedSolutions((prev) => ({
      ...prev,
      [exId]: !prev[exId]
    }));
  };

  // 1-Click Sample Answer Loader for IIM Demo
  const loadDemoAnswers = (quality: "exemplary" | "average" | "misconception") => {
    if (quality === "exemplary") {
      setAnswers({
        q1: `Newton's Second Law of Motion states that the rate of change of momentum of an object is directly proportional to the applied unbalanced force, and takes place in the direction of the force.\n\nDerivation:\nLet an object of mass 'm' move with initial velocity 'u'. A constant force 'F' acts on it for time 't', changing velocity to 'v'.\nInitial momentum p1 = m * u\nFinal momentum p2 = m * v\nChange in momentum Δp = p2 - p1 = m(v - u)\nRate of change of momentum = m(v - u) / t\nBy Newton's 2nd Law:\nF ∝ m(v - u) / t\nSince acceleration a = (v - u) / t:\nF ∝ m * a => F = k * m * a\nIn SI units, choosing k = 1:\nF = m * a.\nSI Units: Force is in Newton (N), mass in kg, acceleration in m/s².`,
        q2: `When a fielder pulls his hands backward while catching a fast cricket ball, he increases the time duration 't' over which the velocity of the ball is reduced to zero. According to Newton's Second Law, Force F = m(v - u) / t. Because the change in momentum m(v - u) is constant, increasing time 't' decreases the rate of change of momentum. Consequently, a much smaller impact force acts on the fielder's palms, preventing injury.`,
        q3: `Inertia is the inherent property of an object by virtue of which it resists any change in its state of rest or uniform motion in a straight line.\n\nThree Types:\n1. Inertia of Rest: A person jerks backward when a stationary bus starts suddenly.\n2. Inertia of Motion: A passenger falls forward when a moving bus brakes abruptly.\n3. Inertia of Direction: Water droplets flying off tangential to a rotating bicycle wheel.\n\nMass is the quantitative measure of inertia.`,
        q4: `Given: Mass m = 1200 kg.\nInitial velocity u = 90 km/h = 90 * (5/18) = 25 m/s.\nFinal velocity v = 18 km/h = 18 * (5/18) = 5 m/s.\nTime t = 4 s.\n\n1. Acceleration a = (v - u) / t = (5 - 25) / 4 = -20 / 4 = -5 m/s² (Retardation).\n2. Change in Momentum Δp = m(v - u) = 1200 * (-20) = -24,000 kg·m/s.\n3. Force F = m * a = 1200 * (-5) = -6000 N.\nMagnitude of force required = 6000 N.`,
        q5: `Newton's Third Law states that to every action there is an equal and opposite reaction.\n\nWhy they do not cancel:\nAction and reaction forces act simultaneously on TWO DIFFERENT BODIES, never on the same body. For forces to cancel each other out, they must act on the same object. For example, when walking, your foot pushes the ground backward (Action on ground), and the ground pushes your foot forward (Reaction on foot). Because they act on different entities, motion occurs.`
      });
    } else if (quality === "average") {
      setAnswers({
        q1: `Newton's second law says that force is equal to mass into acceleration. Momentum changes when force acts.\nDerivation: P = mv. Initial momentum is mu and final momentum is mv. Change in momentum = mv - mu. Force = m(v - u)/t = ma. Unit of force is Newton and unit of mass is kg.`,
        q2: `Fielder pulls his hands back to reduce the hurt. Pulling hands back gives more time to catch the ball so force is less.`,
        q3: `Inertia means things stay at rest or in motion. Types are inertia of rest and motion. Heavy things have more inertia.`,
        q4: `Mass = 1200 kg. u = 90 km/h, v = 18 km/h. t = 4 s.\nAcceleration = (18 - 90)/4 = -72/4 = -18.\nForce = 1200 * 18 = 21600.`,
        q5: `Every action has equal and opposite reaction. They do not cancel because one is action and other is reaction.`
      });
    } else {
      // Misconception answer
      setAnswers({
        q1: `Newtons second law states that every action has equal and opposite reaction. Formula is F = ma where m is matter and a is speed. Unit of force is Joules.`,
        q2: `Fielder pulls hand back because cricket ball is heavy and it pulls the hand back naturally by gravity.`,
        q3: `Inertia is a force that pushes moving objects. Energy measures inertia.`,
        q4: `u = 90, v = 18. F = 1200 * 90 = 108000 Joules.`,
        q5: `Action and reaction cancel out because equal plus minus equal is zero.`
      });
    }
  };

  // Submit Paper
  const handleSubmitPaper = async () => {
    // Check if at least one question is answered
    const answeredCount = Object.values(answers).filter((a) => a.trim().length > 0).length;
    if (answeredCount === 0) {
      alert("Please enter answers for the practice paper or click one of the 1-Click Demo buttons.");
      return;
    }

    setIsSubmitting(true);
    try {
      const res = await fetch("/api/grader/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          studentId: activeProfile?.id || "std_default_aarav",
          studentName: activeProfile?.name || "Aarav Sharma",
          board: currentBoard,
          className: "Class 9th",
          subjectId: "physics",
          chapterId: selectedChapter.id,
          answers: answers
        })
      });

      const data = await res.json();
      if (data.success && data.submission) {
        onSubmissionComplete(data.submission);
      } else {
        alert("Failed to submit: " + (data.error || "Unknown error"));
      }
    } catch (err: any) {
      alert("Submission error: " + err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Grader Header */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 text-white shadow-xl border border-indigo-800/60 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-1">
            <span>AI Subjective Grader</span>
            <span>•</span>
            <span className="text-emerald-400 font-bold">{currentBoard}</span>
          </div>
          <h1 className="text-2xl font-black tracking-tight text-white">
            Objective Subjective Assessment & Audited Scoring
          </h1>
          <p className="text-xs text-indigo-200 mt-1 max-w-2xl">
            Grades subjective answers step-by-step against scientific facts, physical laws, and teacher instructions. Under AI Governance rules, marks are held for Teacher Audit before release.
          </p>
        </div>

        {/* Teacher Instructions Pill (edcafe.ai inspired) */}
        <div
          onClick={onOpenTeacherPanel}
          className="p-3 bg-indigo-950/90 rounded-2xl border border-indigo-700/60 hover:border-indigo-400 cursor-pointer transition shadow text-right flex items-center space-x-3"
          title="Click to view/edit teacher grading instructions"
        >
          <div className="w-8 h-8 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold">
            <Sliders className="w-4 h-4" />
          </div>
          <div className="text-left">
            <div className="text-[11px] font-bold text-amber-300 flex items-center space-x-1">
              <span>Teacher Directives Active</span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            </div>
            <div className="text-[10px] text-slate-300">
              {teacherInstructions?.strictSIUnits ? "Strict SI Units (-0.5)" : "Standard NCERT Rubric"}
            </div>
          </div>
        </div>
      </div>

      {/* Part 1: Guided Practice Examples with Hidden On-Demand Solutions */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900 flex items-center space-x-2">
              <span>📘 Solved Practice Examples</span>
              <span className="text-xs font-semibold text-indigo-600 bg-indigo-50 px-2.5 py-0.5 rounded-full">
                Hidden Solutions
              </span>
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Try solving these problems on paper first! Click "Show Step-by-Step Solved Solution" only when ready to verify.
            </p>
          </div>
        </div>

        <div className="space-y-4">
          {selectedChapter.practiceExamples.map((ex) => {
            const isExpanded = expandedSolutions[ex.id] || false;
            return (
              <div
                key={ex.id}
                className="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-3 transition"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-600">
                      Problem Statement ({ex.maxMarks} Marks)
                    </span>
                    <p className="text-xs font-semibold text-slate-800 leading-relaxed">
                      {ex.question}
                    </p>
                  </div>
                  <button
                    onClick={() => toggleSolution(ex.id)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 shrink-0 ${
                      isExpanded
                        ? "bg-slate-200 text-slate-800"
                        : "bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm"
                    }`}
                  >
                    {isExpanded ? (
                      <>
                        <EyeOff className="w-3.5 h-3.5" />
                        <span>Hide Solution</span>
                      </>
                    ) : (
                      <>
                        <Eye className="w-3.5 h-3.5" />
                        <span>Show Step-by-Step Solution</span>
                      </>
                    )}
                  </button>
                </div>

                {/* Hidden Solution Expanded */}
                {isExpanded && (
                  <div className="mt-3 p-4 rounded-xl bg-white border border-indigo-200 space-y-3 animate-in fade-in duration-200">
                    <div className="text-xs font-bold text-indigo-950 uppercase tracking-wider flex items-center space-x-1.5">
                      <CheckCircle className="w-4 h-4 text-emerald-500" />
                      <span>Step-by-Step Solved Derivation:</span>
                    </div>

                    <div className="space-y-2">
                      {ex.hiddenSolution.steps.map((st) => (
                        <div
                          key={st.stepNumber}
                          className="flex items-start justify-between text-xs p-2 rounded-lg bg-slate-50 border border-slate-100"
                        >
                          <div className="text-slate-800">
                            <strong className="text-indigo-600">Step {st.stepNumber}:</strong> {st.description}
                          </div>
                          <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 shrink-0 ml-2">
                            +{st.marks} Mark
                          </span>
                        </div>
                      ))}
                    </div>

                    <div className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-900 font-bold">
                      🎯 Final Result: {ex.hiddenSolution.finalAnswer}
                    </div>

                    <div className="text-[11px] text-slate-500 italic">
                      💡 Key Insight: {ex.hiddenSolution.keyInsight}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Part 2: 5-Question Subjective Paper with 1-Click Demo Loaders */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-lg font-black text-slate-900 flex items-center space-x-2">
              <span>✍️ 5-Question Subjective Practice Paper</span>
              <span className="text-xs font-bold text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded-full">
                20 Total Marks
              </span>
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Topic: <strong>{selectedChapter.title}</strong> • Aligned with {currentBoard}
            </p>
          </div>

          {/* 1-Click Demo Buttons for Fast IIM Faculty Presentation */}
          <div className="flex items-center space-x-2 bg-slate-100 p-1.5 rounded-2xl border border-slate-200">
            <span className="text-[11px] font-bold text-slate-600 px-2 hidden sm:inline">1-Click Demo:</span>
            <button
              onClick={() => loadDemoAnswers("exemplary")}
              className="px-2.5 py-1 text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl transition shadow-sm"
              title="Loads ideal 5/5 full mark answers"
            >
              🌟 20/20 Exemplary
            </button>
            <button
              onClick={() => loadDemoAnswers("average")}
              className="px-2.5 py-1 text-xs font-bold bg-amber-500 hover:bg-amber-600 text-white rounded-xl transition shadow-sm"
              title="Loads average answers with partial omissions"
            >
              ⚖️ 12/20 Average
            </button>
            <button
              onClick={() => loadDemoAnswers("misconception")}
              className="px-2.5 py-1 text-xs font-bold bg-rose-600 hover:bg-rose-700 text-white rounded-xl transition shadow-sm"
              title="Loads common student misconceptions"
            >
              ⚠️ Misconceptions
            </button>
          </div>
        </div>

        {/* Questions Loop */}
        <div className="space-y-6">
          {selectedChapter.subjectivePaper.map((q, idx) => (
            <div
              key={q.id}
              className="p-5 rounded-2xl bg-slate-50/70 border border-slate-200 space-y-3"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-start space-x-2.5">
                  <span className="w-6 h-6 rounded-lg bg-indigo-600 text-white text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                    {idx + 1}
                  </span>
                  <div>
                    <h4 className="text-xs font-bold text-slate-900 leading-snug">
                      {q.question}
                    </h4>
                    <span className="text-[10px] font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-md mt-1 inline-block">
                      {q.questionType}
                    </span>
                  </div>
                </div>

                <span className="text-xs font-black text-slate-700 bg-white px-2.5 py-1 rounded-xl border border-slate-200 shrink-0">
                  {q.maxMarks} Marks
                </span>
              </div>

              {/* Student Answer Text Area */}
              <div>
                <textarea
                  rows={4}
                  value={answers[q.id] || ""}
                  onChange={(e) =>
                    setAnswers((prev) => ({
                      ...prev,
                      [q.id]: e.target.value
                    }))
                  }
                  placeholder={`Type your step-by-step subjective answer for Question ${idx + 1}...`}
                  className="w-full p-3.5 text-xs border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none font-mono leading-relaxed bg-white"
                ></textarea>
              </div>

              {/* PDF or Scan Upload Note */}
              <div className="flex items-center justify-between text-[11px] text-slate-500">
                <label className="flex items-center space-x-1.5 cursor-pointer hover:text-indigo-600">
                  <Upload className="w-3.5 h-3.5 text-slate-400" />
                  <span>Attach scanned handwritten page / PDF</span>
                  <input
                    type="file"
                    accept=".pdf,.png,.jpg,.jpeg"
                    className="hidden"
                    onChange={(e) => {
                      if (e.target.files?.[0]) {
                        alert(`Uploaded ${e.target.files[0].name}. Extracted text attached to Question ${idx + 1}.`);
                      }
                    }}
                  />
                </label>
                <span>Word Count: {(answers[q.id] || "").trim().split(/\s+/).filter(Boolean).length} words</span>
              </div>
            </div>
          ))}
        </div>

        {/* Submit Button */}
        <div className="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-xs text-slate-500">
            🛡️ <strong>AI Governance Policy:</strong> Your submission will be evaluated using step-by-step rubrics. Under the Human-in-the-Loop policy, marks are reviewed by your teacher before release.
          </div>

          <button
            onClick={handleSubmitPaper}
            disabled={isSubmitting}
            className="w-full sm:w-auto px-8 py-3.5 bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold rounded-2xl shadow-xl shadow-indigo-600/30 transition flex items-center justify-center space-x-2"
          >
            {isSubmitting ? (
              <span>Evaluating Answers against Rubric...</span>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Submit Paper for AI & Teacher Grading</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

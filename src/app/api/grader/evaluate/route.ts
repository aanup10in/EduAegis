import { NextResponse } from "next/server";
import { getDatabase, saveDatabase, SubjectiveSubmission, QuestionGrading } from "@/lib/storage";
import { evaluateStudentAnswer } from "@/lib/evaluator";
import { CURRICULUM_DATA } from "@/lib/curriculum";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const {
      studentId,
      studentName,
      board,
      className,
      subjectId,
      chapterId,
      answers, // record of questionId -> studentAnswer
      teacherInstructionsOverride
    } = body;

    const db = getDatabase();

    // Look up chapter paper
    const class9 = CURRICULUM_DATA[9];
    const subject = class9.subjects.find(s => s.id === (subjectId || "physics"));
    const chapter = subject?.chapters.find(c => c.id === (chapterId || "force_and_laws"));

    if (!chapter) {
      return NextResponse.json({ error: "Chapter not found" }, { status: 404 });
    }

    const paper = chapter.subjectivePaper;
    const teacherInst = teacherInstructionsOverride || db.teacherInstructions[chapter.id];

    const gradedQuestions: QuestionGrading[] = [];
    let totalMax = 0;
    let totalAwarded = 0;

    for (const q of paper) {
      totalMax += q.maxMarks;
      const studentAnsText = answers[q.id] || "";

      const graded = evaluateStudentAnswer({
        questionId: q.id,
        questionText: q.question,
        studentAnswer: studentAnsText,
        maxMarks: q.maxMarks,
        modelAnswer: q.modelAnswer,
        rubricPoints: q.rubricPoints,
        referenceChapter: `${chapter.title} (${chapter.ncertChapter})`,
        authenticReferences: chapter.concepts[0]?.authenticReferences || [
          {
            title: "NCERT Official Textbook",
            url: "https://ncert.nic.in",
            source: "NCERT"
          }
        ],
        teacherInstruction: teacherInst,
        board: board || "CBSE (All India)"
      });

      gradedQuestions.push(graded);
      totalAwarded += graded.awardedMarks;
    }

    totalAwarded = Math.round(totalAwarded * 10) / 10;

    const submission: SubjectiveSubmission = {
      id: "sub_" + Date.now(),
      studentId: studentId || "std_default_aarav",
      studentName: studentName || "Aarav Sharma",
      board: board || "CBSE (All India)",
      className: className || "Class 9th",
      subjectName: subject?.name || "Physics",
      chapterTitle: chapter.title,
      topicName: chapter.title,
      submittedAt: new Date().toISOString(),
      totalMaxMarks: totalMax,
      totalAwardedMarks: totalAwarded,
      status: "PENDING_TEACHER_RELEASE", // AI Governance: Human-in-the-Loop release required
      teacherInstructionsUsed: teacherInst?.specificInstructions || "Default CBSE Rubrics",
      questions: gradedQuestions
    };

    db.submissions.unshift(submission);
    saveDatabase(db);

    return NextResponse.json({
      success: true,
      submission
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Evaluation failed" }, { status: 500 });
  }
}

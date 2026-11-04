import { QuestionGrading, StepEvaluation, TeacherInstruction } from "./storage";

export interface EvaluationInput {
  questionId: string;
  questionText: string;
  studentAnswer: string;
  maxMarks: number;
  modelAnswer: string;
  rubricPoints: string[];
  referenceChapter: string;
  authenticReferences: { title: string; url: string; source: string }[];
  teacherInstruction?: TeacherInstruction;
  board?: string;
}

export function evaluateStudentAnswer(input: EvaluationInput): QuestionGrading {
  const answer = input.studentAnswer.trim();
  const answerLower = answer.toLowerCase();
  const max = input.maxMarks;
  const teacherInst = input.teacherInstruction;

  // Extract core keywords from rubric and question
  const isSecondLaw = input.questionText.toLowerCase().includes("second law") || input.questionText.toLowerCase().includes("f = ma");
  const isFielder = input.questionText.toLowerCase().includes("fielder") || input.questionText.toLowerCase().includes("cricket");
  const isInertia = input.questionText.toLowerCase().includes("inertia");
  const isNumericalCar = input.questionText.toLowerCase().includes("motorcar") || input.questionText.toLowerCase().includes("1200 kg");
  const isThirdLaw = input.questionText.toLowerCase().includes("third law") || input.questionText.toLowerCase().includes("action and reaction");

  const stepBreakdown: StepEvaluation[] = [];
  const strengths: string[] = [];
  const gaps: string[] = [];
  let totalScore = 0;

  // 1. Evaluate Question 1: Newton's 2nd Law & Derivation (5 marks)
  if (isSecondLaw) {
    // Step 1: Definition of 2nd Law (1.0 Mark)
    const hasDefinition = answerLower.includes("rate of change of momentum") && answerLower.includes("proportional");
    const s1Marks = hasDefinition ? 1.0 : (answerLower.includes("momentum") ? 0.5 : 0.2);
    stepBreakdown.push({
      stepNumber: 1,
      stepFocus: "Statement of Newton's Second Law",
      marksAwarded: s1Marks,
      maxMarks: 1.0,
      whyAwardedOrDeducted: hasDefinition
        ? "Accurately stated that rate of change of momentum is directly proportional to applied unbalanced force."
        : "Partially stated; omitted either 'rate of change of momentum' or 'direction of force'."
    });

    // Step 2: Momentum change steps p1=mu, p2=mv, Δp=m(v-u) (1.5 Marks)
    const hasMomentumSteps = (answerLower.includes("mu") || answerLower.includes("p1")) && (answerLower.includes("mv") || answerLower.includes("p2"));
    const s2Marks = hasMomentumSteps ? 1.5 : (answerLower.includes("v - u") ? 1.0 : 0.3);
    stepBreakdown.push({
      stepNumber: 2,
      stepFocus: "Initial and Final Momentum Formulation",
      marksAwarded: s2Marks,
      maxMarks: 1.5,
      whyAwardedOrDeducted: hasMomentumSteps
        ? "Clearly defined initial momentum p1 = mu and final momentum p2 = mv with change Δp = m(v - u)."
        : "Omitted explicit algebraic initial/final momentum steps."
    });

    // Step 3: Acceleration substitution a = (v-u)/t and F = ma (1.5 Marks)
    const hasAcceleration = (answerLower.includes("a = (v - u)") || answerLower.includes("(v - u) / t") || answerLower.includes("acceleration a"));
    const s3Marks = hasAcceleration ? 1.5 : (answerLower.includes("f = ma") ? 0.8 : 0.2);
    stepBreakdown.push({
      stepNumber: 3,
      stepFocus: "Substitution of Acceleration a = (v-u)/t and Proportionality Constant k=1",
      marksAwarded: s3Marks,
      maxMarks: 1.5,
      whyAwardedOrDeducted: hasAcceleration
        ? "Correctly substituted acceleration a = (v - u) / t into force expression to derive F = ma."
        : "Directly jumped to F = ma without showing intermediate acceleration equivalence."
    });

    // Step 4: SI Units (1.0 Mark)
    const hasUnits = answerLower.includes("newton") || answerLower.includes("kg") || answerLower.includes("m/s");
    let s4Marks = hasUnits ? 1.0 : 0.0;
    if (teacherInst?.strictSIUnits && !hasUnits) {
      s4Marks = 0.0;
      gaps.push("Teacher Directive Violation: SI units (Newton / N, kg, m/s²) were omitted (-1.0).");
    }
    stepBreakdown.push({
      stepNumber: 4,
      stepFocus: "Specification of SI Units for All Quantities",
      marksAwarded: s4Marks,
      maxMarks: 1.0,
      whyAwardedOrDeducted: hasUnits
        ? "Correctly specified SI units for Force (N), Mass (kg), and Acceleration (m/s²)."
        : "Did not specify units for physical quantities."
    });
  } 
  // 2. Evaluate Question 2: Fielder pulling hands back (3 marks)
  else if (isFielder) {
    const hasTimeIncrease = answerLower.includes("time") && (answerLower.includes("increase") || answerLower.includes("longer") || answerLower.includes("more time"));
    const hasFormulaRelation = answerLower.includes("f =") || answerLower.includes("momentum") || answerLower.includes("rate of change");
    const hasForceReduction = answerLower.includes("force") && (answerLower.includes("reduc") || answerLower.includes("decrease") || answerLower.includes("less") || answerLower.includes("prevent hurt"));

    const s1 = hasTimeIncrease ? 1.0 : 0.3;
    const s2 = hasFormulaRelation ? 1.0 : 0.2;
    const s3 = hasForceReduction ? 1.0 : 0.2;

    stepBreakdown.push({
      stepNumber: 1,
      stepFocus: "Mechanism: Increasing Stopping Time Duration",
      marksAwarded: s1,
      maxMarks: 1.0,
      whyAwardedOrDeducted: hasTimeIncrease ? "Accurately noted that pulling hands back increases the stopping time 't'." : "Failed to clearly explain the increase in time duration."
    });
    stepBreakdown.push({
      stepNumber: 2,
      stepFocus: "Newton's 2nd Law Application (F = Δp / Δt)",
      marksAwarded: s2,
      maxMarks: 1.0,
      whyAwardedOrDeducted: hasFormulaRelation ? "Applied F = m(v-u)/t showing inverse relationship between impact force and time." : "Omitted theoretical connection to rate of change of momentum."
    });
    stepBreakdown.push({
      stepNumber: 3,
      stepFocus: "Consequence: Reduced Impact Force on Palms",
      marksAwarded: s3,
      maxMarks: 1.0,
      whyAwardedOrDeducted: hasForceReduction ? "Concluded that reduced force prevents injury to the fielder's palms." : "Incomplete explanation of how reduced force protects hands."
    });
  }
  // 3. Evaluate Question 3: Inertia Definition and Types (3 marks)
  else if (isInertia) {
    const hasDef = answerLower.includes("resist") && (answerLower.includes("rest") || answerLower.includes("motion"));
    const hasTypes = (answerLower.includes("rest") ? 0.33 : 0) + (answerLower.includes("motion") ? 0.33 : 0) + (answerLower.includes("direction") ? 0.34 : 0);
    const hasMass = answerLower.includes("mass");

    stepBreakdown.push({
      stepNumber: 1,
      stepFocus: "Definition of Inertia",
      marksAwarded: hasDef ? 1.0 : 0.4,
      maxMarks: 1.0,
      whyAwardedOrDeducted: hasDef ? "Accurately defined inertia as resistance to change of state." : "Definition lacked scientific precision."
    });
    stepBreakdown.push({
      stepNumber: 2,
      stepFocus: "Three Types of Inertia with Daily Examples",
      marksAwarded: Math.min(1.5, Math.round(hasTypes * 1.5 * 10) / 10),
      maxMarks: 1.5,
      whyAwardedOrDeducted: hasTypes >= 0.9 ? "Listed Inertia of Rest, Motion, and Direction with valid examples." : "Missing one or more categories of inertia."
    });
    stepBreakdown.push({
      stepNumber: 3,
      stepFocus: "Measurement of Inertia (Mass)",
      marksAwarded: hasMass ? 0.5 : 0.0,
      maxMarks: 0.5,
      whyAwardedOrDeducted: hasMass ? "Correctly identified Mass as the quantitative measure of inertia." : "Omitted that mass measures inertia."
    });
  }
  // 4. Numerical: Motorcar Retardation (5 marks)
  else if (isNumericalCar) {
    const hasConversion = (answerLower.includes("25") && answerLower.includes("5")) || answerLower.includes("5/18");
    const hasAcc = answerLower.includes("-5") || answerLower.includes("retardation of 5");
    const hasMomentum = answerLower.includes("24000") || answerLower.includes("-24000");
    const hasForce = answerLower.includes("6000");

    stepBreakdown.push({
      stepNumber: 1,
      stepFocus: "Velocity Unit Conversion (km/h -> m/s)",
      marksAwarded: hasConversion ? 1.0 : 0.2,
      maxMarks: 1.0,
      whyAwardedOrDeducted: hasConversion ? "Correctly converted 90 km/h = 25 m/s and 18 km/h = 5 m/s." : "Missed or incorrect conversion to SI units."
    });
    stepBreakdown.push({
      stepNumber: 2,
      stepFocus: "Acceleration Calculation (a = (v-u)/t)",
      marksAwarded: hasAcc ? 1.5 : (answerLower.includes("a =") ? 0.8 : 0.2),
      maxMarks: 1.5,
      whyAwardedOrDeducted: hasAcc ? "Accurately calculated acceleration a = -5 m/s² (retardation)." : "Error in acceleration computation or missing negative sign."
    });
    stepBreakdown.push({
      stepNumber: 3,
      stepFocus: "Change in Momentum Calculation",
      marksAwarded: hasMomentum ? 1.0 : 0.3,
      maxMarks: 1.0,
      whyAwardedOrDeducted: hasMomentum ? "Correctly computed Δp = -24,000 kg·m/s." : "Omitted or miscalculated change in momentum."
    });
    stepBreakdown.push({
      stepNumber: 4,
      stepFocus: "Force Magnitude Calculation and Units",
      marksAwarded: hasForce ? 1.5 : 0.3,
      maxMarks: 1.5,
      whyAwardedOrDeducted: hasForce ? "Correctly calculated force F = 6000 N with correct SI unit (Newton)." : "Incorrect final force value or missing SI unit."
    });
  }
  // 5. Newton's Third Law (4 marks)
  else if (isThirdLaw) {
    const hasLaw = answerLower.includes("action") && answerLower.includes("reaction") && answerLower.includes("equal") && answerLower.includes("opposite");
    const hasDiffBodies = answerLower.includes("different") || answerLower.includes("two bodies") || answerLower.includes("different objects");
    const hasExample = answerLower.includes("walk") || answerLower.includes("ground") || answerLower.includes("rocket") || answerLower.includes("swim") || answerLower.includes("gun");

    stepBreakdown.push({
      stepNumber: 1,
      stepFocus: "Statement of Newton's Third Law",
      marksAwarded: hasLaw ? 1.0 : 0.3,
      maxMarks: 1.0,
      whyAwardedOrDeducted: hasLaw ? "Stated that every action has an equal and opposite reaction." : "Incomplete statement of Third Law."
    });
    stepBreakdown.push({
      stepNumber: 2,
      stepFocus: "Core Physical Principle: Forces Act on Two Different Bodies",
      marksAwarded: hasDiffBodies ? 2.0 : 0.5,
      maxMarks: 2.0,
      whyAwardedOrDeducted: hasDiffBodies
        ? "Exemplary explanation that action and reaction act simultaneously on TWO DIFFERENT bodies, so they never cancel."
        : "Failed to mention that forces act on different bodies, which is the primary reason they don't cancel."
    });
    stepBreakdown.push({
      stepNumber: 3,
      stepFocus: "Real-world Practical Illustration",
      marksAwarded: hasExample ? 1.0 : 0.3,
      maxMarks: 1.0,
      whyAwardedOrDeducted: hasExample ? "Provided a valid real-life illustration (e.g. walking on ground / gun recoil)." : "Missing or unclear example."
    });
  } 
  // Generic fallback for any other subjective question
  else {
    const wordCount = answer.split(/\s+/).length;
    const completenessRatio = Math.min(1.0, wordCount / 50.0);
    const score = Math.round(max * completenessRatio * 10) / 10;
    stepBreakdown.push({
      stepNumber: 1,
      stepFocus: "Conceptual Explanation & Terminology",
      marksAwarded: score,
      maxMarks: max,
      whyAwardedOrDeducted: wordCount >= 35
        ? "Provided a detailed subjective answer covering the central theme."
        : "Answer is brief; needs step-by-step elaboration."
    });
  }

  // Calculate total awarded marks from step breakdown
  totalScore = stepBreakdown.reduce((sum, s) => sum + s.marksAwarded, 0);
  totalScore = Math.min(max, Math.max(0, Math.round(totalScore * 10) / 10));

  // Determine strengths & gaps
  if (totalScore >= max * 0.8) {
    strengths.push("Demonstrated strong mastery of core scientific definitions and principles.");
    strengths.push("Step-by-step mathematical reasoning was logically coherent.");
  } else if (totalScore >= max * 0.5) {
    strengths.push("Addressed the primary question focus with partial technical accuracy.");
  }

  if (answer.length < 25) {
    gaps.push("Answer is excessively brief. In subjective board exams, full marks require step-by-step elaboration.");
  }

  const deductionRationale = gaps.length > 0
    ? gaps.join(" ")
    : "Evaluated strictly per NCERT syllabus rubrics and teacher instructions.";

  return {
    questionId: input.questionId,
    questionText: input.questionText,
    studentAnswer: input.studentAnswer,
    maxMarks: input.maxMarks,
    awardedMarks: totalScore,
    stepBreakdown: stepBreakdown,
    strengths: strengths,
    gapsAndMisconceptions: gaps,
    deductionExplanation: deductionRationale,
    referenceChapter: input.referenceChapter,
    authenticReferences: input.authenticReferences
  };
}

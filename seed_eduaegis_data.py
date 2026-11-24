import json
import os

DB_PATH = r"C:\Users\ADMIN\.gemini\antigravity\scratch\eduaegis\eduaegis_data.json"

def create_seed_data():
    users = {
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

    students = [
        users["anup"],
        users["nandita"],
        {
            "id": "std_default_aarav",
            "name": "Aarav Sharma",
            "studentClass": 9,
            "board": "CBSE (All India)",
            "email": "aarav.sharma@school.edu",
            "phone": "+91 98765 43210",
            "cityState": "Bangalore, Karnataka"
        }
    ]

    teacher_instructions = {
        "mathematics": {
            "specificInstructions": "Strictly check intermediate algebraic steps and simplification. Deduct 0.5 for missing radical simplifications.",
            "strictSIUnits": False,
            "partialCreditForSteps": True,
            "lenientSpelling": True
        },
        "chemistry": {
            "specificInstructions": "Strictly verify scientific terminology (latent heat, kinetic energy, intermolecular forces). Deduct 0.5 for missing temperature/pressure units.",
            "strictSIUnits": True,
            "partialCreditForSteps": True,
            "lenientSpelling": True
        },
        "physics": {
            "specificInstructions": "Focus strictly on proper statement of Newton's 2nd Law (rate of change of momentum). Penalize 0.5 marks if SI units (N, kg, m/s²) are omitted.",
            "strictSIUnits": True,
            "partialCreditForSteps": True,
            "lenientSpelling": True
        }
    }

    submissions = [
        # 1. Anup - Mathematics (Released)
        {
            "id": "sub_anup_math_1",
            "studentId": "std_anup",
            "studentName": "Anup",
            "board": "CBSE (All India)",
            "className": "Class 9th",
            "subject": "Mathematics",
            "subjectName": "Mathematics",
            "topic": "Rational and Real Numbers",
            "chapterTitle": "Rational and Real Numbers",
            "topicName": "Rational and Real Numbers",
            "totalAwarded": 18.0,
            "totalAwardedMarks": 18.0,
            "totalMax": 20.0,
            "totalMaxMarks": 20.0,
            "status": "RELEASED",
            "submittedAt": "2026-11-20T10:15:00.000Z",
            "evaluatedAt": "2026-11-20T11:45:00.000Z",
            "evaluationTimeMins": 3.2,
            "assignedTeacher": "akanksha",
            "questions": [
                {
                    "question": "Show that 0.3333... can be expressed in the form p/q where p, q are integers and q ≠ 0.",
                    "questionText": "Show that 0.3333... can be expressed in the form p/q where p, q are integers and q ≠ 0.",
                    "max": 3.0,
                    "maxMarks": 3.0,
                    "score": 3.0,
                    "awardedMarks": 3.0,
                    "student_ans": "Let x = 0.333... Multiply by 10: 10x = 3.333... Subtracting: 9x = 3 => x = 3/9 = 1/3 in p/q form.",
                    "studentAnswer": "Let x = 0.333... Multiply by 10: 10x = 3.333... Subtracting: 9x = 3 => x = 3/9 = 1/3 in p/q form.",
                    "stepBreakdown": [
                        {"stepNumber": 1, "stepFocus": "Formulation & Multiplier 10", "marksAwarded": 1.5, "maxMarks": 1.5, "whyAwardedOrDeducted": "Correct algebraic setup."},
                        {"stepNumber": 2, "stepFocus": "Subtraction and Simplification", "marksAwarded": 1.5, "maxMarks": 1.5, "whyAwardedOrDeducted": "Accurate simplification to 1/3."}
                    ]
                },
                {
                    "question": "Rationalize the denominator of 1 / (7 + 3√2). Show intermediate steps.",
                    "questionText": "Rationalize the denominator of 1 / (7 + 3√2). Show intermediate steps.",
                    "max": 3.0,
                    "maxMarks": 3.0,
                    "score": 3.0,
                    "awardedMarks": 3.0,
                    "student_ans": "Multiply numerator and denominator by conjugate (7 - 3√2). Denominator: 7^2 - (3√2)^2 = 49 - 18 = 31. Result = (7 - 3√2) / 31.",
                    "studentAnswer": "Multiply numerator and denominator by conjugate (7 - 3√2). Denominator: 7^2 - (3√2)^2 = 49 - 18 = 31. Result = (7 - 3√2) / 31.",
                    "stepBreakdown": [
                        {"stepNumber": 1, "stepFocus": "Conjugate Multiplication", "marksAwarded": 1.5, "maxMarks": 1.5, "whyAwardedOrDeducted": "Correct conjugate."},
                        {"stepNumber": 2, "stepFocus": "Difference of Squares Simplification", "marksAwarded": 1.5, "maxMarks": 1.5, "whyAwardedOrDeducted": "Correct computation 49 - 18 = 31."}
                    ]
                },
                {
                    "question": "Find three rational numbers between 3/5 and 4/5.",
                    "questionText": "Find three rational numbers between 3/5 and 4/5.",
                    "max": 4.0,
                    "maxMarks": 4.0,
                    "score": 3.5,
                    "awardedMarks": 3.5,
                    "student_ans": "Equivalent fractions with denominator 50: 30/50 and 40/50. Numbers: 31/50, 32/50, 33/50.",
                    "studentAnswer": "Equivalent fractions with denominator 50: 30/50 and 40/50. Numbers: 31/50, 32/50, 33/50.",
                    "stepBreakdown": [
                        {"stepNumber": 1, "stepFocus": "Common Denominator Scaling", "marksAwarded": 2.0, "maxMarks": 2.0, "whyAwardedOrDeducted": "Appropriate scaling method."},
                        {"stepNumber": 2, "stepFocus": "Selection of Intermediate Values", "marksAwarded": 1.5, "maxMarks": 2.0, "whyAwardedOrDeducted": "Valid numbers selected; could simplify fractions."}
                    ]
                },
                {
                    "question": "Simplify using laws of exponents: (a) 2^(2/3)*2^(1/3), (b) (1/3^3)^7.",
                    "questionText": "Simplify using laws of exponents: (a) 2^(2/3)*2^(1/3), (b) (1/3^3)^7.",
                    "max": 5.0,
                    "maxMarks": 5.0,
                    "score": 4.5,
                    "awardedMarks": 4.5,
                    "student_ans": "(a) 2^(2/3 + 1/3) = 2^1 = 2. (b) (3^-3)^7 = 3^-21 = 1 / 3^21.",
                    "studentAnswer": "(a) 2^(2/3 + 1/3) = 2^1 = 2. (b) (3^-3)^7 = 3^-21 = 1 / 3^21.",
                    "stepBreakdown": [
                        {"stepNumber": 1, "stepFocus": "Product Rule of Exponents", "marksAwarded": 2.5, "maxMarks": 2.5, "whyAwardedOrDeducted": "Flawless power addition."},
                        {"stepNumber": 2, "stepFocus": "Power of a Power Rule", "marksAwarded": 2.0, "maxMarks": 2.5, "whyAwardedOrDeducted": "Correct law applied."}
                    ]
                },
                {
                    "question": "Classify as rational or irrational with justification: (i) 2 - √5, (ii) 2π.",
                    "questionText": "Classify as rational or irrational with justification: (i) 2 - √5, (ii) 2π.",
                    "max": 5.0,
                    "maxMarks": 5.0,
                    "score": 4.0,
                    "awardedMarks": 4.0,
                    "student_ans": "(i) 2 - √5 is irrational because difference of rational and irrational is irrational. (ii) 2π is irrational because product of non-zero rational and irrational is irrational.",
                    "studentAnswer": "(i) 2 - √5 is irrational because difference of rational and irrational is irrational. (ii) 2π is irrational because product of non-zero rational and irrational is irrational.",
                    "stepBreakdown": [
                        {"stepNumber": 1, "stepFocus": "Classification (i)", "marksAwarded": 2.0, "maxMarks": 2.5, "whyAwardedOrDeducted": "Correct reason."},
                        {"stepNumber": 2, "stepFocus": "Classification (ii)", "marksAwarded": 2.0, "maxMarks": 2.5, "whyAwardedOrDeducted": "Correct reason."}
                    ]
                }
            ]
        },
        # 2. Anup - Mathematics (Pending Audit)
        {
            "id": "sub_anup_math_2",
            "studentId": "std_anup",
            "studentName": "Anup",
            "board": "CBSE (All India)",
            "className": "Class 9th",
            "subject": "Mathematics",
            "subjectName": "Mathematics",
            "topic": "Laws of Exponents & Polynomials",
            "chapterTitle": "Laws of Exponents & Polynomials",
            "topicName": "Laws of Exponents & Polynomials",
            "totalAwarded": 15.0,
            "totalAwardedMarks": 15.0,
            "totalMax": 20.0,
            "totalMaxMarks": 20.0,
            "status": "PENDING_TEACHER_RELEASE",
            "submittedAt": "2026-11-24T09:30:00.000Z",
            "assignedTeacher": "akanksha",
            "questions": [
                {
                    "question": "Show that 0.3333... can be expressed in the form p/q where p, q are integers and q ≠ 0.",
                    "max": 3.0,
                    "score": 2.5,
                    "student_ans": "x = 0.333..., 10x = 3.333..., 9x = 3, so x = 1/3.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Algebraic Steps", "marksAwarded": 2.5, "maxMarks": 3.0, "whyAwardedOrDeducted": "Good steps."}]
                },
                {
                    "question": "Rationalize the denominator of 1 / (7 + 3√2). Show intermediate steps.",
                    "max": 3.0,
                    "score": 2.5,
                    "student_ans": "Multiply (7 - 3√2), denom = 49 - 18 = 31.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Conjugate", "marksAwarded": 2.5, "maxMarks": 3.0, "whyAwardedOrDeducted": "Solid."}]
                },
                {
                    "question": "Find three rational numbers between 3/5 and 4/5.",
                    "max": 4.0,
                    "score": 3.0,
                    "student_ans": "30/50, 40/50 => 31/50, 32/50, 33/50.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Scaling", "marksAwarded": 3.0, "maxMarks": 4.0, "whyAwardedOrDeducted": "Correct."}]
                },
                {
                    "question": "Simplify using laws of exponents: (a) 2^(2/3)*2^(1/3), (b) (1/3^3)^7.",
                    "max": 5.0,
                    "score": 3.5,
                    "student_ans": "2^1 = 2 and 3^-21.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Exponent Laws", "marksAwarded": 3.5, "maxMarks": 5.0, "whyAwardedOrDeducted": "Brief explanation."}]
                },
                {
                    "question": "Classify as rational or irrational with justification: (i) 2 - √5, (ii) 2π.",
                    "max": 5.0,
                    "score": 3.5,
                    "student_ans": "Both are irrational because operations with root5 and pi give irrational numbers.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Justification", "marksAwarded": 3.5, "maxMarks": 5.0, "whyAwardedOrDeducted": "Adequate."}]
                }
            ]
        },
        # 3. Anup - Chemistry (Challenged / Appealed)
        {
            "id": "sub_anup_chem_1",
            "studentId": "std_anup",
            "studentName": "Anup",
            "board": "CBSE (All India)",
            "className": "Class 9th",
            "subject": "Chemistry",
            "subjectName": "Chemistry",
            "topic": "Evaporation & Latent Heat Cooling",
            "chapterTitle": "Evaporation & Latent Heat Cooling",
            "topicName": "Evaporation & Latent Heat Cooling",
            "totalAwarded": 13.5,
            "totalAwardedMarks": 13.5,
            "totalMax": 20.0,
            "totalMaxMarks": 20.0,
            "status": "CHALLENGED",
            "submittedAt": "2026-11-22T14:20:00.000Z",
            "evaluatedAt": "2026-11-22T15:00:00.000Z",
            "evaluationTimeMins": 4.5,
            "assignedTeacher": "ankur",
            "challengeQuestions": ["Q2"],
            "challengeReason": "In Question 2, I explicitly described latent heat absorption by liquid molecules from the palm causing the cooling effect. Please review step 2 for partial credit.",
            "questions": [
                {
                    "question": "Define Evaporation. Explain four factors affecting evaporation with examples.",
                    "max": 5.0,
                    "score": 4.0,
                    "student_ans": "Evaporation is the transition of liquid into vapor below its boiling point. Factors: Surface area, temperature, humidity, and wind speed.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Definition & Factors", "marksAwarded": 4.0, "maxMarks": 5.0, "whyAwardedOrDeducted": "Well answered."}]
                },
                {
                    "question": "What is Latent Heat of Vaporization? Why does steam burn worse than boiling water?",
                    "max": 4.0,
                    "score": 1.5,
                    "student_ans": "Latent heat of vaporization is heat required to change liquid to vapor. Steam has higher energy than boiling water so it causes severe burns.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Latent Heat Definition & Extra Heat Content", "marksAwarded": 1.5, "maxMarks": 4.0, "whyAwardedOrDeducted": "Deducted 2.5 marks: Missed quantitative explanation of 22.5 x 10^5 J/kg extra energy stored."}]
                },
                {
                    "question": "Differentiate between Boiling and Evaporation on any three parameters.",
                    "max": 3.0,
                    "score": 3.0,
                    "student_ans": "1. Boiling is bulk, evaporation is surface. 2. Boiling occurs at specific temp, evaporation occurs at any temp. 3. Evaporation causes cooling.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "3 Parameters", "marksAwarded": 3.0, "maxMarks": 3.0, "whyAwardedOrDeducted": "All 3 points clear."}]
                },
                {
                    "question": "Convert 25°C to Kelvin and 373 K to Celsius. State the formula used.",
                    "max": 3.0,
                    "score": 2.5,
                    "student_ans": "T(K) = T(C) + 273. 25°C = 298 K. 373 K = 100°C.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Temperature Conversions", "marksAwarded": 2.5, "maxMarks": 3.0, "whyAwardedOrDeducted": "Accurate."}]
                },
                {
                    "question": "Why is ice at 273 K more effective in cooling than water at the same temperature?",
                    "max": 5.0,
                    "score": 2.5,
                    "student_ans": "Ice absorbs extra heat to melt so it cools better.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Latent Heat of Fusion", "marksAwarded": 2.5, "maxMarks": 5.0, "whyAwardedOrDeducted": "Missing mention of latent heat of fusion."}]
                }
            ]
        },
        # 4. Nandita - Chemistry (Accepted)
        {
            "id": "sub_nandita_chem_1",
            "studentId": "std_nandita",
            "studentName": "Nandita",
            "board": "ICSE / CISCE",
            "className": "Class 9th",
            "subject": "Chemistry",
            "subjectName": "Chemistry",
            "topic": "Matter in Our Surroundings",
            "chapterTitle": "Matter in Our Surroundings",
            "topicName": "Matter in Our Surroundings",
            "totalAwarded": 19.0,
            "totalAwardedMarks": 19.0,
            "totalMax": 20.0,
            "totalMaxMarks": 20.0,
            "status": "ACCEPTED",
            "submittedAt": "2026-11-19T11:00:00.000Z",
            "evaluatedAt": "2026-11-19T12:10:00.000Z",
            "evaluationTimeMins": 3.8,
            "assignedTeacher": "ankur",
            "questions": [
                {
                    "question": "Define Evaporation. Explain four factors affecting evaporation with examples.",
                    "max": 5.0,
                    "score": 5.0,
                    "student_ans": "Evaporation is a surface phenomenon where liquid turns to vapor below boiling point. Factors: 1. Surface area (spreading clothes), 2. Temperature (hot summer days), 3. Humidity (dry vs rainy days), 4. Wind speed (fan drying).",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Definition & Factors", "marksAwarded": 5.0, "maxMarks": 5.0, "whyAwardedOrDeducted": "Exemplary answer."}]
                },
                {
                    "question": "What is Latent Heat of Vaporization? Why does steam burn worse than boiling water?",
                    "max": 4.0,
                    "score": 4.0,
                    "student_ans": "Latent heat of vaporization is the amount of heat energy required to change 1 kg of liquid into gas at atmospheric pressure at its boiling point. Steam has absorbed additional latent heat of 2.26 x 10^6 J/kg, which is released upon contact with skin.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Latent Heat & Energy Difference", "marksAwarded": 4.0, "maxMarks": 4.0, "whyAwardedOrDeducted": "Comprehensive and mathematically sound."}]
                },
                {
                    "question": "Differentiate between Boiling and Evaporation on any three parameters.",
                    "max": 3.0,
                    "score": 3.0,
                    "student_ans": "1. Bulk vs Surface. 2. Constant boiling point vs Any temperature. 3. External heat required vs Absorbs heat causing cooling.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Comparison", "marksAwarded": 3.0, "maxMarks": 3.0, "whyAwardedOrDeducted": "Perfect comparison table."}]
                },
                {
                    "question": "Convert 25°C to Kelvin and 373 K to Celsius. State the formula used.",
                    "max": 3.0,
                    "score": 3.0,
                    "student_ans": "K = °C + 273.15. 25°C = 298.15 K. 373 K = 99.85°C (or 100°C with 273).",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Calculations", "marksAwarded": 3.0, "maxMarks": 3.0, "whyAwardedOrDeducted": "Accurate."}]
                },
                {
                    "question": "Why is ice at 273 K more effective in cooling than water at the same temperature?",
                    "max": 5.0,
                    "score": 4.0,
                    "student_ans": "Ice at 273 K has less heat content than water at 273 K because it needs to absorb latent heat of fusion (3.34 x 10^5 J/kg) to melt, thus pulling more heat from the substance.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Latent Heat of Fusion", "marksAwarded": 4.0, "maxMarks": 5.0, "whyAwardedOrDeducted": "Accurate."}]
                }
            ]
        },
        # 5. Nandita - Chemistry (Pending Audit)
        {
            "id": "sub_nandita_chem_2",
            "studentId": "std_nandita",
            "studentName": "Nandita",
            "board": "ICSE / CISCE",
            "className": "Class 9th",
            "subject": "Chemistry",
            "subjectName": "Chemistry",
            "topic": "States of Matter & Phase Transitions",
            "chapterTitle": "States of Matter & Phase Transitions",
            "topicName": "States of Matter & Phase Transitions",
            "totalAwarded": 14.5,
            "totalAwardedMarks": 14.5,
            "totalMax": 20.0,
            "totalMaxMarks": 20.0,
            "status": "PENDING_TEACHER_RELEASE",
            "submittedAt": "2026-11-24T10:05:00.000Z",
            "assignedTeacher": "ankur",
            "questions": [
                {
                    "question": "Define Evaporation. Explain four factors affecting evaporation with examples.",
                    "max": 5.0,
                    "score": 3.5,
                    "student_ans": "Evaporation is liquid becoming gas. Factors are heat, wind, area, and humidity.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Factors", "marksAwarded": 3.5, "maxMarks": 5.0, "whyAwardedOrDeducted": "Good."}]
                },
                {
                    "question": "What is Latent Heat of Vaporization? Why does steam burn worse than boiling water?",
                    "max": 4.0,
                    "score": 3.0,
                    "student_ans": "Heat needed for phase change without temperature rise. Steam gives off latent heat.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Latent Heat", "marksAwarded": 3.0, "maxMarks": 4.0, "whyAwardedOrDeducted": "Clear."}]
                },
                {
                    "question": "Differentiate between Boiling and Evaporation on any three parameters.",
                    "max": 3.0,
                    "score": 2.5,
                    "student_ans": "Boiling is bulk, evaporation is surface.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Contrast", "marksAwarded": 2.5, "maxMarks": 3.0, "whyAwardedOrDeducted": "Adequate."}]
                },
                {
                    "question": "Convert 25°C to Kelvin and 373 K to Celsius. State the formula used.",
                    "max": 3.0,
                    "score": 2.5,
                    "student_ans": "298 K and 100 C using T + 273.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Conversion", "marksAwarded": 2.5, "maxMarks": 3.0, "whyAwardedOrDeducted": "Correct."}]
                },
                {
                    "question": "Why is ice at 273 K more effective in cooling than water at the same temperature?",
                    "max": 5.0,
                    "score": 3.0,
                    "student_ans": "Ice absorbs latent heat of fusion from surroundings.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Fusion", "marksAwarded": 3.0, "maxMarks": 5.0, "whyAwardedOrDeducted": "Good."}]
                }
            ]
        },
        # 6. Nandita - Mathematics (Challenged / Appealed)
        {
            "id": "sub_nandita_math_1",
            "studentId": "std_nandita",
            "studentName": "Nandita",
            "board": "ICSE / CISCE",
            "className": "Class 9th",
            "subject": "Mathematics",
            "subjectName": "Mathematics",
            "topic": "Rationalizing the Denominator",
            "chapterTitle": "Rationalizing the Denominator",
            "topicName": "Rationalizing the Denominator",
            "totalAwarded": 12.0,
            "totalAwardedMarks": 12.0,
            "totalMax": 20.0,
            "totalMaxMarks": 20.0,
            "status": "CHALLENGED",
            "submittedAt": "2026-11-21T16:40:00.000Z",
            "evaluatedAt": "2026-11-21T17:30:00.000Z",
            "evaluationTimeMins": 4.1,
            "assignedTeacher": "akanksha",
            "challengeQuestions": ["Q2"],
            "challengeReason": "In Q2, my intermediate conjugate expression was (7 - 3√2)/31 which matches the textbook answer. Please recheck.",
            "questions": [
                {
                    "question": "Show that 0.3333... can be expressed in the form p/q where p, q are integers and q ≠ 0.",
                    "max": 3.0,
                    "score": 2.5,
                    "student_ans": "x = 0.333... 10x = 3.333... 9x = 3 => x = 1/3.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Derivation", "marksAwarded": 2.5, "maxMarks": 3.0, "whyAwardedOrDeducted": "Correct."}]
                },
                {
                    "question": "Rationalize the denominator of 1 / (7 + 3√2). Show intermediate steps.",
                    "max": 3.0,
                    "score": 1.0,
                    "student_ans": "Multiplied (7 - 3√2) to both numerator and denominator. Denom = 49 - 18 = 31.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Steps", "marksAwarded": 1.0, "maxMarks": 3.0, "whyAwardedOrDeducted": "Deducted 2 marks: Final single line fraction not clearly boxed."}]
                },
                {
                    "question": "Find three rational numbers between 3/5 and 4/5.",
                    "max": 4.0,
                    "score": 3.0,
                    "student_ans": "30/50, 40/50 gives 31/50, 32/50, 33/50.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Rational numbers", "marksAwarded": 3.0, "maxMarks": 4.0, "whyAwardedOrDeducted": "Good."}]
                },
                {
                    "question": "Simplify using laws of exponents: (a) 2^(2/3)*2^(1/3), (b) (1/3^3)^7.",
                    "max": 5.0,
                    "score": 2.5,
                    "student_ans": "2^(3/3) = 2. (3^-3)^7 = 3^-21.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Exponents", "marksAwarded": 2.5, "maxMarks": 5.0, "whyAwardedOrDeducted": "Accurate."}]
                },
                {
                    "question": "Classify as rational or irrational with justification: (i) 2 - √5, (ii) 2π.",
                    "max": 5.0,
                    "score": 3.0,
                    "student_ans": "Both are irrational.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Classification", "marksAwarded": 3.0, "maxMarks": 5.0, "whyAwardedOrDeducted": "Minimal justification."}]
                }
            ]
        },
        # 7. Aarav Sharma - Physics (for cross-subject completeness)
        {
            "id": "sub_aarav_phys_1",
            "studentId": "std_default_aarav",
            "studentName": "Aarav Sharma",
            "board": "CBSE (All India)",
            "className": "Class 9th",
            "subject": "Physics",
            "subjectName": "Physics",
            "topic": "Force and Laws of Motion",
            "chapterTitle": "Force and Laws of Motion",
            "topicName": "Force and Laws of Motion",
            "totalAwarded": 16.5,
            "totalAwardedMarks": 16.5,
            "totalMax": 20.0,
            "totalMaxMarks": 20.0,
            "status": "RELEASED",
            "submittedAt": "2026-11-21T09:00:00.000Z",
            "evaluatedAt": "2026-11-21T10:15:00.000Z",
            "evaluationTimeMins": 3.9,
            "assignedTeacher": "physics_faculty",
            "questions": [
                {
                    "question": "State Newton's Second Law of Motion. Derive the formula F = ma defining all SI units.",
                    "max": 5.0,
                    "score": 4.5,
                    "student_ans": "Newton's 2nd Law states rate of change of momentum is proportional to applied force. p1=mu, p2=mv, F = k*m(v-u)/t = ma. Force in N, mass in kg, acc in m/s².",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Law Statement and Derivation", "marksAwarded": 4.5, "maxMarks": 5.0, "whyAwardedOrDeducted": "Well formulated."}]
                },
                {
                    "question": "Why does a fielder pull his hands backward while catching a fast cricket ball?",
                    "max": 3.0,
                    "score": 3.0,
                    "student_ans": "Fielder pulls hands back to increase stopping time t. As F = Δp/t, increasing t reduces impact force on palms.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Time-Force Relationship", "marksAwarded": 3.0, "maxMarks": 3.0, "whyAwardedOrDeducted": "Accurate mechanism."}]
                },
                {
                    "question": "Define Inertia. Name its three types with daily-life examples and state its measure.",
                    "max": 3.0,
                    "score": 2.5,
                    "student_ans": "Inertia is resistance to change of state. Rest, motion, direction. Mass is its measure.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Inertia Types & Mass", "marksAwarded": 2.5, "maxMarks": 3.0, "whyAwardedOrDeducted": "Good."}]
                },
                {
                    "question": "A 1200 kg car slows from 90 km/h to 18 km/h in 4 s. Calculate acceleration and force.",
                    "max": 5.0,
                    "score": 4.0,
                    "student_ans": "u = 25 m/s, v = 5 m/s. a = (5 - 25)/4 = -5 m/s². Force = 1200 * (-5) = -6000 N.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "SI conversions and Force", "marksAwarded": 4.0, "maxMarks": 5.0, "whyAwardedOrDeducted": "Accurate."}]
                },
                {
                    "question": "State Newton's Third Law. Why do action and reaction forces not cancel each other?",
                    "max": 4.0,
                    "score": 2.5,
                    "student_ans": "Action and reaction are equal and opposite. They act on two different bodies.",
                    "stepBreakdown": [{"stepNumber": 1, "stepFocus": "Newton's 3rd Law & Different Bodies", "marksAwarded": 2.5, "maxMarks": 4.0, "whyAwardedOrDeducted": "Correct explanation."}]
                }
            ]
        }
    ]

    data = {
        "users": users,
        "students": students,
        "teacherInstructions": teacher_instructions,
        "submissions": submissions
    }

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully seeded {len(users)} users and {len(submissions)} submissions to {DB_PATH}")

if __name__ == "__main__":
    create_seed_data()

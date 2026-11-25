import os
import json
import streamlit_app

def test_enhancements():
    # 1. Test evaluate_single_question for all subjects and all 5 questions
    subjects = ["Physics", "Chemistry", "Mathematics"]
    sample_answers = {
        "Physics": [
            "Newton's Second Law states that rate of change of momentum is proportional to applied force in direction of force. p1=mu, p2=mv, Delta p = m(v-u). Rate=ma, F=ma. Units: Force in N, mass in kg, acc in m/s2.",
            "Fielder pulls hands back to increase stopping time t. Since F = m(v-u)/t, increasing time decreases the rate of change of momentum, reducing impact force on palms.",
            "Inertia is property resisting change of rest or motion. Types: rest, motion, direction. Mass measures inertia.",
            "u = 25 m/s, v = 5 m/s. a = (5-25)/4 = -5 m/s2 (retardation). Force = 1200*(-5) = -6000 N.",
            "Action and reaction are equal and opposite. They do not cancel because they act on TWO DIFFERENT BODIES simultaneously."
        ],
        "Chemistry": [
            "Evaporation is liquid turning to vapor below boiling point. Factors: surface area, temperature, humidity, wind speed.",
            "Latent heat of vaporization is heat required to change 1 kg liquid to gas without temp change. Steam contains extra latent heat released on skin.",
            "Evaporation is surface phenomenon below boiling point causing cooling; boiling is bulk phenomenon at boiling point.",
            "T(K) = T(C) + 273. 25 C = 298 K. 373 K = 100 C.",
            "Ice at 273 K absorbs latent heat of fusion (3.34x10^5 J/kg) to melt, extracting more heat than water at 0 C."
        ],
        "Mathematics": [
            "Let x = 0.333... 10x = 3.333... Subtract: 9x = 3 => x = 1/3.",
            "Multiply conjugate (7 - 3 root 2) / (49 - 18) = (7 - 3 root 2) / 31.",
            "3/5 = 30/50, 4/5 = 40/50. Numbers: 31/50, 32/50, 33/50.",
            "2^(2/3+1/3) = 2^1 = 2. (3^-3)^7 = 1/3^21.",
            "2 - root 5 is irrational (rational minus irrational). 2 pi is irrational."
        ]
    }

    print("[TEST 1] Testing Question-by-Question Evaluation Engine:")
    for subj in subjects:
        total = 0
        for idx in range(5):
            ans = sample_answers[subj][idx]
            q_text = f"Sample question {idx+1} for {subj}"
            q_max = 5.0 if idx in [0, 3, 4] else 3.0
            res = streamlit_app.evaluate_single_question(subj, idx, q_text, q_max, ans)
            assert res["score"] > 0, f"Score should be > 0 for {subj} Q{idx+1}"
            assert len(res["stepBreakdown"]) == 2, f"Should have 2 steps for {subj} Q{idx+1}"
            total += res["score"]
        print(f"  [OK] {subj} 5 questions evaluated successfully! Total score: {total}/20.0")

    print("\n[TEST 2] Testing Blank / Partial Answer Handling:")
    blank_res = streamlit_app.evaluate_single_question("Physics", 0, "Newton Law", 5.0, "")
    assert blank_res["score"] == 0.0, "Blank answer should score 0"
    assert "blank" in blank_res["deductionExplanation"].lower(), "Should mention blank"
    print("  [OK] Blank answer correctly scored 0 with clear feedback.")

    partial_res = streamlit_app.evaluate_single_question("Physics", 0, "Newton Law", 5.0, "Force is mass into acceleration")
    assert 0 < partial_res["score"] < 5.0, "Partial answer should score between 0 and 5"
    print(f"  [OK] Partial answer correctly scored {partial_res['score']} / 5.0 with step breakdown.")

    print("\n[TEST 3] Testing RBAC and Database Persistence:")
    db = streamlit_app.load_db()
    assert "users" in db and "anup" in db["users"] and "nandita" in db["users"]
    assert "akanksha" in db["users"] and "ankur" in db["users"] and "admin" in db["users"]
    print("  [OK] All 5 user personas verified in database.")

    print("\nALL ENHANCEMENT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_enhancements()

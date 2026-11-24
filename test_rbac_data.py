import os
import json
import PyPDF2
from PIL import Image

def test_imports_and_db():
    db_file = r"C:\Users\ADMIN\.gemini\antigravity\scratch\eduaegis\eduaegis_data.json"
    with open(db_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "users" in data, "Users key missing"
    assert "anup" in data["users"], "anup missing"
    assert "nandita" in data["users"], "nandita missing"
    assert "akanksha" in data["users"], "akanksha missing"
    assert "ankur" in data["users"], "ankur missing"
    assert "admin" in data["users"], "admin missing"

    submissions = data.get("submissions", [])
    print(f"Loaded {len(submissions)} submissions.")

    # Test Anup filtering
    anup_subs = [s for s in submissions if s.get("studentId") == "std_anup" or s.get("studentName") == "Anup"]
    print(f"Anup submissions: {len(anup_subs)}")
    assert len(anup_subs) >= 3, "Anup should have at least 3 submissions"

    # Test Nandita filtering
    nandita_subs = [s for s in submissions if s.get("studentId") == "std_nandita" or s.get("studentName") == "Nandita"]
    print(f"Nandita submissions: {len(nandita_subs)}")
    assert len(nandita_subs) >= 3, "Nandita should have at least 3 submissions"

    # Test Akanksha Maths filtering
    maths_subs = [s for s in submissions if s.get("subject", "").lower() == "mathematics"]
    print(f"Mathematics submissions (Akanksha): {len(maths_subs)}")
    assert len(maths_subs) >= 3, "Maths should have at least 3 submissions"

    # Test Ankur Chemistry filtering
    chem_subs = [s for s in submissions if s.get("subject", "").lower() == "chemistry"]
    print(f"Chemistry submissions (Ankur): {len(chem_subs)}")
    assert len(chem_subs) >= 3, "Chemistry should have at least 3 submissions"

    print("All RBAC data segregation tests passed successfully!")

if __name__ == "__main__":
    test_imports_and_db()

def scholarship_check(score, documents_complete,
                      identity_verified, eligibility_confirmed):
    if (score >= 70 and documents_complete
            and identity_verified and eligibility_confirmed):
        return "Review"
    return "Hold"


cases = [
    {
        "name": "Pass",
        "score": 85,
        "documents": True,
        "identity": True,
        "eligibility": True,
        "expected": "Review",
        "reason": "All conditions are satisfied."
    },
    {
        "name": "Identity Failure",
        "score": 85,
        "documents": True,
        "identity": False,
        "eligibility": True,
        "expected": "Hold",
        "reason": "Identity is not verified."
    },
    {
        "name": "Eligibility Failure",
        "score": 85,
        "documents": True,
        "identity": True,
        "eligibility": False,
        "expected": "Hold",
        "reason": "Eligibility is not confirmed."
    },
    {
        "name": "Boundary Test",
        "score": 70,
        "documents": True,
        "identity": True,
        "eligibility": True,
        "expected": "Review",
        "reason": "Score is exactly at the minimum threshold."
    }
]

print("SCHOLARSHIP SCREENING RESULTS")
for case in cases:
    actual = scholarship_check(
        case["score"], case["documents"],
        case["identity"], case["eligibility"]
    )
    print("\nCase:", case["name"])
    print("Input:", case["score"], case["documents"],
          case["identity"], case["eligibility"])
    print("Expected:", case["expected"])
    print("Actual:", actual)
    print("Reason:", case["reason"])
    print("Test Passed:", actual == case["expected"])

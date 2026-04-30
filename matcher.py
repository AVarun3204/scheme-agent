import json

def load_schemes():
    with open("schemes.json", "r", encoding="utf-8") as f:
        return json.load(f)

def match_schemes(user_profile):
    schemes = load_schemes()
    matched = []

    for scheme in schemes:
        e = scheme["eligibility"]
        skip = False

        if "state" in e:
            if user_profile.get("state", "").lower() != e["state"].lower():
                skip = True

        if "occupation" in e:
            if user_profile.get("occupation", "").lower() != e["occupation"].lower():
                skip = True

        if "min_age" in e:
            if user_profile.get("age", 0) < e["min_age"]:
                skip = True

        if "max_age" in e:
            if user_profile.get("age", 999) > e["max_age"]:
                skip = True

        if "max_annual_income" in e:
            if user_profile.get("annual_income", 999999) > e["max_annual_income"]:
                skip = True

        if "gender" in e:
            if user_profile.get("gender", "").lower() != e["gender"].lower():
                skip = True

        if e.get("bpl_required"):
            if not user_profile.get("is_bpl"):
                skip = True

        if e.get("must_own_land"):
            if not user_profile.get("owns_land"):
                skip = True

        if e.get("enrolled_in_college"):
            if not user_profile.get("enrolled_in_college"):
                skip = True

        if not skip:
            matched.append(scheme)

    return matched


if __name__ == "__main__":
    test_profile = {
        "age": 42,
        "gender": "male",
        "state": "telangana",
        "occupation": "farmer",
        "annual_income": 80000,
        "is_bpl": True,
        "owns_land": True,
        "has_bank_account": True,
        "enrolled_in_college": False
    }

    results = match_schemes(test_profile)
    print(f"\nFound {len(results)} matching schemes:\n")
    for scheme in results:
        print(f"  - {scheme['name']}")
        print(f"    Benefit: {scheme['benefit']}")
        print(f"    Apply: {scheme['apply_link']}")
        print()
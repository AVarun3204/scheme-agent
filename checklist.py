# Document checklist generator - tells users exactly how to get each document

DOCUMENT_GUIDE = {
    "Aadhaar card": {
        "description": "12-digit unique identity number issued by UIDAI",
        "how_to_get": "Visit nearest Aadhaar enrollment center or post office",
        "time_needed": "7-15 days after enrollment",
        "cost": "Free",
        "link": "https://uidai.gov.in",
        "tip": "If you already have Aadhaar, download e-Aadhaar free from uidai.gov.in"
    },
    "Ration card": {
        "description": "Card issued by state government for subsidized food grains",
        "how_to_get": "Apply at nearest Tahsildar office or Food & Civil Supplies office",
        "time_needed": "15-30 days",
        "cost": "Free or small fee depending on state",
        "link": "https://nfsa.gov.in",
        "tip": "Carry Aadhaar, family photo, and address proof when applying"
    },
    "Income certificate": {
        "description": "Official document certifying your annual family income",
        "how_to_get": "Apply at nearest Tahsildar/Revenue office or MeeSeva center in Telangana",
        "time_needed": "7-15 days",
        "cost": "Rs 10-50 depending on state",
        "link": "https://meeseva.telangana.gov.in",
        "tip": "In Telangana you can apply online through MeeSeva portal"
    },
    "BPL certificate": {
        "description": "Below Poverty Line certificate proving economic status",
        "how_to_get": "Apply at Gram Panchayat office or nearest government office",
        "time_needed": "15-30 days",
        "cost": "Free",
        "link": "https://nfsa.gov.in",
        "tip": "Check if your name is in SECC 2011 list first at nfsa.gov.in"
    },
    "Land ownership documents": {
        "description": "Documents proving you own agricultural land",
        "how_to_get": "Get from Tahsildar office or Revenue department",
        "time_needed": "Available immediately if you own land",
        "cost": "Small fee for certified copy",
        "link": "https://dharani.telangana.gov.in",
        "tip": "In Telangana, download your land records free from dharani.telangana.gov.in"
    },
    "Bank account details": {
        "description": "Your bank account number and IFSC code",
        "how_to_get": "Check your passbook or online banking app",
        "time_needed": "Immediate if you have account",
        "cost": "Free",
        "link": "https://www.jandhanyojana.net",
        "tip": "If no bank account, open free Jan Dhan account at any bank with just Aadhaar"
    },
    "PAN card": {
        "description": "Permanent Account Number card for tax purposes",
        "how_to_get": "Apply online at incometax.gov.in or through NSDL/UTIITSL",
        "time_needed": "10-15 days",
        "cost": "Rs 107 online",
        "link": "https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html",
        "tip": "You can get instant e-PAN free if you have Aadhaar linked mobile number"
    },
    "Land passbook": {
        "description": "Pattadar passbook showing land ownership in Telangana",
        "how_to_get": "Visit nearest MeeSeva or revenue office",
        "time_needed": "Available immediately if you own land",
        "cost": "Small fee",
        "link": "https://dharani.telangana.gov.in",
        "tip": "Download and verify your land details at dharani.telangana.gov.in"
    },
    "College admission letter": {
        "description": "Letter from college confirming your enrollment",
        "how_to_get": "Get from your college administrative office",
        "time_needed": "Immediate",
        "cost": "Free",
        "link": "",
        "tip": "Ask for official letterhead with college stamp and principal signature"
    },
    "Business proof": {
        "description": "Document proving your business exists",
        "how_to_get": "Shop establishment certificate from municipality or Udyam registration",
        "time_needed": "7-15 days",
        "cost": "Small fee",
        "link": "https://udyamregistration.gov.in",
        "tip": "Register your business free on Udyam portal to get instant certificate"
    },
    "Bank statement": {
        "description": "Last 6 months bank statement",
        "how_to_get": "Download from your bank's online portal or get from branch",
        "time_needed": "Immediate",
        "cost": "Free online, small fee at branch",
        "link": "",
        "tip": "Most banks allow free download of statements from mobile app"
    },
    "Educational certificate": {
        "description": "Your highest education qualification certificate",
        "how_to_get": "Get from your school or college",
        "time_needed": "Immediate if you have it",
        "cost": "Free",
        "link": "",
        "tip": "Keep both original and photocopy ready"
    },
    "Project report": {
        "description": "Business plan document for your proposed business",
        "how_to_get": "Prepare yourself or get help from KVIC/KVIB office",
        "time_needed": "3-7 days to prepare",
        "cost": "Free with KVIC help",
        "link": "https://www.kviconline.gov.in",
        "tip": "KVIC offices help you prepare project reports for free - visit them!"
    },
    "Mobile number": {
        "description": "Mobile number linked to your Aadhaar",
        "how_to_get": "Link your mobile to Aadhaar at nearest Aadhaar center",
        "time_needed": "Immediate",
        "cost": "Free",
        "link": "https://uidai.gov.in",
        "tip": "Must be linked to Aadhaar for OTP verification during applications"
    },
    "Passport photo": {
        "description": "Recent passport size photograph",
        "how_to_get": "Any photo studio near you",
        "time_needed": "Immediate",
        "cost": "Rs 30-100 for set of photos",
        "link": "",
        "tip": "Take 6-8 photos at once - you'll need them for multiple applications"
    },
    "Hospital registration card": {
        "description": "Card from government hospital for antenatal care",
        "how_to_get": "Register at nearest government hospital during pregnancy",
        "time_needed": "Immediate at hospital",
        "cost": "Free",
        "link": "",
        "tip": "Register early in pregnancy for full scheme benefits"
    },
    "Birth certificate": {
        "description": "Official birth certificate from municipality",
        "how_to_get": "Apply at nearest municipality/panchayat office",
        "time_needed": "7-15 days",
        "cost": "Small fee",
        "link": "",
        "tip": "Apply within 21 days of birth for free certificate"
    },
    "Caste certificate": {
        "description": "Certificate proving SC/ST/OBC category",
        "how_to_get": "Apply at Tahsildar office or MeeSeva in Telangana",
        "time_needed": "15-30 days",
        "cost": "Small fee",
        "link": "https://meeseva.telangana.gov.in",
        "tip": "Apply online through MeeSeva in Telangana for faster processing"
    }
}

def generate_checklist(schemes):
    """Generate a complete document checklist for all matched schemes"""
    all_docs = {}
    
    for scheme in schemes:
        for doc in scheme.get("documents", []):
            if doc not in all_docs:
                all_docs[doc] = {
                    "needed_for": [],
                    "guide": DOCUMENT_GUIDE.get(doc, {
                        "description": "Required document",
                        "how_to_get": "Contact your nearest government office",
                        "time_needed": "Varies",
                        "cost": "Varies",
                        "link": "",
                        "tip": "Carry original and photocopy"
                    })
                }
            all_docs[doc]["needed_for"].append(scheme["name"])
    
    return all_docs

def get_priority_docs(checklist):
    """Sort documents by how many schemes need them"""
    sorted_docs = sorted(
        checklist.items(),
        key=lambda x: len(x[1]["needed_for"]),
        reverse=True
    )
    return sorted_docs

if __name__ == "__main__":
    # Test the checklist generator
    from matcher import match_schemes
    
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
    
    matched = match_schemes(test_profile)
    checklist = generate_checklist(matched)
    priority = get_priority_docs(checklist)
    
    print("\n📋 COMPLETE DOCUMENT CHECKLIST")
    print("="*50)
    print(f"You need {len(checklist)} unique documents for all {len(matched)} schemes\n")
    
    print("📌 START WITH THESE (needed for most schemes):\n")
    for doc, info in priority:
        schemes_str = ", ".join(info["needed_for"])
        guide = info["guide"]
        print(f"✅ {doc}")
        print(f"   Needed for: {len(info['needed_for'])} scheme(s)")
        print(f"   How to get: {guide['how_to_get']}")
        print(f"   Cost: {guide['cost']}")
        print(f"   Time: {guide['time_needed']}")
        if guide.get('tip'):
            print(f"   💡 Tip: {guide['tip']}")
        print()
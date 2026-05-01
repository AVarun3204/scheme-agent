import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Scheme details stored as text - Gemini will analyze these
SCHEME_DETAILS = {
    "PM Kisan Samman Nidhi": """
        PM Kisan Samman Nidhi Scheme Details:
        - Financial benefit of Rs 6000 per year given in 3 installments of Rs 2000 each
        - For all landholding farmer families across India
        - Eligibility: Must own cultivable land, must be Indian citizen
        - Exclusions: Income taxpayers, institutional landholders, government employees
        - Documents: Aadhaar card, land records, bank account linked to Aadhaar
        - Application: Online at pmkisan.gov.in or through local patwari/revenue officer
        - Amount directly transferred to bank account via DBT
        - Registration free of cost
    """,
    "Ayushman Bharat PM-JAY": """
        Ayushman Bharat Pradhan Mantri Jan Arogya Yojana:
        - Health cover of Rs 5 lakh per family per year
        - Covers secondary and tertiary hospitalization
        - Eligibility: Based on SECC 2011 data, BPL families
        - Covers pre and post hospitalization expenses
        - No cap on family size or age
        - Documents: Aadhaar card, ration card, income certificate
        - Cashless treatment at empanelled hospitals
        - Over 1500 medical procedures covered
        - Apply at nearest Common Service Centre or empanelled hospital
    """,
    "PM Awas Yojana (Gramin)": """
        Pradhan Mantri Awas Yojana Gramin:
        - Financial assistance of Rs 1.20 lakh in plains and Rs 1.30 lakh in hilly areas
        - For construction of pucca house for houseless families
        - Eligibility: Families without pucca house, BPL category, rural areas
        - Priority: SC/ST, minorities, disabled, women headed households
        - Documents: Aadhaar, ration card, income certificate, BPL certificate
        - Payment directly to beneficiary bank account in instalments
        - Must construct house within stipulated time
        - Apply through Gram Panchayat or Block Development Office
    """,
    "Telangana Rythu Bandhu": """
        Telangana Rythu Bandhu Scheme:
        - Investment support of Rs 10,000 per acre per year (Rs 5000 per season)
        - For all farm land owning farmers in Telangana state
        - Eligibility: Must own agricultural land in Telangana, must have Pattadar passbook
        - Covers both Kharif and Rabi seasons
        - Documents: Aadhaar card, Pattadar passbook, bank account
        - Amount directly credited to farmer bank account before each crop season
        - No application needed - automatic based on land records
        - Both small and large farmers eligible
    """,
    "PMEGP Self Employment Loan": """
        Prime Minister Employment Generation Programme:
        - Subsidy of 15 to 35 percent on project cost
        - Maximum project cost Rs 25 lakh for manufacturing, Rs 10 lakh for services
        - Eligibility: Age 18 years and above, at least 8th pass for projects above Rs 10 lakh
        - For new business only, not for existing businesses
        - Higher subsidy for SC/ST/OBC/women/ex-servicemen/differently abled
        - Documents: Aadhaar, PAN, educational certificate, project report, caste certificate
        - Apply online at kviconline.gov.in
        - Loan through scheduled banks after KVIC/KVIB approval
    """
}

def get_scheme_details_from_gemini(scheme_name, user_profile=None):
    """Use Gemini to analyze scheme details and give personalized advice"""
    
    scheme_text = SCHEME_DETAILS.get(scheme_name, "")
    
    if not scheme_text:
        return "Detailed information not available. Please visit the official website."
    
    if user_profile:
        prompt = f"""Based on this government scheme information:

{scheme_text}

Give a simple, personalized explanation for a person with this profile:
- Age: {user_profile.get('age')}
- Occupation: {user_profile.get('occupation')}
- Annual Income: Rs {user_profile.get('annual_income')}
- State: {user_profile.get('state')}

Tell them:
1. Why they specifically qualify
2. Exact benefit they will get
3. Most important documents they need
4. First step they should take to apply

Keep it simple, friendly and in 150 words maximum."""
    else:
        prompt = f"""Based on this government scheme information:

{scheme_text}

Give a clear, simple summary covering:
1. Who can apply
2. What benefit they get
3. Key documents needed
4. How to apply

Keep it simple and under 150 words."""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Could not analyze scheme details: {str(e)}"

if __name__ == "__main__":
    print("🤖 Testing Gemini Scheme Analyzer")
    print("="*50)
    
    test_profile = {
        "age": 42,
        "occupation": "farmer",
        "annual_income": 80000,
        "state": "telangana"
    }
    
    print("\nTesting with PM Kisan scheme + farmer profile...\n")
    result = get_scheme_details_from_gemini("PM Kisan Samman Nidhi", test_profile)
    print(result)
    print("\n" + "="*50)
    print("✅ Gemini analyzer working!")
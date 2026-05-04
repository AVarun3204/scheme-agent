import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)

def generate_success_story(name, schemes, profile):
    """Generate a personalized success story showing potential benefits"""
    
    if not schemes:
        return None
    
    # Calculate total potential benefit (rough estimate)
    scheme_list = "\n".join([f"- {s['name']}: {s['benefit']}" for s in schemes[:8]])
    
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful advisor. Write a short, motivating 
                    success story (3-4 sentences) for a person showing what they could 
                    achieve by applying for government schemes. Be specific, warm, and 
                    encouraging. Mention rupee amounts where relevant. Keep it under 80 words."""
                },
                {
                    "role": "user",
                    "content": f"""Person: {name}
Age: {profile.get('age')}, {profile.get('occupation')}, from {profile.get('state')}
Annual income: Rs {profile.get('annual_income')}

Eligible schemes:
{scheme_list}

Write their success story if they apply for all these schemes."""
                }
            ],
            temperature=0.8,
            max_tokens=200
        )
        return response.choices[0].message.content
    except:
        return None

def generate_whatsapp_message(name, schemes, checklist):
    """Generate a WhatsApp-ready message with scheme details"""
    
    msg = f"🏛️ *Government Schemes for {name}*\n"
    msg += f"Found by Scheme Agent AI\n\n"
    msg += f"✅ *You qualify for {len(schemes)} schemes:*\n\n"
    
    for i, scheme in enumerate(schemes, 1):
        msg += f"{i}. *{scheme['name']}*\n"
        msg += f"   💰 {scheme['benefit']}\n"
        msg += f"   🔗 {scheme['apply_link']}\n\n"
    
    # Add top documents
    all_docs = {}
    for scheme in schemes:
        for doc in scheme.get("documents", []):
            all_docs[doc] = all_docs.get(doc, 0) + 1
    
    top_docs = sorted(all_docs.items(), key=lambda x: x[1], reverse=True)[:5]
    
    msg += f"📄 *Key Documents Needed:*\n"
    for doc, count in top_docs:
        msg += f"• {doc}\n"
    
    msg += f"\n🤖 _Discovered using Scheme Agent AI_"
    msg += f"\n🌐 _Try it free: scheme-agent-6q8kkmrpxxylunbh4scajn.streamlit.app_"
    
    return msg

if __name__ == "__main__":
    print("Testing success story generator...\n")
    
    test_schemes = [
        {"name": "PM Kisan Samman Nidhi", "benefit": "6,000 per year"},
        {"name": "Telangana Rythu Bandhu", "benefit": "10,000 per acre per year"},
        {"name": "Ayushman Bharat", "benefit": "5 lakh health cover"}
    ]
    
    test_profile = {
        "age": 42,
        "occupation": "farmer",
        "state": "telangana",
        "annual_income": 80000
    }
    
    story = generate_success_story("Raju", test_schemes, test_profile)
    print("Success Story:")
    print(story)
    print("\n✅ Working!")
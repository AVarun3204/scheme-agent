import os
from dotenv import load_dotenv
from groq import Groq
import json
from matcher import match_schemes

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful Indian government scheme advisor called SchemeBot.
Your job is to help Indian citizens discover government schemes and subsidies they are eligible for.

Collect this information one question at a time:
1. Name
2. Age
3. Gender (male/female)
4. State they live in
5. Occupation (farmer/student/self_employed/salaried/unemployed/street_vendor)
6. Annual family income in rupees
7. Whether they are BPL card holder (yes/no)
8. Whether they own land (yes/no)
9. Whether they have a bank account (yes/no)
10. Whether they are enrolled in college (yes/no)

Ask ONE question at a time in simple friendly English.

After collecting all information output exactly:
PROFILE_COMPLETE: {"name": "X", "age": 0, "gender": "male", "state": "telangana", "occupation": "farmer", "annual_income": 0, "is_bpl": true, "owns_land": true, "has_bank_account": true, "enrolled_in_college": false}

Rules:
- state always lowercase
- occupation must be one of: farmer, student, self_employed, salaried, unemployed, street_vendor
- booleans must be true or false
- age and annual_income must be numbers
"""

def extract_profile(text):
    if "PROFILE_COMPLETE:" in text:
        json_part = text.split("PROFILE_COMPLETE:")[1].strip()
        try:
            return json.loads(json_part)
        except:
            return None
    return None

def format_results(matched_schemes, name):
    if not matched_schemes:
        return "No matching schemes found. Please visit your nearest government office."

    result = f"\n✅ Great news {name}! You qualify for {len(matched_schemes)} scheme(s):\n"
    result += "="*50 + "\n\n"

    for i, scheme in enumerate(matched_schemes, 1):
        result += f"{i}. {scheme['name']}\n"
        result += f"   📋 {scheme['description']}\n"
        result += f"   💰 Benefit: {scheme['benefit']}\n"
        result += f"   📄 Documents needed:\n"
        for doc in scheme['documents']:
            result += f"      • {doc}\n"
        result += f"   🔗 Apply at: {scheme['apply_link']}\n"
        result += f"   ⏰ Deadline: {scheme['deadline']}\n\n"

    result += "="*50
    result += "\n💡 Start with the scheme that gives the highest benefit!"
    return result

def chat(messages):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

def run_agent():
    print("\n" + "="*50)
    print("  WELCOME TO SCHEME AGENT")
    print("  Government Scheme Discovery Assistant")
    print("="*50)
    print("\nType your answers below. Type 'quit' to exit.\n")

    while True:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.append({"role": "user", "content": "Greet the user warmly and ask their name."})

        bot_message = chat(messages)
        messages.append({"role": "assistant", "content": bot_message})
        print(f"SchemeBot: {bot_message}\n")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == 'quit':
                print("\nThank you! Goodbye! 🙏")
                return

            if not user_input:
                continue

            messages.append({"role": "user", "content": user_input})
            bot_message = chat(messages)
            messages.append({"role": "assistant", "content": bot_message})

            profile = extract_profile(bot_message)

            if profile:
                name = profile.get("name", "Friend")
                print(f"\nSchemeBot: Perfect! Searching schemes for you...\n")
                print("🔍 Searching government schemes database...")
                matched = match_schemes(profile)
                print(format_results(matched, name))
                print("\n\nCheck schemes for another person? (yes/no)")
                again = input("You: ").strip().lower()
                if again == "yes":
                    print("\nStarting fresh...\n")
                    break
                else:
                    print("\nThank you for using Scheme Agent! 🙏")
                    return
            else:
                print(f"\nSchemeBot: {bot_message}\n")

if __name__ == "__main__":
    run_agent()
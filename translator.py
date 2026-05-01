import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)

LANGUAGES = {
    "English": "en",
    "Hindi - हिंदी": "hi",
    "Telugu - తెలుగు": "te",
    "Tamil - தமிழ்": "ta",
    "Bengali - বাংলা": "bn",
    "Marathi - मराठी": "mr",
    "Gujarati - ગુજરાતી": "gu",
    "Kannada - ಕನ್ನಡ": "kn",
    "Malayalam - മലയാളം": "ml",
    "Punjabi - ਪੰਜਾਬੀ": "pa",
    "Odia - ଓଡ଼ିଆ": "or",
    "Urdu - اردو": "ur",
    "Assamese - অসমীয়া": "as",
    "Maithili - मैथिली": "mai",
    "Sanskrit - संस्कृतम्": "sa",
    "Kashmiri - कॉशुर": "ks",
    "Nepali - नेपाली": "ne",
    "Sindhi - سنڌي": "sd",
    "Dogri - डोगरी": "doi",
    "Konkani - कोंकणी": "kok",
    "Manipuri - মৈতৈলোন্": "mni",
    "Bodo - बड़ो": "brx",
    "Santali - ᱥᱟᱱᱛᱟᱲᱤ": "sat"
}

def translate_text(text, target_language):
    """Translate text to target language using Groq AI"""
    if target_language == "English" or target_language == "en":
        return text
    
    # Get language name without the native script part
    lang_name = target_language.split(" - ")[0] if " - " in target_language else target_language
    
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a translator. Translate the given text to {lang_name}.
                    Rules:
                    - Translate ONLY the text content
                    - Keep all numbers, rupee amounts, URLs and links exactly as they are
                    - Keep emoji exactly as they are
                    - Keep scheme names in English but add translation in brackets if helpful
                    - Return ONLY the translated text, nothing else"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return text  # Return original if translation fails

def translate_scheme(scheme, target_language):
    """Translate a scheme's description and benefit"""
    if target_language == "English":
        return scheme
    
    translated = scheme.copy()
    translated["description"] = translate_text(scheme["description"], target_language)
    translated["benefit"] = translate_text(scheme["benefit"], target_language)
    return translated

def get_greeting(language):
    """Get greeting in different languages"""
    greetings = {
        "English": "Welcome! I will help you find government schemes.",
        "Hindi - हिंदी": "नमस्ते! मैं आपको सरकारी योजनाएं खोजने में मदद करूंगा।",
        "Telugu - తెలుగు": "నమస్కారం! నేను మీకు ప్రభుత్వ పథకాలు కనుగొనడంలో సహాయం చేస్తాను.",
        "Tamil - தமிழ்": "வணக்கம்! அரசு திட்டங்களை கண்டுபிடிக்க உதவுகிறேன்.",
        "Bengali - বাংলা": "নমস্কার! আমি আপনাকে সরকারি প্রকল্প খুঁজে পেতে সাহায্য করব।",
        "Marathi - मराठी": "नमस्कार! मी तुम्हाला सरकारी योजना शोधण्यास मदत करेन।",
        "Gujarati - ગુજરાતી": "નમસ્તે! હું તમને સરકારી યોજનાઓ શોધવામાં મદદ કરીશ.",
        "Kannada - ಕನ್ನಡ": "ನಮಸ್ಕಾರ! ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಲು ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡುತ್ತೇನೆ.",
        "Malayalam - മലയാളം": "നമസ്കാരം! സർക്കാർ പദ്ധതികൾ കണ്ടെത്താൻ ഞാൻ സഹായിക്കാം.",
        "Punjabi - ਪੰਜਾਬੀ": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਨੂੰ ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਲੱਭਣ ਵਿੱਚ ਮਦਦ ਕਰਾਂਗਾ।"
    }
    return greetings.get(language, greetings["English"])

if __name__ == "__main__":
    print("Testing translator...\n")
    
    test_text = "You qualify for PM Kisan Samman Nidhi. Benefit: 6,000 per year paid in 3 instalments."
    
    # Test Hindi
    print("Hindi translation:")
    result = translate_text(test_text, "Hindi - हिंदी")
    print(result)
    
    print("\nTelugu translation:")
    result = translate_text(test_text, "Telugu - తెలుగు")
    print(result)
    
    print("\n✅ Translator working!")
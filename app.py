import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import json
from matcher import match_schemes
from checklist import generate_checklist, get_priority_docs
from tracker import (save_application, get_user_applications,
                     update_status, STATUS_OPTIONS, STATUS_EMOJI, delete_application)
from translator import LANGUAGES, translate_text, translate_scheme, get_greeting

load_dotenv(override=True)

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

def chat(messages):
    load_dotenv(override=True)
    fresh_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = fresh_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

def show_scheme_card(scheme, index):
    with st.container():
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3px;
            border-radius: 15px;
            margin-bottom: 20px;
        ">
        <div style="
            background: white;
            border-radius: 13px;
            padding: 20px;
        ">
            <h3 style="color: #4a4a8a; margin: 0 0 10px 0;">
                {index}. {scheme['name']}
            </h3>
            <p style="color: #666; margin: 5px 0;">📋 {scheme['description']}</p>
            <div style="
                background: #f0fff4;
                border-left: 4px solid #38a169;
                padding: 10px 15px;
                border-radius: 5px;
                margin: 10px 0;
            ">
                <strong style="color: #276749;">💰 Benefit: {scheme['benefit']}</strong>
            </div>
            <p style="color: #e53e3e; margin: 5px 0;">⏰ Deadline: {scheme['deadline']}</p>
            <a href="{scheme['apply_link']}" target="_blank" style="
                display: inline-block;
                background: #4a4a8a;
                color: white;
                padding: 8px 20px;
                border-radius: 20px;
                text-decoration: none;
                font-size: 14px;
                margin-top: 10px;
            ">🔗 Apply Now</a>
        </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("💡 Get Personalized Advice for this Scheme"):
            st.info("Gemini AI analysis will be available on final demo day. For now, check the documents section below and visit the official link to apply.")

        with st.expander("📄 View Documents Needed"):
            for doc in scheme['documents']:
                st.write(f"• {doc}")

st.set_page_config(
    page_title="Scheme Agent — Find Your Government Benefits",
    page_icon="🏛️",
    layout="centered"
)

st.markdown("""
<style>
    .main { background-color: #f8f9ff; }
    .stChatMessage { border-radius: 15px; margin: 5px 0; }
    .stTextInput input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 10px 20px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 30px 0 10px 0;">
    <h1 style="color: #4a4a8a; font-size: 2.5em;">🏛️ Scheme Agent</h1>
    <p style="color: #666; font-size: 1.1em;">
        Discover government schemes & subsidies you qualify for — instantly
    </p>
    <div style="
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 15px;
        flex-wrap: wrap;
    ">
        <span style="background:#e8f5e9; color:#2e7d32; padding:5px 15px; border-radius:20px; font-size:13px;">✅ 100% Free</span>
        <span style="background:#e3f2fd; color:#1565c0; padding:5px 15px; border-radius:20px; font-size:13px;">🤖 AI Powered</span>
        <span style="background:#fce4ec; color:#880e4f; padding:5px 15px; border-radius:20px; font-size:13px;">🇮🇳 India Focused</span>
        <span style="background:#f3e5f5; color:#6a1b9a; padding:5px 15px; border-radius:20px; font-size:13px;">⚡ Instant Results</span>
    </div>
</div>
<hr style="border: 1px solid #e0e0e0; margin: 20px 0;">
""", unsafe_allow_html=True)

# Language Selector
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_lang = st.selectbox(
        "🌐 Select Language / भाषा चुनें / భాష ఎంచుకోండి",
        list(LANGUAGES.keys()),
        index=0
    )
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "profile_found" not in st.session_state:
    st.session_state.profile_found = False
if "matched_schemes" not in st.session_state:
    st.session_state.matched_schemes = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "Friend"
if "started" not in st.session_state:
    st.session_state.started = False
if "show_tracker" not in st.session_state:
    st.session_state.show_tracker = False
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"

st.session_state.selected_language = selected_lang

if not st.session_state.started:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Finding My Schemes", use_container_width=True):
            st.session_state.started = True
            st.session_state.messages.append({
                "role": "user",
                "content": "Greet the user warmly and ask their name."
            })
            response = chat(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

if st.session_state.started and not st.session_state.profile_found:
    for msg in st.session_state.chat_history:
        if msg["role"] == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                display_text = msg["content"]
                if "PROFILE_COMPLETE:" in display_text:
                    display_text = "Perfect! I have all the information I need. Let me search for your schemes now..."
                st.write(display_text)
        else:
            with st.chat_message("user", avatar="👤"):
                st.write(msg["content"])

    user_input = st.chat_input("Type your answer here...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = chat(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        profile = extract_profile(response)
        if profile:
            st.session_state.profile_found = True
            st.session_state.user_name = profile.get("name", "Friend")
            st.session_state.matched_schemes = match_schemes(profile)
        st.rerun()

if st.session_state.profile_found:
    name = st.session_state.user_name
    schemes = st.session_state.matched_schemes
    lang = st.session_state.selected_language

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        color: white;
    ">
        <h2 style="margin: 0; color: white;">🎉 Great News, {name}!</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.2em; color: white;">
            You qualify for <strong>{len(schemes)} government scheme(s)</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    if schemes:
        st.markdown("### 📋 Your Eligible Schemes")

        # Translate if needed
        if lang != "English":
            with st.spinner(f"Translating to {lang.split(' - ')[0]}... please wait"):
                display_schemes = [translate_scheme(s, lang) for s in schemes]
        else:
            display_schemes = schemes

        for i, scheme in enumerate(display_schemes, 1):
            show_scheme_card(scheme, i)

        # Document Checklist
        st.markdown("---")
        st.markdown("### 📋 Your Complete Document Checklist")
        st.markdown("*Collect these documents to apply for all your schemes*")
        checklist = generate_checklist(schemes)
        priority = get_priority_docs(checklist)
        st.info(f"You need **{len(checklist)} documents** in total for all {len(schemes)} schemes. Start collecting them today!")
        for doc, info in priority:
            guide = info["guide"]
            with st.expander(f"✅ {doc} — needed for {len(info['needed_for'])} scheme(s)"):
                st.write(f"**📝 What is it:** {guide['description']}")
                st.write(f"**🏛️ How to get it:** {guide['how_to_get']}")
                st.write(f"**⏰ Time needed:** {guide['time_needed']}")
                st.write(f"**💰 Cost:** {guide['cost']}")
                if guide.get('tip'):
                    st.success(f"💡 Tip: {guide['tip']}")
                if guide.get('link'):
                    st.write(f"**🔗 Link:** {guide['link']}")
                st.write(f"**📌 Needed for:** {', '.join(info['needed_for'])}")

        # Application Tracker
        st.markdown("---")
        st.markdown("### 📊 Track Your Applications")
        st.markdown("*Save schemes and track your application status*")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save All Schemes to Tracker", use_container_width=True):
                saved_count = 0
                for scheme in schemes:
                    result = save_application(
                        name,
                        scheme["name"],
                        scheme["benefit"],
                        scheme["apply_link"]
                    )
                    if result:
                        saved_count += 1
                if saved_count > 0:
                    st.success(f"✅ Saved {saved_count} schemes to your tracker!")
                else:
                    st.info("All schemes already saved!")

        with col2:
            if st.button("📊 View My Applications", use_container_width=True):
                st.session_state.show_tracker = not st.session_state.show_tracker
                st.rerun()

        if st.session_state.show_tracker:
            user_apps = get_user_applications(name)
            if user_apps:
                st.markdown(f"#### {name}'s Applications ({len(user_apps)} total)")
                for app in user_apps:
                    emoji = STATUS_EMOJI.get(app["status"], "⬜")
                    with st.expander(f"{emoji} {app['scheme_name']} — {app['status']}"):
                        st.write(f"**💰 Benefit:** {app['scheme_benefit']}")
                        st.write(f"**📅 Saved on:** {app['date_saved']}")
                        if app['date_applied']:
                            st.write(f"**📤 Applied on:** {app['date_applied']}")
                        new_status = st.selectbox(
                            "Update status:",
                            STATUS_OPTIONS,
                            index=STATUS_OPTIONS.index(app["status"]),
                            key=f"status_{app['id']}"
                        )
                        notes = st.text_input(
                            "Add notes:",
                            value=app.get("notes", ""),
                            key=f"notes_{app['id']}"
                        )
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("💾 Update", key=f"update_{app['id']}"):
                                update_status(app["id"], new_status, notes)
                                st.success("Updated!")
                                st.rerun()
                        with col_b:
                            if st.button("🗑️ Delete", key=f"delete_{app['id']}"):
                                delete_application(app["id"])
                                st.success("Deleted!")
                                st.rerun()
            else:
                st.info("No applications saved yet. Click 'Save All Schemes' first!")

        st.markdown("""
        <div style="
            background: #fff8e1;
            border: 1px solid #ffc107;
            border-radius: 10px;
            padding: 15px 20px;
            margin-top: 20px;
        ">
            <strong>⚠️ Important Note:</strong> Eligibility shown is based on information you provided.
            Final verification is done by the government using your Aadhaar and documents.
            Make sure all your documents are genuine before applying.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("No matching schemes found for your profile. Please visit your nearest government office.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Check for Another Person", use_container_width=True):
        for key in ["messages", "chat_history", "profile_found",
                    "matched_schemes", "user_name", "started",
                    "show_tracker", "selected_language"]:
            del st.session_state[key]
        st.rerun()
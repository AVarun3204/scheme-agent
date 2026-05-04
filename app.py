import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import json
from matcher import match_schemes
from checklist import generate_checklist, get_priority_docs
from tracker import (save_application, get_user_applications,
                     update_status, STATUS_OPTIONS, STATUS_EMOJI, delete_application)
from translator import LANGUAGES, get_greeting
from stats import get_scheme_stats, get_application_stats
from success_story import generate_success_story, generate_whatsapp_message
import translator as translator_module
translate_schemes_bulk = translator_module.translate_schemes_bulk

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
    apply_link = scheme['apply_link']
    if apply_link.startswith('http'):
        apply_button = f'''<a href="{apply_link}" target="_blank" style="
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 10px 24px;
            border-radius: 25px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            margin-top: 12px;
            box-shadow: 0 4px 15px rgba(102,126,234,0.4);
        ">🔗 Apply Now</a>'''
    else:
        apply_button = f'''<div style="
            background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
            color: #2e7d32;
            padding: 10px 16px;
            border-radius: 10px;
            margin-top: 12px;
            font-size: 13px;
            border-left: 4px solid #4caf50;
        ">📍 {apply_link}</div>'''

    with st.container():
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #f0f0f0;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <div style="
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 16px;
                    margin-right: 12px;
                    flex-shrink: 0;
                ">{index}</div>
                <h3 style="color: #2d3748; margin: 0; font-size: 18px; font-weight: 600;">
                    {scheme['name']}
                </h3>
            </div>
            <p style="color: #718096; margin: 0 0 12px 0; font-size: 14px; line-height: 1.6;">
                {scheme['description']}
            </p>
            <div style="
                background: linear-gradient(135deg, #f0fff4, #e6fffa);
                border-left: 4px solid #38a169;
                padding: 12px 16px;
                border-radius: 0 12px 12px 0;
                margin: 12px 0;
            ">
                <span style="color: #276749; font-weight: 600; font-size: 15px;">
                    💰 {scheme['benefit']}
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <span style="
                    background: #fff5f5;
                    color: #e53e3e;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    border: 1px solid #fed7d7;
                ">⏰ {scheme['deadline']}</span>
                {apply_button}
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📄 Documents Needed"):
            for doc in scheme['documents']:
                st.markdown(f"✅ {doc}")

        with st.expander("💡 Personalized Advice"):
            st.info("Gemini AI analysis coming on demo day. Visit the official link to apply now!")

st.set_page_config(
    page_title="Scheme Agent — Find Your Government Benefits",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <div style="font-size: 40px;">🏛️</div>
        <h2 style="color: #4a4a8a; margin: 8px 0 4px 0;">Scheme Agent</h2>
        <p style="color: #888; font-size: 12px; margin: 0;">AI-Powered Welfare Discovery</p>
    </div>
    """, unsafe_allow_html=True)

    stats = get_scheme_stats()
    app_stats = get_application_stats()

    st.markdown("### 📊 Database Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", stats["total_schemes"])
        st.metric("Central", stats["central_schemes"])
    with col2:
        st.metric("Telangana", stats["telangana_schemes"])
        st.metric("Online", stats["online_schemes"])

    st.markdown("---")
    st.markdown("### 📋 By Category")
    for cat, count in sorted(stats["categories"].items(), key=lambda x: x[1], reverse=True):
        pct = int((count / stats["total_schemes"]) * 100)
        st.markdown(f"""
        <div style="margin-bottom: 6px;">
            <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 2px;">
                <span>{cat.replace('_', ' ').title()}</span>
                <span><b>{count}</b></span>
            </div>
            <div style="background: #f0f0f0; border-radius: 4px; height: 6px;">
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); width: {pct*3}%; height: 6px; border-radius: 4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 👥 Usage")
    st.metric("Applications Saved", app_stats["total_applications"])
    st.metric("Unique Users", app_stats["unique_users"])
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <div style="font-size: 13px; color: #888;">🌐 23 Indian Languages</div>
        <div style="font-size: 11px; color: #aaa; margin-top: 4px;">Milan AI Week Hackathon 2026</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.info("👈 Click the arrow at top to hide/show this panel")

# Main CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .main { background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%); }
    .stChatMessage { border-radius: 18px; margin: 8px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .stChatInput > div { border-radius: 25px !important; border: 2px solid #667eea !important; }
    .stButton > button { border-radius: 25px !important; font-weight: 500 !important; transition: all 0.3s !important; }
    .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stExpander { border-radius: 12px !important; border: 1px solid #e8e8e8 !important; margin-bottom: 8px !important; }
    [data-testid="metric-container"] { background: white; border-radius: 12px; padding: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    [data-testid="collapsedControl"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border-radius: 0 12px 12px 0 !important;
        width: 28px !important;
        top: 50% !important;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 24px;
    padding: 40px 30px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(102,126,234,0.3);
">
    <div style="font-size: 48px; margin-bottom: 12px;">🏛️</div>
    <h1 style="color: white; margin: 0 0 8px 0; font-size: 2.2em; font-weight: 700;">Scheme Agent</h1>
    <p style="color: rgba(255,255,255,0.85); margin: 0 0 20px 0; font-size: 1.1em;">
        Find every government scheme you qualify for — instantly & freely
    </p>
    <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
        <span style="background: rgba(255,255,255,0.2); color: white; padding: 6px 16px; border-radius: 20px; font-size: 13px;">✅ 100% Free</span>
        <span style="background: rgba(255,255,255,0.2); color: white; padding: 6px 16px; border-radius: 20px; font-size: 13px;">🤖 AI Powered</span>
        <span style="background: rgba(255,255,255,0.2); color: white; padding: 6px 16px; border-radius: 20px; font-size: 13px;">🇮🇳 35+ Schemes</span>
        <span style="background: rgba(255,255,255,0.2); color: white; padding: 6px 16px; border-radius: 20px; font-size: 13px;">🌐 23 Languages</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Language Selector
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_lang = st.selectbox(
        "🌐 Select Language / भाषा चुनें / భాష ఎంచుకోండి",
        list(LANGUAGES.keys()),
        index=0
    )

st.markdown("<br>", unsafe_allow_html=True)

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
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

st.session_state.selected_language = selected_lang

if not st.session_state.started:
    st.markdown("""
    <div style="background: white; border-radius: 20px; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
        <h3 style="color: #2d3748; margin: 0 0 16px 0; text-align: center;">How it works</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; text-align: center;">
            <div>
                <div style="font-size: 32px; margin-bottom: 8px;">💬</div>
                <div style="font-weight: 600; color: #4a4a8a; margin-bottom: 4px;">Chat</div>
                <div style="font-size: 12px; color: #888;">Answer 10 simple questions</div>
            </div>
            <div>
                <div style="font-size: 32px; margin-bottom: 8px;">🔍</div>
                <div style="font-weight: 600; color: #4a4a8a; margin-bottom: 4px;">Discover</div>
                <div style="font-size: 12px; color: #888;">AI finds your matching schemes</div>
            </div>
            <div>
                <div style="font-size: 32px; margin-bottom: 8px;">✅</div>
                <div style="font-weight: 600; color: #4a4a8a; margin-bottom: 4px;">Apply</div>
                <div style="font-size: 12px; color: #888;">Get documents and apply easily</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Finding My Schemes", use_container_width=True, type="primary"):
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
    st.markdown("""
    <div style="background: white; border-radius: 20px; padding: 20px; margin-bottom: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
        <p style="color: #888; font-size: 13px; margin: 0; text-align: center;">
            💡 Answer all questions to discover your eligible schemes
        </p>
    </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                display_text = msg["content"]
                if "PROFILE_COMPLETE:" in display_text:
                    display_text = "Perfect! I have all your details. Searching for schemes now..."
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
            st.session_state.user_profile = profile
            st.session_state.matched_schemes = match_schemes(profile)
        st.rerun()

if st.session_state.profile_found:
    name = st.session_state.user_name
    schemes = st.session_state.matched_schemes
    lang = st.session_state.selected_language
    profile = st.session_state.get("user_profile", {})

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(102,126,234,0.3);
    ">
        <div style="font-size: 48px; margin-bottom: 12px;">🎉</div>
        <h2 style="margin: 0 0 8px 0; color: white; font-size: 1.8em;">Great News, {name}!</h2>
        <p style="margin: 0; color: rgba(255,255,255,0.9); font-size: 1.1em;">
            You qualify for <strong>{len(schemes)} government scheme(s)</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    if schemes:

        # Success Story
        with st.spinner("✨ Generating your personalized success story..."):
            story = generate_success_story(name, schemes, profile)
        if story:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
                border-radius: 20px;
                padding: 24px;
                margin: 20px 0;
                box-shadow: 0 4px 20px rgba(253,160,133,0.3);
            ">
                <h3 style="color: white; margin: 0 0 12px 0;">🌟 Your Success Story</h3>
                <p style="color: rgba(255,255,255,0.95); margin: 0; font-size: 15px; line-height: 1.7;">
                    {story}
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## 📋 Your Eligible Schemes")

        if lang != "English":
            with st.spinner(f"Translating to {lang.split(' - ')[0]}..."):
                display_schemes = translate_schemes_bulk(schemes, lang)
        else:
            display_schemes = schemes

        for i, scheme in enumerate(display_schemes, 1):
            show_scheme_card(scheme, i)

        # WhatsApp Export
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #e8f8f0, #f0fff4);
            border-radius: 20px;
            padding: 24px;
            margin: 24px 0 16px 0;
            border-left: 5px solid #25D366;
        ">
            <h2 style="color: #2c3e50; margin: 0 0 8px 0;">📱 Share on WhatsApp</h2>
            <p style="color: #7f8c8d; margin: 0; font-size: 14px;">
                Share your scheme list with family who don't have internet access
            </p>
        </div>
        """, unsafe_allow_html=True)

        whatsapp_msg = generate_whatsapp_message(name, schemes, {})
        st.text_area("Copy this message:", value=whatsapp_msg, height=180, key="whatsapp_msg")
        encoded_msg = whatsapp_msg.replace(' ', '%20').replace('\n', '%0A').replace('*', '%2A')
        st.markdown(f"""
        <a href="https://wa.me/?text={encoded_msg}" target="_blank" style="
            display: inline-block;
            background: #25D366;
            color: white;
            padding: 12px 28px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            font-size: 15px;
            box-shadow: 0 4px 15px rgba(37,211,102,0.4);
            margin-top: 8px;
        ">📱 Open in WhatsApp</a>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Document Checklist
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #e8f4fd, #f0f8ff);
            border-radius: 20px;
            padding: 24px;
            margin: 24px 0 16px 0;
            border-left: 5px solid #3498db;
        ">
            <h2 style="color: #2c3e50; margin: 0 0 8px 0;">📋 Your Document Checklist</h2>
            <p style="color: #7f8c8d; margin: 0; font-size: 14px;">
                Collect these documents to apply for all your schemes
            </p>
        </div>
        """, unsafe_allow_html=True)

        checklist = generate_checklist(schemes)
        priority = get_priority_docs(checklist)
        st.info(f"You need **{len(checklist)} documents** for all {len(schemes)} schemes!")

        for doc, info in priority:
            guide = info["guide"]
            with st.expander(f"📄 {doc} — needed for {len(info['needed_for'])} scheme(s)"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**📝 What:** {guide['description']}")
                    st.write(f"**🏛️ Where:** {guide['how_to_get']}")
                with col2:
                    st.write(f"**⏰ Time:** {guide['time_needed']}")
                    st.write(f"**💰 Cost:** {guide['cost']}")
                if guide.get('tip'):
                    st.success(f"💡 {guide['tip']}")
                if guide.get('link'):
                    st.write(f"**🔗** {guide['link']}")
                st.write(f"**📌 For:** {', '.join(info['needed_for'])}")

        # Application Tracker
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #e8f8f5, #f0fff4);
            border-radius: 20px;
            padding: 24px;
            margin: 24px 0 16px 0;
            border-left: 5px solid #27ae60;
        ">
            <h2 style="color: #2c3e50; margin: 0 0 8px 0;">📊 Track Your Applications</h2>
            <p style="color: #7f8c8d; margin: 0; font-size: 14px;">
                Save and track the status of each scheme you apply for
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save All to Tracker", use_container_width=True, type="primary"):
                saved_count = 0
                for scheme in schemes:
                    result = save_application(
                        name, scheme["name"],
                        scheme["benefit"], scheme["apply_link"]
                    )
                    if result:
                        saved_count += 1
                if saved_count > 0:
                    st.success(f"✅ Saved {saved_count} schemes!")
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
                        st.write(f"**📅 Saved:** {app['date_saved']}")
                        if app['date_applied']:
                            st.write(f"**📤 Applied:** {app['date_applied']}")
                        new_status = st.selectbox(
                            "Update status:",
                            STATUS_OPTIONS,
                            index=STATUS_OPTIONS.index(app["status"]),
                            key=f"status_{app['id']}"
                        )
                        notes = st.text_input(
                            "Notes:",
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
                st.info("No applications saved yet. Click 'Save All to Tracker' first!")

        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fff8e1, #fffde7);
            border-radius: 16px;
            padding: 16px 20px;
            margin-top: 24px;
            border-left: 4px solid #ffc107;
        ">
            <strong>⚠️ Important:</strong> Eligibility shown is based on your provided information.
            Final verification is done by the government using your Aadhaar and documents.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("No matching schemes found. Please visit your nearest government office.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Check for Another Person", use_container_width=True):
        for key in ["messages", "chat_history", "profile_found",
                    "matched_schemes", "user_name", "started",
                    "show_tracker", "selected_language", "user_profile"]:
            del st.session_state[key]
        st.rerun()
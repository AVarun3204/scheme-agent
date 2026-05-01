# 🏛️ Scheme Agent — AI-Powered Government Scheme Discovery

> Find every government scheme you qualify for — instantly, in your language.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-brightgreen)](https://scheme-agent-6q8kkmrpxxylunbh4scajn.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.14-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3-orange)](https://groq.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini-yellow)](https://ai.google.dev)

---

## 🎯 The Problem

India has **1,000+ government schemes** worth **₹2 lakh crore+** in benefits every year.

But **95% of eligible citizens never apply** — because:
- They don't know which schemes exist
- Government websites are confusing and scattered
- Eligibility rules are buried in complex PDFs
- Application process is overwhelming

**A farmer in Telangana might qualify for 8-10 different schemes worth ₹2-3 lakh — but never knows.**

---

## 💡 The Solution

**Scheme Agent** is an autonomous AI agent that:

1. 🗣️ **Talks to citizens** in a friendly conversation
2. 🔍 **Discovers** every scheme they qualify for
3. 📋 **Generates** a complete document checklist
4. 🌐 **Speaks their language** — 23 Indian languages supported
5. 📊 **Tracks** their application status over time

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 AI Conversation | Natural chat to collect user profile |
| 🎯 Smart Matching | Matches against 35+ government schemes |
| 📋 Document Checklist | Exact documents needed with how to get them |
| 🌐 23 Languages | All Indian languages including Hindi Telugu Tamil |
| 📊 Application Tracker | Track status from applied to received |
| 💰 Zero Cost | Completely free for citizens to use |
| 📄 Gemini PDF Reader | Reads official government PDFs with Gemini AI |

---

## 🏆 Impact

- **Target users:** 300 million+ eligible citizens in India
- **Schemes covered:** 35 central + Telangana state schemes
- **Languages:** 23 Indian languages + English
- **Cost to user:** Completely free

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Groq Llama 3.3 70B** | Conversational AI and multilingual translation |
| **Google Gemini** | PDF reading and scheme analysis |
| **Featherless AI** | Domain-specialized government policy models |
| **Streamlit** | Web application framework |
| **Python** | Backend logic and matching engine |
| **LangChain** | AI orchestration |

---

## 🚀 How It Works
---

## 📸 Demo

Try it live: https://scheme-agent-6q8kkmrpxxylunbh4scajn.streamlit.app

Example — Telangana Farmer Profile:
- Age: 42, Male, Farmer, Income 80,000 per year
- BPL card holder, owns 2 acres land
- Result: 12 matching schemes worth 3+ lakh in benefits

---

## 🏗️ Project Structure

- app.py — Main Streamlit web application
- agent.py — Terminal-based AI agent
- matcher.py — Scheme eligibility matching engine
- schemes.json — Database of 35+ government schemes
- checklist.py — Document checklist generator
- tracker.py — Application status tracker
- translator.py — 23 Indian language translator
- pdf_reader.py — Gemini PDF analyzer
- requirements.txt — Python dependencies

---

## ⚙️ Setup Instructions

1. Clone the repository: git clone https://github.com/AVarun3204/scheme-agent.git
2. Install dependencies: pip install -r requirements.txt
3. Create a .env file with your API keys:
   - GROQ_API_KEY=your_groq_key_here
   - GEMINI_API_KEY=your_gemini_key_here
   - FEATHERLESS_API_KEY=your_featherless_key_here
4. Run the app: streamlit run app.py

---

## 🔑 API Keys Required

| API | Purpose | Cost |
|---|---|---|
| Groq | AI conversation and translation | Free |
| Google Gemini | PDF reading and analysis | Free tier |
| Featherless | Domain specialized models | Free tier |

---

## 🎯 Hackathon Tracks

This project is submitted for:
- Gemini Track — Uses Google Gemini for PDF analysis
- Featherless Track — Domain-specialized government policy agent
- Social Engagement Track — Building in public on Twitter/X

---

## 👨‍💻 Built By

Varun — Built during Milan AI Week Hackathon 2026

300 million people are leaving free government money unclaimed. We built an AI to fix that.

---

## 📄 License

MIT License — Free to use and modify
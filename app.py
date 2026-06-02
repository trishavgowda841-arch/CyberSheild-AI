import streamlit as st
import pickle
import base64

# -----------------------------
# LOAD MODEL
# -----------------------------
model = pickle.load(open("phishing_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="wide"
)
bg_image = get_base64("hacker.jpg")

st.markdown(
    f"""
    <style>

    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        background: rgba(0,0,0,0.82);
        padding: 2rem;
        border-radius: 20px;
    }}

    h1 {{
        color: #00ff41 !important;
        text-align:center;
        text-shadow: 0 0 15px #00ff41;
        font-size: 4rem;
    }}

    h2,h3 {{
        color:#00ff41 !important;
        text-shadow:0 0 10px #00ff41;
    }}

    [data-testid="stMetric"] {{
        background: rgba(0,0,0,0.75);
        border: 1px solid #00ff41;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 0 20px rgba(0,255,65,0.4);
    }}

    .stTextInput input {{
        background:black;
        color:#00ff41;
        border:1px solid #00ff41;
    }}

    .stTextArea textarea {{
        background:black;
        color:#00ff41;
        border:1px solid #00ff41;
    }}

    .stButton button {{
        background:black;
        color:#00ff41;
        border:2px solid #00ff41;
        border-radius:15px;
        font-weight:bold;
        width:100%;
        height:60px;
    }}

    .stButton button:hover {{
        box-shadow:0 0 25px #00ff41;
        transform:scale(1.02);
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0

if "high_risk" not in st.session_state:
    st.session_state.high_risk = 0

if "medium_risk" not in st.session_state:
    st.session_state.medium_risk = 0

if "low_risk" not in st.session_state:
    st.session_state.low_risk = 0

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
"""
<h1>🛡 CYBERSHIELD AI</h1>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div style="
background:rgba(0,0,0,0.8);
padding:20px;
border-radius:20px;
border:1px solid #00ff41;
text-align:center;
font-size:20px;
font-weight:bold;
color:#00ff41;">
⚡ ELITE PHISHING THREAT INTELLIGENCE SYSTEM ⚡
</div>
""",
unsafe_allow_html=True
)
st.write(
    "Analyze suspicious emails, phishing attempts, spam messages and social engineering attacks."
)

# -----------------------------
# DASHBOARD
# -----------------------------
st.subheader("📊 Dashboard Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Scans", st.session_state.total_scans)
c2.metric("High Risk", st.session_state.high_risk)
c3.metric("Medium Risk", st.session_state.medium_risk)
c4.metric("Low Risk", st.session_state.low_risk)

# -----------------------------
# INPUTS
# -----------------------------
sender_email = st.text_input(
    "📧 Sender Email Address",
    placeholder="support@example.com"
)
website_url = st.text_input(
    "🌐 Website URL (Optional)",
    placeholder="https://example.com"
)
email_subject = st.text_input(
    "📝 Email Subject",
    placeholder="Enter email subject"
)

email_text = st.text_area(
    "📄 Paste Email Content",
    height=250
)

# -----------------------------
# ANALYZE BUTTON
# -----------------------------
if st.button("🔍 Analyze Threat"):

    if email_text.strip() == "":
        st.warning("Please paste email content.")
        st.stop()

    # AI Prediction
    transformed = vectorizer.transform([email_text])

    prediction = model.predict(transformed)[0]
    probability = model.predict_proba(transformed)[0][1]

    threat_score = round(probability * 100)
    # URL Analysis

    if website_url:

       if len(website_url) > 60:
        threat_score += 10

       if "-" in website_url:
        threat_score += 10

       if ".xyz" in website_url:
        threat_score += 20

       if ".ru" in website_url:
        threat_score += 20

       if "login" in website_url:
        threat_score += 10

       if "verify" in website_url:
        threat_score += 10

    # -----------------------------
    # EXTRA THREAT ANALYSIS
    # -----------------------------
    suspicious_domains = [
        ".ru",
        ".xyz",
        ".tk",
        ".top",
        ".gq"
    ]

    urgency_words = [
        "urgent",
        "immediately",
        "verify",
        "suspended",
        "act now",
        "limited"
    ]

    suspicious_words = [
        "free",
        "winner",
        "bank",
        "password",
        "claim",
        "click",
        "prize",
        "offer"
    ]

    # Domain Check
    for domain in suspicious_domains:
        if domain in sender_email.lower():
            threat_score += 20

    # Urgency Check
    for word in urgency_words:
        if word in email_text.lower():
            threat_score += 5

    # Keyword Check
    for word in suspicious_words:
        if word in email_text.lower():
            threat_score += 3

    # Link Check
    link_count = email_text.lower().count("http")

    if link_count > 2:
        threat_score += 15

    threat_score = min(threat_score, 100)

    # -----------------------------
    # UPDATE STATS
    # -----------------------------
    st.session_state.total_scans += 1

    if threat_score >= 80:
        st.session_state.high_risk += 1
    elif threat_score >= 50:
        st.session_state.medium_risk += 1
    else:
        st.session_state.low_risk += 1

    # -----------------------------
    # RESULTS
    # -----------------------------
    st.subheader("🚨 Threat Assessment")

    st.progress(threat_score)
    st.subheader("⚡ Live Threat Meter")

    st.progress(threat_score)
    st.subheader("🧠 AI Verdict")

    if threat_score >= 80:
       st.markdown("""
### 🔴 CRITICAL

This email contains multiple phishing indicators and should not be trusted.
""")

    elif threat_score >= 50:
        st.markdown("""
### 🟠 SUSPICIOUS

Exercise caution before interacting with this message.
""")

    else:
        st.markdown("""
### 🟢 SAFE

No major phishing indicators detected.
""")  

    if threat_score >= 80:
         st.error(f"Threat Level: {threat_score}%")
    elif threat_score >= 50:
         st.warning(f"Threat Level: {threat_score}%")
    else:
         st.success(f"Threat Level: {threat_score}%")

    st.metric(
        "Threat Score",
        f"{threat_score}%"
    )

    # Risk Label
    if threat_score >= 80:
        st.error("🔴 HIGH RISK EMAIL")
    elif threat_score >= 50:
        st.warning("🟠 MEDIUM RISK EMAIL")
    else:
        st.success("🟢 LOW RISK EMAIL")
    reasons = []
    report = f"""
    CYBERSHIELD AI THREAT REPORT
    ==================================

    Sender Email:
    {sender_email}

    Subject:
    {email_subject}

    Threat Score:
    {threat_score}%

    Risk Level:
    {"HIGH RISK" if threat_score >= 80 else "MEDIUM RISK" if threat_score >= 50 else "LOW RISK"}

    Indicators Found:
    {chr(10).join(reasons)}

    Links Detected:
    {link_count}

    Generated by CyberShield AI
    """

    # -----------------------------
    # AI ANALYSIS
    # -----------------------------
    st.subheader("🤖 AI Security Analysis")

    reasons = []

    for word in urgency_words:
        if word in email_text.lower():
            reasons.append(f"Uses urgency keyword: {word}")

    for domain in suspicious_domains:
        if domain in sender_email.lower():
            reasons.append(f"Suspicious sender domain: {domain}")

    if link_count > 2:
        reasons.append("Contains multiple links")
    if website_url:

      if ".xyz" in website_url:
        reasons.append("Suspicious .xyz domain")

      if ".ru" in website_url:
        reasons.append("Suspicious .ru domain")

      if "-" in website_url:
        reasons.append("URL contains hyphens")

      if len(website_url) > 60:
        reasons.append("Very long URL")

    if reasons:
        for reason in reasons:
            st.write("•", reason)
    else:
        st.success("No major phishing indicators detected.")

    # -----------------------------
    # CONFIDENCE
    # -----------------------------
    st.subheader("📈 Detection Confidence")

    if threat_score >= 80:
        st.metric("Confidence", "Very High")
    elif threat_score >= 50:
        st.metric("Confidence", "Medium")
    else:
        st.metric("Confidence", "Low")

    # -----------------------------
    # KEYWORDS FOUND
    # -----------------------------
    st.subheader("🔍 Suspicious Keywords Found")

    found_words = []

    for word in suspicious_words:
        if word in email_text.lower():
            found_words.append(word)

    if found_words:
        st.write(", ".join(found_words))
    else:
        st.success("No suspicious keywords detected.")

    # -----------------------------
    # SECURITY ADVICE
    # -----------------------------
    st.subheader("🛡️ Security Recommendations")

    if threat_score >= 80:
        st.error("""
• Do NOT click links.
• Do NOT open attachments.
• Verify sender independently.
• Report email to security team.
• Delete if malicious.
""")

    elif threat_score >= 50:
        st.warning("""
• Verify sender before responding.
• Be cautious with links.
• Avoid sharing credentials.
""")

    else:
        st.success("""
• No major threat detected.
• Continue normal caution.
""")

    # -----------------------------
    # RISK BREAKDOWN
    # -----------------------------
    st.subheader("📊 Risk Breakdown")

    st.write("Links Detected:", link_count)
    st.write("Threat Indicators:", len(reasons))

    st.progress(min(link_count * 20, 100))
    st.progress(min(len(reasons) * 20, 100))
    # -----------------------------
    # DOWNLOADABLE THREAT REPORT
    # -----------------------------

    report = f"""
CYBERSHIELD AI THREAT REPORT
====================================

Sender Email:
{sender_email}

Email Subject:
{email_subject}

Threat Score:
{threat_score}%

Risk Level:
{"HIGH RISK" if threat_score >= 80 else "MEDIUM RISK" if threat_score >= 50 else "LOW RISK"}

Threat Indicators:
{chr(10).join(reasons)}

Links Detected:
{link_count}

Security Recommendation:
{"Do NOT interact with this email." if threat_score >= 80 else "Exercise caution." if threat_score >= 50 else "No major threat detected."}

Generated by CyberShield AI
"""
    st.download_button(
        label="📄 Download Threat Report",
        data=report,
        file_name="CyberShield_Report.txt",
        mime="text/plain",
        key="download_report"
        )
    
    
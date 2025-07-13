import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests
import base64
from gtts import gTTS
from tempfile import NamedTemporaryFile
import google.generativeai as genai

# --- APP CONFIG AND THEME ---
st.set_page_config(page_title="Cruel Justice - Advanced Analysis", layout="wide")


# --- TTS FUNCTION ---
def speak_text(text):
    try:
        tts = gTTS(text)
        with NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            with open(fp.name, "rb") as f:
                audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            audio_html = f"""
                <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Audio failed to play: {e}")


# --- ADVANCED UI STYLES ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

body, .stApp {
    background: linear-gradient(110deg, #0f172a 60%, #1e3a8a 100%);
    color: #FFFFFF; /* Made main text pure white */
    font-family: 'Roboto', sans-serif;
}

.stSidebar > div {
    /* White Gradient Sidebar */
    background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(240,240,240,0.95) 100%);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px); /* For Safari support */
    border-right: 1px solid rgba(0, 0, 0, 0.1); /* Adjusted border for light background */
    color: #333333; /* Ensure text in sidebar is readable on white */
}

/* Ensure header and radio button text in sidebar is readable */
.stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
    color: #0f172a !important; /* Darker color for headers in white sidebar */
}
.stSidebar .stRadio div label span { /* Target radio button labels */
    color: #333333 !important;
}


h1, h2, h3, h4, h5, h6 {
    color: #facc15 !important; /* Kept main headings yellow for contrast */
    font-weight: 700;
}

.stRadio > div {
    background-color: rgba(30, 41, 59, 0.5);
    padding: 1em;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-container {
    background: rgba(30, 41, 59, 0.5);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 1.5em;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 1em;
}

.content-box {
    padding: 1.5em;
}

.header-box {
    text-align: center;
    padding-top: 2em;
    padding-bottom: 1em;
}

.header-box h1 {
    font-size: 3.5em;
    font-weight: 700;
    letter-spacing: 2px;
}

/* --- Professional Timeline CSS --- */
.timeline-container {
    border-left: 3px solid #38bdf8;
    padding: 1em 2em;
    position: relative;
    list-style: none;
}

.timeline-item {
    margin-bottom: 2em;
    position: relative;
}

.timeline-item:before {
    content: '';
    background-color: #facc15;
    border: 3px solid #38bdf8;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    position: absolute;
    left: -33px;
    top: 0;
}

.timeline-item-content {
    color: #FFFFFF; /* Made timeline content text pure white */
    background: rgba(45, 55, 72, 0.7);
    padding: 1em;
    border-radius: 8px;
}

.timeline-item-content strong {
    color: #facc15;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# --- SIDEBAR ---
with st.sidebar:
    st.header("🔐 API Setup")
    GOOGLE_API_KEY = st.text_input("Enter Gemini API Key", type="password")
    if GOOGLE_API_KEY:
        genai.configure(api_key=GOOGLE_API_KEY)

    st.header("🧭 Navigation")
    mode = st.radio("Choose Mode:", ["Explore Famous Cases", "AI Case Generator"])


with st.container():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://judgeai.cloud/images/homepage_2.webp", width=125)
    with col2:
        st.markdown("""
        <div class="header-box">
            <h1>Cruel Justice</h1>
        </div>
        """, unsafe_allow_html=True)

# ------------------ FAMOUS CASES MODE ------------------
if mode == "Explore Famous Cases":
    st.header("📁 Select a Famous Criminal Case")
    case_option = st.selectbox("Choose a case:", [
        "Aarushi Talwar Case",
    "Bhima Koregaon Case",
    "George Floyd Case",
    "Jessica Lal Murder Case",
    "Adnan Syed Case"
    ], label_visibility="collapsed")

    case_data = {} # This will be populated based on selection

    # --- CASE DATA DICTIONARY ---
    cases = {"Arushi Talwar Case": {
    "name": "Aarushi Talwar Case",
    "timeline": [
           "<strong>2008 (May 16):</strong> 14-year-old Aarushi Talwar found murdered in her bedroom in Noida, India.",
           "<strong>2008 (May 17):</strong> Family's domestic helper, Hemraj, initially the prime suspect, is found dead on the terrace.",
           "<strong>2013 (November):</strong> Parents, Rajesh and Nupur Talwar, are convicted for the double murder by a trial court and sentenced to life imprisonment.",
           "<strong>2017 (October):</strong> The Allahabad High Court acquits the parents, citing lack of conclusive 'irresistible' evidence."
    ],
    "summary": "The unsolved double murder of 14-year-old Aarushi Talwar and her family's domestic helper, Hemraj Banjade. The case was marred by a botched initial investigation, multiple changes in investigation teams (from local police to CBI), and intense media sensationalism, leading to the parents' conviction and subsequent acquittal.",
    "verdict": "Parents initially convicted to life imprisonment, but later acquitted by the High Court due to insufficient evidence.",
    "laws": "IPC Section 302 (Murder), IPC Section 201 (Destruction of evidence), IPC Section 34 (Acts done by several persons in furtherance of common intention)",
    "real_outcome": "The parents were acquitted, but the 'benefit of doubt' verdict meant the murders remain officially unsolved, leaving a cloud of mystery and public debate.",
    "ai_opinion": "This case exposed significant systemic flaws in forensic investigation, crime scene management, and the detrimental influence of a 'media trial'. AI emphasizes the critical need for meticulous, unbiased police work, free from external pressures, to ensure justice is not compromised by procedural failures."
},
  {
    "Bhima Koregaon Case": {
        "name": "Bhima Koregaon Arrests",
        "timeline": [
            "<strong>2018 (January 1):</strong> Violence erupts during the annual commemoration of the 1818 Bhima Koregaon battle.",
            "<strong>2018 (June-August):</strong> Activists and intellectuals are arrested under the Unlawful Activities (Prevention) Act (UAPA).",
            "<strong>2019-2023:</strong> Multiple accused, including academics and lawyers, remain in jail for years without formal trial.",
            "<strong>2022:</strong> Accused Stan Swamy dies in custody due to lack of medical care.",
            "<strong>2023-2024:</strong> Courts begin to grant bail citing lack of strong evidence."
        ],
        "summary": "Several activists were accused of plotting to overthrow the Indian government, allegedly linked to Maoist groups. However, investigations and independent reports raised questions about the authenticity of digital evidence and political motivations behind the arrests.",
        "verdict": "No final verdict. Most of the accused spent years in jail under trial without conviction.",
        "laws": "UAPA (Unlawful Activities Prevention Act), IPC Sections 124A (Sedition), 120B (Criminal Conspiracy)",
        "real_outcome": "The case is still under trial, but it has raised serious concerns about misuse of anti-terror laws to suppress dissent.",
        "ai_opinion": "This case reflects how broad and vague anti-terror laws can be weaponized to silence critics. The prolonged pre-trial detention without clear evidence undermines constitutional rights and the presumption of innocence."
    },

    "George Floyd Case": {
        "name": "George Floyd Murder and Trial of Derek Chauvin",
        "timeline": [
            "<strong>2020 (May 25):</strong> George Floyd, an unarmed Black man, is killed by police officer Derek Chauvin in Minneapolis.",
            "<strong>2020 (May-June):</strong> Protests erupt across the US and globally under the #BlackLivesMatter movement.",
            "<strong>2021 (April):</strong> Chauvin is found guilty of murder and manslaughter.",
            "<strong>2021 (June):</strong> Chauvin sentenced to 22.5 years in prison."
        ],
        "summary": "The killing of George Floyd highlighted systemic racism and police brutality in the United States. Though Chauvin was eventually convicted, the incident drew attention to decades of racially biased policing practices.",
        "verdict": "Chauvin was convicted on all counts, including second-degree unintentional murder.",
        "laws": "US Code Title 18: Civil Rights Violations, Second-Degree Murder (Minnesota)",
        "real_outcome": "The case led to some police reform discussions and global protests, though many argue deeper change is still needed.",
        "ai_opinion": "While justice was served in this individual case, it exposed systemic racial inequality within law enforcement. True justice would require systemic change, not just convictions in high-profile cases."
    },

    "Jessica Lal Murder Case": {
        "name": "Jessica Lal Murder Case",
        "timeline": [
            "<strong>1999 (April):</strong> Jessica Lal is shot dead at a party in Delhi by Manu Sharma, son of a powerful politician.",
            "<strong>2006:</strong> After public outcry and media campaigns, the Delhi High Court reverses the initial acquittal and convicts Sharma.",
            "<strong>2010:</strong> Supreme Court upholds conviction. Sharma is sentenced to life imprisonment.",
            "<strong>2020:</strong> Sharma is released early citing “good behavior.”"
        ],
        "summary": "The murder of model Jessica Lal in front of dozens of witnesses initially resulted in acquittal due to witnesses turning hostile. A media campaign helped reopen the case. Bias from power, privilege, and money was evident.",
        "verdict": "Eventually convicted and sentenced to life imprisonment after retrial.",
        "laws": "IPC Section 302 (Murder), IPC Section 201 (Destruction of Evidence)",
        "real_outcome": "Sharma was released in 2020 after serving part of his life sentence. The case exposed how power and political connections can influence early investigations and court outcomes.",
        "ai_opinion": "The initial acquittal exposed how wealth and political power can obstruct justice. While later public pressure helped correct it, justice shouldn't require media intervention."
    },

    "Adnan Syed Case": {
        "name": "Adnan Syed / Serial Podcast Case",
        "timeline": [
            "<strong>1999:</strong> Hae Min Lee is found murdered in Baltimore. Her ex-boyfriend Adnan Syed is arrested.",
            "<strong>2000:</strong> Syed is convicted based on a single witness and inconsistent phone records.",
            "<strong>2014:</strong> Case gains attention through the hit podcast *Serial*.",
            "<strong>2016-2022:</strong> Multiple appeals are filed citing ineffective legal counsel and unreliable evidence.",
            "<strong>2022:</strong> Conviction is vacated. Syed is released from prison after 23 years."
        ],
        "summary": "Adnan Syed was convicted largely on circumstantial evidence. Years later, investigations revealed poor defense representation and weak forensic evidence. Media attention helped reopen the case.",
        "verdict": "Conviction vacated in 2022 due to prosecutorial issues and unreliable evidence.",
        "laws": "Maryland Criminal Code: First-degree murder, obstruction of justice",
        "real_outcome": "Syed’s release reignited conversations about wrongful convictions and the power of media in justice.",
        "ai_opinion": "This case exemplifies how procedural failures and poor legal defense can result in wrongful imprisonment. Media can be a double-edged sword—sometimes correcting injustice, other times distorting perception."
    }
}
    case_data = cases.get(case_option) # Safely get the selected case data

    # --- DISPLAY STRUCTURED CASE ---
    if case_data:
        st.markdown(f"## 🧾 {case_data['name']}")
        st.markdown("---")

        col1, col2 = st.columns((1, 1))

        with col1:
            st.markdown("### 🕒 Professional Timeline")
            timeline_html = "<ul class='timeline-container'>"
            for event in case_data["timeline"]:
                timeline_html += f"<li class='timeline-item'><div class='timeline-item-content'>{event}</div></li>"
            timeline_html += "</ul>"
            st.markdown(timeline_html, unsafe_allow_html=True)

        with col2:
            st.markdown("### 📋 Case Summary")
            st.markdown(f"<div class='glass-container content-box'>{case_data['summary']}</div>", unsafe_allow_html=True)

            st.markdown("### ⚖️ Verdict")
            st.success(case_data["verdict"])

            st.markdown("### 📌 Real Outcome")
            st.info(case_data["real_outcome"])

        st.markdown("---")
        st.markdown("### 🧠 AI's Opinion & Analysis")
        col_ai_1, col_ai_2 = st.columns(2)
        with col_ai_1:
            st.markdown(f"<div class='glass-container content-box'><strong>Applicable Laws:</strong><br>{case_data['laws']}</div>", unsafe_allow_html=True)
        with col_ai_2:
            st.markdown(f"<div class='glass-container content-box'><strong>AI's Ethical Judgement:</strong><br>{case_data['ai_opinion']}</div>", unsafe_allow_html=True)

        if st.button("▶️ Play AI Opinion Audio"):
            speak_text(case_data["ai_opinion"])


# ------------------ AI-GENERATED CASE MODE ------------------
elif mode == "AI Case Generator":
    st.header("🧠 Generate AI Analysis")
    st.markdown("---")

    with st.container():
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        choice = st.radio("How would you like to input your case?", ["Type a Case Name or Summary", "Upload a Text File"])

        case_text = ""
        if choice == "Upload a Text File":
            uploaded = st.file_uploader("Upload a .txt file", type=["txt"], label_visibility="collapsed")
            if uploaded:
                case_text = uploaded.read().decode("utf-8")
        else:
            typed = st.text_area("Enter Case Name or a brief summary:", height=150, label_visibility="collapsed")
            if typed:
                case_text = typed

        if case_text and GOOGLE_API_KEY:
            if st.button("Analyze with AI"):
                with st.spinner("Analyzing case using Gemini..."):
                    try:
                        model = genai.GenerativeModel("gemini-pro")
                        prompt = f"""
                        Analyze this criminal case thoroughly. Provide the following information in a structured, clear, and concise manner, using the exact headings provided below. Ensure all details are relevant to the case you are analyzing.

                        ## Case Summary:
                        (Provide a brief, factual summary of the case.)

                        ## Timeline of Events:
                        (List key events in chronological order, e.g., "YYYY: Event description.")

                        ## Applicable Laws:
                        (List relevant legal statutes or codes. If an Indian case, use Indian Penal Code (IPC) sections. For international cases, specify the jurisdiction's laws. Example: "IPC Section 302 (Murder)" or "US Code Title 18 – Deprivation of rights".)

                        ## Legal Gaps or Misuses:
                        (Discuss any perceived flaws in the legal process, loopholes, or misapplications of law.)

                        ## Real-life Outcome:
                        (State the final judgment, sentence, or resolution of the case.)

                        ## Ethical Judgment from an Unbiased AI:
                        (Offer an unbiased, ethical assessment of the case, focusing on fairness, justice, and societal impact.)

                        ## AI Recommendation:
                        (Provide constructive recommendations based on the case's handling or outcome, such as improvements to legal procedures or policy changes.)

                        Case: {case_text}
                        """
                        response = model.generate_content(prompt)
                        st.subheader("📖 AI Generated Analysis")
                        st.markdown("---")
                        st.markdown(f"<div class='glass-container content-box'>{response.text}</div>", unsafe_allow_html=True)
                        if st.button("▶️ Play Analysis Audio"):
                            speak_text(response.text)
                    except Exception as e:
                        st.error(f"An error occurred during AI analysis: {e}")
                        st.warning("Please ensure your Gemini API key is valid and the input is clear.")
        elif not GOOGLE_API_KEY:
            st.warning("Please provide your Gemini API key to use AI features.")

        st.markdown("</div>", unsafe_allow_html=True)

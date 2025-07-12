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

# --- LOTTIE ANIMATION FUNCTION ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

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


# --- HEADER ---
with st.container():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2122/2122709.png", width=150) # The law logo image
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
        "Ted Bundy Case",
        "Arushi Talwar Case",
        "Jessica Lal Murder Case",
        "Sheena Bora Murder Case",
        "O.J. Simpson Case"
    ], label_visibility="collapsed")

    case_data = {} # This will be populated based on selection

    # --- CASE DATA DICTIONARY ---
    cases = {
        "Ted Bundy Case": {
            "name": "The Case of Ted Bundy",
            "timeline": [
                "<strong>1974-1978:</strong> Carries out a multi-state crime spree, murdering at least 30 young women and girls.",
                "<strong>1975 (August):</strong> First arrested in Utah for aggravated kidnapping and attempted criminal assault.",
                "<strong>1977 (June):</strong> Escapes from custody in Aspen, Colorado. Recaptured after 6 days.",
                "<strong>1977 (December):</strong> Escapes again from a jail in Glenwood Springs, Colorado.",
                "<strong>1978 (January):</strong> Murders two students at the Chi Omega sorority house in Florida.",
                "<strong>1978 (February):</strong> Abducts and murders 12-year-old Kimberly Leach. Arrested for the final time.",
                "<strong>1979 (July):</strong> Convicted for the Chi Omega murders and sentenced to death.",
                "<strong>1989 (January):</strong> Executed in Florida's electric chair after confessing to dozens of murders."
            ],
            "summary": "Ted Bundy was a charismatic American serial killer who kidnapped, raped, and murdered numerous young women and girls during the 1970s. He used his charm to gain victims' trust. His case gained notoriety for his two dramatic prison escapes and his decision to act as his own attorney, turning his trials into a media spectacle.",
            "verdict": "Convicted of three counts of first-degree murder, attempted murder, kidnapping, and burglary. He received three death sentences.",
            "laws": "First-Degree Murder (Florida Statutes), Aggravated Kidnapping (Utah Code), Burglary, Attempted Criminal Assault",
            "real_outcome": "Bundy was executed on January 24, 1989. His case profoundly impacted law enforcement, leading to a greater understanding of serial killer psychology and the development of the FBI's Behavioral Science Unit.",
            "ai_opinion": "The Ted Bundy case is a chilling study in the duality of human nature, where a facade of normalcy can mask extreme psychopathy. It highlights the critical importance of inter-state law enforcement communication and the value of behavioral science in criminal profiling. The case serves as a stark reminder of the manipulative capabilities of such offenders."
        },
"Arushi Talwar Case": {
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

        # ... (other cases would be formatted similarly)
    }
    # Add other cases here in the same format...
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
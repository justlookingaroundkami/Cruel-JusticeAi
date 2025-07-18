import streamlit as st
import base64
from tempfile import NamedTemporaryFile
from gtts import gTTS
import openai as OPENAI 

st.set_page_config(page_title="Cruel Justice", layout="wide")

def speak_text(text):
    try:
        tts = gTTS(text)
        with NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
        audio_bytes = open(fp.name, "rb").read()
        b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f"""<audio controls autoplay>
                           <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                        </audio>""",
                    unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Audio play failed: {e}")


def set_page_style(css):
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# --- GLOBAL STYLES (including glass, timeline, crime banner) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap"
      rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
<style>
    body, .stApp {
        background: #111; color: #eee;
        font-family: 'Roboto', sans-serif;
    }
    .stSidebar > div {
        background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(240,240,240,0.95) 100%);
        backdrop-filter: blur(10px); border-right:1px solid rgba(0,0,0,0.1); color:#333;
    }
    .stSidebar h1, .stSidebar h2 {
        color: #0f172a !important;
    }
    .stSidebar .stRadio label span { color: #333 !important; }

    .crime-scene-banner {
        position: relative;
        background: url('https://images.unsplash.com/photo-1589385554083-91d4e1a1f09f?...') center/cover no-repeat;
        height: 340px; border-radius: 12px; overflow: hidden;
        margin: 2em 0;
        box-shadow: inset 0 0 60px rgba(0,0,0,0.8), 0 6px 30px rgba(0,0,0,0.9);
    }
    .crime-scene-banner::after {
        content: '';
        position: absolute; inset: 0;
        background: radial-gradient(circle at center, rgba(0,0,0,0.4), rgba(0,0,0,0.9));
    }
    .flashlight {
        position: absolute; pointer-events: none;
        width:250px; height:250px;
        background: radial-gradient(circle at center, rgba(0,0,0,0), rgba(0,0,0,0.85) 60%);
        border-radius:50%; mix-blend-mode: destination-out;
        opacity:0.95; transition: transform 0.1s;
    }
    .crime-scene-content {
        position: relative; display: flex; align-items: center;
        gap: 1.5em; height: 100%; padding:1em 3em;
    }
    .crime-scene-content img {
        width: 140px; border: 4px solid #facc15;
        border-radius: 12px;
        box-shadow: 0 0 40px crimson;
        filter: brightness(1.3);
        transform: rotate(-2deg);
        transition: transform 0.2s;
    }
    .crime-scene-content img:hover {
        transform: rotate(0deg) scale(1.1);
    }
    .hero-text h1 {
        font-family: 'VT323', monospace; font-size: 5em;
        color: #ff4c4c; margin: 0;
        text-shadow: 4px 4px #220000;
        filter: brightness(1.4);
    }
    .hero-text p {
        font-size:1.4em; color:#f1f5f9; filter: brightness(1.2);
        margin-top:0.3em;
    }
    .police-tape {
        position:absolute; top:23%; left:-18%;
        width:160%; height:50px;
        background: repeating-linear-gradient(-45deg,
            #facc15,#facc15 20px,#000 20px,#000 40px);
        opacity:0.88;
        transform: rotate(-10deg);
        box-shadow: 0 0 14px rgba(0,0,0,0.7);
    }
    .blood-splatter {
        position:absolute; opacity:0.9;
    }
    .splatter1 { bottom:-20px; right:-40px; width:220px; transform:rotate(-15deg); }
    .splatter2 { top:30px; left:10px; width:180px; transform:rotate(25deg); }

    .header-box h1 {
        font-size: 3.5em; color: #facc15; letter-spacing: 2px;
        text-align:center; padding:1em 0;
    }

    .glass-container {
        background: rgba(30,41,59,0.5);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5em;
        border:1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.37);
        margin-bottom:1em;
    }

    .timeline-container {
        border-left: 3px solid #38bdf8;
        padding: 1em 2em; position: relative; list-style: none;
    }
    .timeline-item {
        margin-bottom: 2em; position: relative;
    }
    .timeline-item:before {
        content: '';
        background-color: #facc15;
        border: 3px solid #38bdf8;
        border-radius: 50%;
        width:20px; height:20px;
        position: absolute; left: -33px; top: 0;
    }
    .timeline-item-content {
        background: rgba(45,55,72,0.7);
        color:#fff;
        padding:1em;
        border-radius:8px;
    }
    .timeline-item-content strong {
        color:#facc15; font-weight:700;
    }
</style>

<div class="crime-scene-banner" onmousemove="moveSpot(event)">
  <div class="police-tape"></div>
  <img class="blood-splatter splatter1"
       src="https://www.pngmart.com/files/21/Blood-Splatter-PNG-Transparent-Image.png">
  <img class="blood-splatter splatter2"
       src="https://tse2.mm.bing.net/th/id/OIP.vnO7ZRm-2l--kOCS9MJCogHaHa?pid=Api&P=0&h=180">
  <div id="flashlight" class="flashlight"></div>
  <div class="crime-scene-content">
    <img src="https://judgeai.cloud/images/homepage_2.webp"
         alt="Cruel Justice Logo">
    <div class="hero-text">
      <h1>Cruel Justice</h1>
      <p>Uncover the Truth. Judge the Invisible.</p>
    </div>
  </div>
</div>

<script>
const f = document.getElementById('flashlight');
function moveSpot(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    f.style.transform = `translate(${e.clientX-rect.left-125}px, ${e.clientY-rect.top-125}px)`;
}
</script>

<audio autoplay loop hidden>
  <source src="https://cdn.pixabay.com/audio/2023/03/04/audio_2d93c0c328.mp3"
          type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

# --- SIDEBAR: OpenAI key + navigation ---
with st.sidebar:
    st.header("🔐 API Setup")
    OPENAI_API_KEY = st.text_input("Enter OpenAI API Key", type="password")
    if OPENAI_API_KEY:
        OPENAI.api_key = OPENAI_API_KEY

    st.header("🧭 Navigation")
    selected_page = st.radio(
        "Choose Mode:",
        ["🏠 Home", "📂 Explore Famous Cases", "🎭 Imaginary Case Creator", "🤖 AI Case Generator"],
        key="nav_mode"
    )

    if selected_page == "🏠 Home":
        st.title("🏠 Home")

    elif selected_page == "📂 Explore Famous Cases":
        st.title("📂 Famous Cases")

    elif selected_page == "🎭 Imaginary Case Creator":
        st.title("🎭 Imaginary Case Creator")

    elif selected_page == "🤖 AI Case Generator":
        st.title("🤖 AI Case Generator")

def set_page_style(css: str):
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
def set_page_background(page: str):
    if selected_page == "🏠 Home":
        set_page_style("""
        .stApp {
            background: radial-gradient(circle, #0a0a0a 0%, #2c2c2c 100%) !important;
            color: #f1f5f9 !important;
        }
        h1, h2, h3, h4, h5 {
            color: #facc15 !important;
            text-shadow: 1px 1px 2px #000;
        }
        .glass-container {
            background: rgba(30, 30, 30, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5em;
            backdrop-filter: blur(10px);
        }
        """)

    elif selected_page == "📂 Explore Famous Cases":
     set_page_style("""
    .stApp {
        background: radial-gradient(circle, #2d0000 0%, #000000 100%) !important;
        color: #f1f5f9 !important;
    }
    h1, h2, h3, h4, h5 {
        color: #ff4c4c !important;
        text-shadow: 1px 1px 2px #000;
    }
    .glass-container {
        background: rgba(60, 10, 10, 0.65);
        border: 1px solid rgba(255, 0, 0, 0.4);
        border-radius: 12px;
        padding: 1.5em;
        backdrop-filter: blur(12px);
    }
    .timeline-container {
        border-left: 4px solid crimson;
    }
    .timeline-item-content {
        background: rgba(90, 0, 0, 0.65);
        color: white;
    }
    """)

    elif selected_page == "🎭 Imaginary Case Creator":
     set_page_style("""
    .stApp {
        background: linear-gradient(145deg, #0a0f1a 0%, #1e293b 100%) !important;
        color: #e0f2fe !important;
    }
    h1, h2, h3 {
        color: #60a5fa !important;
    }
    .glass-container {
        background: rgba(30, 58, 138, 0.3);
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    """)

    elif selected_page == "🤖 AI Case Generator":
     set_page_style("""
    .stApp {
        background: linear-gradient(130deg, #0a0f0a 0%, #1f2937 100%) !important;
        color: #d1fae5 !important;
    }
    h1, h2, h3 {
        color: #34d399 !important;
    }
    .glass-container {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 12px;
        backdrop-filter: blur(8px);
    }
    """)


set_page_background(selected_page)

# --- PART 2: 📂 Famous Cases Section ---

if selected_page == "📂 Explore Famous Cases":
    st.header("📁 Select a Famous Criminal Case")

    case_option = st.selectbox(
        "Choose a case:",
        [
            "Aarushi Talwar Case",
            "Bhima Koregaon Case",
            "George Floyd Case",
            "Jessica Lal Murder Case",
            "Adnan Syed Case"
        ],
        label_visibility="collapsed"
    )

    cases = {
        "Aarushi Talwar Case": {
            "name": "Aarushi Talwar Case",
            "timeline": [
                "<strong>2008 (May 16):</strong> 14‑year‑old Aarushi Talwar found murdered in her bedroom in Noida, India.",
                "<strong>2008 (May 17):</strong> The family's domestic helper, Hemraj, initially prime suspect, found dead on the terrace.",
                "<strong>2013 (Nov):</strong> Parents convicted by trial court; global media storm ensues.",
                "<strong>2017 (Oct):</strong> Allahabad High Court acquits both citing lack of conclusive evidence."
            ],
            "summary": """The unsolved double murder of young Aarushi and the family's helper sparked allegations of sloppy investigation, sensationalist media coverage, and possible police negligence. Investigative lapses and chain-of-custody issues plagued the case, casting doubt on the reliability of evidence.""",
            "verdict": "Parents initially convicted to life imprisonment, then acquitted.",
            "laws": "IPC 302 (Murder), IPC 201 (Destruction of Evidence), IPC 34 (Common Intention)",
            "real_outcome": "Case remains officially unsolved; debate continues.",
            "ai_opinion": """AI highlights the disastrous combination of media pressure, poor forensic handling and shifting investigation teams. The flawed process undermines evidentiary value.""",
        },
        "Bhima Koregaon Case": {
            "name": "Bhima Koregaon Case",
            "timeline": [
                "<strong>2018:</strong> Commemoration event turns violent; arrests begin.",
                "<strong>2018–2021:</strong> Academics and activists held under UAPA with little trial progress.",
                "<strong>2022:</strong> Father‑Jesuit activist Stan Swamy dies in custody.",
                "<strong>2023:</strong> Several release on bail amid judiciary questioning evidence validity."
            ],
            "summary": """Activists alleged to have Maoist links were detained under anti-terror laws following a historical event's violence. The prolonged pre-trial incarceration and questionable digital evidence flags misuse of India's stringent statutes.""",
            "verdict": "Ongoing; no convictions yet, heavy bail rulings.",
            "laws": "UAPA | IPC 124A (Sedition), 120B (Conspiracy)",
            "real_outcome": "Highlighted judicial delays and civil liberties concerns.",
            "ai_opinion": """AI flags misuse of anti-terror provisions against dissent, stressing need for stringent evidence rules and expeditious trials."""
        },
        "George Floyd Case": {
            "name": "George Floyd Case",
            "timeline": [
                "<strong>2020:</strong> George Floyd dies under police restraint in Minneapolis.",
                "<strong>2020–2021:</strong> Protests erupt globally under #BlackLivesMatter.",
                "<strong>2021:</strong> Derek Chauvin found guilty of murder and sentenced to 22.5 years."
            ],
            "summary": """The death of George Floyd under police restraint sparked global outrage and ignited conversations on systemic racism, police reform, and human rights.""",
            "verdict": "Officer Chauvin convicted on all counts.",
            "laws": "US Title 18 Civil Rights Violations, Minnesota Murder Statutes",
            "real_outcome": "Conviction set precedent; systemic reforms remain incomplete.",
            "ai_opinion": """AI notes that individual verdicts cannot substitute for institutional change—calls for comprehensive policing reform."""
        },
        "Jessica Lal Murder Case": {
            "name": "Jessica Lal Case",
            "timeline": [
                "<strong>1999:</strong> Jessica Lal shot dead at a Delhi party by Manu Sharma.",
                "<strong>2006:</strong> Delhi HC overturns acquittal following public uproar.",
                "<strong>2010:</strong> SC upholds conviction; Sharma sentenced to life.",
                "<strong>2020:</strong> Sharma released early on remission."
            ],
            "summary": """A high-profile murder of a model where initial acquittal due to witness tampering sparked massive public outrage and media reform campaigns.""",
            "verdict": "Convicted and later released early.",
            "laws": "IPC 302 (Murder), 201 (Evidence Tampering)",
            "real_outcome": "Highlighted power, media role, and judicial integrity.",
            "ai_opinion": """AI underscores importance of witness protection and transparent judicial processes in politically-tainted cases."""
        },
        "Adnan Syed Case": {
            "name": "Adnan Syed / Serial Podcast Case",
            "timeline": [
                "<strong>1999:</strong> Hae Min Lee murdered; Syed convicted largely on circumstantial evidence.",
                "<strong>2014:</strong> 'Serial' podcast revives interest and scrutiny.",
                "<strong>2016–2022:</strong> Appeals for ineffective counsel, faulty timelines, unreliable witnesses.",
                "<strong>2022:</strong> Court vacates conviction; Syed released."
            ],
            "summary": """Convicted based on single witness and phone data inconsistencies. Media-driven scrutiny helped uncover gaps in forensic procedures and defense rights.""",
            "verdict": "Conviction vacated in favor of retrial.",
            "laws": "Maryland Code – First‑degree Murder, Fifth‑Amendment Rights",
            "real_outcome": "Raises concerns about wrongful convictions and forensic reliability.",
            "ai_opinion": """AI emphasizes effective legal representation and evidence review, especially in cases of circumstantial reliance."""
        }
    }

    case_data = cases.get(case_option)
    if case_data:
        st.markdown(f"## 🧾 {case_data['name']}")
        st.markdown("---")

        col1, col2 = st.columns((1, 1))
        with col1:
            st.markdown("### 🕒 Timeline of Events")
            timeline_html = "<ul class='timeline-container'>"
            for ev in case_data["timeline"]:
                timeline_html += f"<li class='timeline-item'><div class='timeline-item-content'>{ev}</div></li>"
            timeline_html += "</ul>"
            st.markdown(timeline_html, unsafe_allow_html=True)

        with col2:
            st.markdown("### 📋 Summary")
            st.markdown(f"<div class='glass-container content-box'>{case_data['summary']}</div>", unsafe_allow_html=True)
            st.markdown("### ⚖️ Verdict")
            st.success(case_data['verdict'])
            st.markdown("### 📌 Real Outcome")
            st.info(case_data['real_outcome'])

        st.markdown("---")
        st.markdown("### 🧠 AI’s Insight & Legal Commentary")
        ai_col1, ai_col2 = st.columns(2)
        with ai_col1:
            st.markdown(f"<div class='glass-container content-box'><strong>Applicable Laws:</strong><br>{case_data['laws']}</div>", unsafe_allow_html=True)
        with ai_col2:
            st.markdown(f"<div class='glass-container content-box'><strong>AI Opinion:</strong><br>{case_data['ai_opinion']}</div>", unsafe_allow_html=True)

        if st.button("▶️ Play AI Opinion Audio"):
            speak_text(case_data['ai_opinion'])
elif selected_page == "🎭 Imaginary Case Creator":
    st.header("🎭 Build a Hypothetical Case")
    st.markdown("Enter the crime profile and receive a full case report:")

    case_data = None  # placeholder to use later outside form

    with st.form("imaginary_form"):
        col1, col2 = st.columns(2)
        with col1:
            case_name = st.text_input("Case Name", placeholder="E.g. The Red Garden Mystery")
            age = st.selectbox("Age Group", ["Under 18", "18–30", "31–50", "51+"])
            gender = st.selectbox("Gender", ["Male", "Female", "Non-binary"])
            country = st.selectbox("Country", ["India", "USA", "UK", "Other"])
        with col2:
            crime = st.selectbox("Crime Type", ["Murder", "Fraud", "Assault", "Cybercrime", "Corruption"])
            motive = st.text_area("Suspected Motive", max_chars=200)
            evidence = st.text_area("Key Evidence", max_chars=200)

        submitted = st.form_submit_button("🧠 Generate Case Report")

    if submitted:
        base = {"Murder": 20, "Fraud": 10, "Assault": 8, "Cybercrime": 12, "Corruption": 15}
        est = base.get(crime, 10)
        est_text = f"Estimated prison sentence: **~{est} years**"

        timeline = [
            f"**Event 1:** In {country}, a {age.lower()} {gender.lower()} was suspected of committing {crime.lower()} following unusual activity noticed by authorities.",
            f"**Event 2:** The crime was officially classified as **{crime}** based on preliminary investigations and evidence.",
            f"**Event 3:** Suspected motive identified: *{motive or 'Unknown'}*. Investigators suspect psychological, financial, or ideological factors.",
            f"**Event 4:** Key evidence submitted includes: *{evidence or 'No details disclosed'}*. Investigators began forensic analysis.",
            f"**Event 5:** The case proceeded to pre-trial where charges were formally framed, drawing attention due to its nature.",
            f"**Event 6:** Prosecution began collecting testimonies and expert statements to build a strong case."
        ]

        law_map = {
            "Murder": "IPC Section 302 (Murder)",
            "Fraud": "IPC Section 420 (Cheating & dishonesty)",
            "Assault": "IPC Section 351 (Assault)",
            "Cybercrime": "IPC Section 66 (Computer Fraud)",
            "Corruption": "IPC Section 7 (Corruption under PC Act)"
        }

        summary = (
            f"This hypothetical case revolves around a {age} {gender} from {country}, "
            f"accused of {crime.lower()}. With {motive or 'undisclosed'} motives and evidence "
            f"like {evidence or 'unavailable materials'}, the authorities launched a full-scale investigation."
        )

        opinion = (
            f"This case reflects good adherence to early investigative standards. "
            f"However, motive clarity and unbiased handling will be key in ensuring justice is achieved."
        )

        # Save case report in a variable so we can use after form
        case_data = {
            "name": case_name or "Unnamed Case",
            "timeline": timeline,
            "summary": summary,
            "verdict": f"Defendant found guilty of {crime.lower()}",
            "real_outcome": est_text,
            "laws": law_map.get(crime, "TBD by Jurisdiction"),
            "ai_opinion": opinion
        }

    # Display Output (outside form)
    if case_data:
        st.markdown(f"### 🧾 {case_data['name']}")
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🕒 Timeline")
            html = "<ul class='timeline-container'>"
            for e in case_data["timeline"]:
                html += f"<li class='timeline-item'><div class='timeline-item-content'>{e}</div></li>"
            html += "</ul><hr>"
            st.markdown(html, unsafe_allow_html=True)

        with c2:
            st.markdown("#### 📋 Summary")
            st.markdown(f"<div class='glass-container'>{case_data['summary']}</div>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("#### ⚖️ Verdict")
            st.success(case_data["verdict"])
            st.markdown("#### 📌 Real Outcome")
            st.info(case_data["real_outcome"])
            st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("#### 📜 Applicable Laws")
        st.markdown(f"<div class='glass-container'><strong>{case_data['laws']}</strong></div>", unsafe_allow_html=True)

        st.markdown("#### 🧠 AI Opinion")
        st.markdown(f"<div class='glass-container'><strong>AI Ethical Insight:</strong><br>{case_data['ai_opinion']}</div>", unsafe_allow_html=True)

        if st.button("▶️ Play AI Opinion Audio", key="play_ai_op"):
            speak_text(case_data["ai_opinion"])

# -------------------- PAGE: AI GENERATOR --------------------
elif selected_page == "🤖 AI Case Generator":
    st.header("🤖 AI Case Analyzer")
    st.markdown("Paste or upload a case summary. AI will analyze it.")
    input_method = st.radio("Choose input:", ["Text", "Upload File"], key="ai_method")
    case_text = ""
    if input_method == "Text":
        case_text = st.text_area("Paste case details here:")
    else:
        uploaded = st.file_uploader("Upload .txt file", type="txt")
        if uploaded:
            case_text = uploaded.read().decode("utf-8")
    if case_text and OPENAI_API_KEY:
        if st.button("🔍 Analyze Case"):
            with st.spinner("Analyzing..."):
                try:
                    prompt = f"""You are a legal AI. Respond in markdown:
## Summary:
## Timeline:
## Laws:
## Gaps:
## Outcome:
## Ethical Insight:
## Recommendation:

Case Details:
{case_text}
"""
                    resp = OPENAI.ChatCompletion.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    analysis = resp["choices"][0]["message"]["content"]
                    st.markdown(f"<div class='glass-container'>{analysis}</div>", unsafe_allow_html=True)
                    if st.button("▶️ Listen to Analysis"):
                        speak_text(analysis)
                except Exception as e:
                    st.error("AI analysis failed")
                    st.code(str(e))
    elif not OPENAI_API_KEY:
        st.warning("Please enter your OpenAI API Key in the sidebar.")  

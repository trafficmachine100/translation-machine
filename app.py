import streamlit as st
from translator import translate_text, translate_file
from utils import detect_language, LANGUAGES
import datetime

# ─── Configuration de la page ───────────────────────────────────────────────
st.set_page_config(
    page_title="No_Limit Translation Machine",
    page_icon="🌐",
    layout="wide"
)

# ─── CSS personnalisé ─────────────────────────────────────────────────────────
st.markdown("""
<style>
.hero-box {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid #f0a500;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 28px;
    text-align: center;
}
.hero-title {
    font-size: 2em;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 1px;
    margin-bottom: 4px;
}
.hero-title span {
    color: #f0a500;
}
.hero-tagline {
    font-size: 1.15em;
    color: #f0a500;
    font-weight: 700;
    margin-bottom: 10px;
}
.hero-desc {
    font-size: 0.97em;
    color: #cccccc;
    margin-bottom: 10px;
    line-height: 1.7;
}
.hero-langs {
    font-size: 1em;
    color: #f0a500;
    font-weight: 600;
    letter-spacing: 2px;
}
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ─── LOGO + Hero Section ──────────────────────────────────────────────────────
logo_url = "https://raw.githubusercontent.com/trafficmachine100/translation-machine/master/LOGO1.png"
col_logo, col_hero = st.columns([1, 3])

with col_logo:
    st.image(logo_url, width=180)

with col_hero:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">No_Limit_Translation,<span>MACHINE</span></div>
        <div class="hero-tagline">— Translate unlimited text for free! —</div>
        <div class="hero-desc">
            No 5,000-character restriction like Google Translate.<br>
            Paste any size text. Get instant translation.
        </div>
        <div class="hero-langs">English &nbsp;·&nbsp; French &nbsp;·&nbsp; Arabic &nbsp;·&nbsp; Always Free</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ─── Initialisation session ───────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "output_text" not in st.session_state:
    st.session_state.output_text = ""

# ─── Layout principal ─────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Source Text")

    lang_names = list(LANGUAGES.keys())
    source_lang = st.selectbox("Source language", lang_names, index=0, key="source")

    # Boutons Clear + Paste SOURCE
    b1, b2 = st.columns(2)
    with b1:
        if st.button("🗑️ Clear", key="clear_src", use_container_width=True):
            st.session_state.input_text = ""
            st.rerun()
    with b2:
        if st.button("📋 Paste", key="paste_src", use_container_width=True):
            try:
                import subprocess
                result = subprocess.run(
                    ["powershell", "-command", "Get-Clipboard"],
                    capture_output=True, text=True
                )
                st.session_state.input_text = result.stdout.strip()
                st.rerun()
            except:
                st.warning("⚠️ Paste not available on cloud — use Ctrl+V directly.")

    input_text = st.text_area(
        label="Enter your text here",
        value=st.session_state.input_text,
        height=320,
        placeholder="Paste or type your text here... (no character limit)",
        key="input_area"
    )
    st.session_state.input_text = input_text

    char_count = len(input_text)
    st.caption(f"📊 {char_count:,} characters")

    if input_text.strip():
        detected = detect_language(input_text)
        st.info(f"🔍 Detected language : **{detected}**")

    st.divider()
    st.subheader("📂 Or import a .txt file")
    uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        st.session_state.input_text = file_content
        input_text = file_content
        st.success(f"✅ File loaded : {len(file_content):,} characters")
        st.text_area("File preview", file_content[:500] + "...", height=120)

with col2:
    st.subheader("🎯 Translation")

    target_lang = st.selectbox("Target language", lang_names, index=1, key="target")

    translate_btn = st.button("🚀 Translate", type="primary", use_container_width=True)

    if translate_btn:
        if not input_text.strip():
            st.warning("⚠️ Please enter text or import a file.")
        elif source_lang == target_lang:
            st.warning("⚠️ Source and target languages are the same.")
        else:
            with st.spinner("⏳ Translating..."):
                result = translate_text(input_text, source_lang, target_lang)
            st.session_state.output_text = result

    # Zone résultat
    output_text = st.session_state.output_text

    # Boutons Clear + Paste TRADUCTION
    b3, b4 = st.columns(2)
    with b3:
        if st.button("🗑️ Clear", key="clear_tgt", use_container_width=True):
            st.session_state.output_text = ""
            st.rerun()
    with b4:
        if st.button("📋 Paste", key="paste_tgt", use_container_width=True):
            try:
                import subprocess
                result_clip = subprocess.run(
                    ["powershell", "-command", "Get-Clipboard"],
                    capture_output=True, text=True
                )
                st.session_state.output_text = result_clip.stdout.strip()
                st.rerun()
            except:
                st.warning("⚠️ Paste not available on cloud — use Ctrl+V directly.")

    st.text_area(
        label="Translation result",
        value=output_text,
        height=320,
        key="output_area"
    )

    if output_text:
        st.caption(f"📊 {len(output_text):,} characters translated")

        st.download_button(
            label="💾 Download translation (.txt)",
            data=output_text.encode("utf-8"),
            file_name=f"translation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

        if translate_btn and input_text.strip():
            st.session_state.history.append({
                "date": datetime.datetime.now().strftime("%H:%M:%S"),
                "source": source_lang,
                "target": target_lang,
                "input": input_text[:80] + "..." if len(input_text) > 80 else input_text,
                "output": output_text[:80] + "..." if len(output_text) > 80 else output_text
            })

# ─── Historique ───────────────────────────────────────────────────────────────
st.divider()
st.subheader("🕒 Translation History")

if st.session_state.history:
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

    for item in reversed(st.session_state.history):
        with st.expander(f"[{item['date']}] {item['source']} → {item['target']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Source :**")
                st.write(item["input"])
            with c2:
                st.markdown("**Translation :**")
                st.write(item["output"])
else:
    st.caption("No translations yet in this session.")

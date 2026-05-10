import streamlit as st
from translator import translate_text, translate_file
from utils import detect_language, LANGUAGES
import datetime

# ─── Configuration de la page ───────────────────────────────────────────────
st.set_page_config(
    page_title="Translation Machine",
    page_icon="🌐",
    layout="wide"
)

# ─── Titre principal ─────────────────────────────────────────────────────────
st.title("🌐 Translation Machine")
st.caption("Traduction sans limite · Anglais · Français · Arabe")
st.divider()

# ─── Initialisation de l'historique ──────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ─── Layout : deux colonnes principales ──────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Texte source")

    # Sélection langue source
    lang_names = list(LANGUAGES.keys())
    source_lang = st.selectbox("Langue source", lang_names, index=0, key="source")

    # Zone de texte source
    input_text = st.text_area(
        label="Entrez votre texte ici",
        height=300,
        placeholder="Collez ou tapez votre texte ici... (sans limite de caractères)",
        key="input_text"
    )

    # Compteur de caractères
    char_count = len(input_text)
    st.caption(f"📊 {char_count:,} caractères")

    # Détection automatique
    if input_text.strip():
        detected = detect_language(input_text)
        st.info(f"🔍 Langue détectée : **{detected}**")

    # Import fichier .txt
    st.divider()
    st.subheader("📂 Ou importer un fichier .txt")
    uploaded_file = st.file_uploader("Choisir un fichier .txt", type=["txt"])
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        input_text = file_content
        st.success(f"✅ Fichier chargé : {len(file_content):,} caractères")
        st.text_area("Aperçu du fichier", file_content[:500] + "...", height=150)

with col2:
    st.subheader("🎯 Traduction")

    # Sélection langue cible
    target_lang = st.selectbox("Langue cible", lang_names, index=1, key="target")

    # Bouton traduire
    translate_btn = st.button("🚀 Traduire", type="primary", use_container_width=True)

    # Zone résultat
    result_area = st.empty()

    if translate_btn:
        if not input_text.strip():
            st.warning("⚠️ Veuillez entrer un texte ou importer un fichier.")
        elif source_lang == target_lang:
            st.warning("⚠️ La langue source et cible sont identiques.")
        else:
            with st.spinner("⏳ Traduction en cours..."):
                result = translate_text(input_text, source_lang, target_lang)

            # Affiche le résultat
            st.text_area(
                label="Résultat",
                value=result,
                height=300,
                key="output"
            )

            st.caption(f"📊 {len(result):,} caractères traduits")

            # Export résultat en .txt
            st.download_button(
                label="💾 Télécharger la traduction (.txt)",
                data=result.encode("utf-8"),
                file_name=f"traduction_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

            # Sauvegarde dans l'historique
            st.session_state.history.append({
                "date": datetime.datetime.now().strftime("%H:%M:%S"),
                "source": source_lang,
                "target": target_lang,
                "input": input_text[:80] + "..." if len(input_text) > 80 else input_text,
                "output": result[:80] + "..." if len(result) > 80 else result
            })

# ─── Historique ──────────────────────────────────────────────────────────────
st.divider()
st.subheader("🕒 Historique des traductions")

if st.session_state.history:
    # Bouton effacer historique
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.history = []
        st.rerun()

    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"[{item['date']}] {item['source']} → {item['target']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Source :**")
                st.write(item["input"])
            with c2:
                st.markdown("**Traduction :**")
                st.write(item["output"])
else:
    st.caption("Aucune traduction effectuée dans cette session.")
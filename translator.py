from deep_translator import GoogleTranslator
from utils import split_text, LANGUAGES


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Traduit un texte sans limite de caractères.
    - Découpe intelligemment le texte en morceaux
    - Traduit chaque morceau
    - Réassemble le résultat final
    """
    if not text.strip():
        return ""

    if source_lang == target_lang:
        return text

    # Récupère les codes langue (ex: "fr", "ar", "en")
    src_code = LANGUAGES.get(source_lang, "en")
    tgt_code = LANGUAGES.get(target_lang, "en")

    # Découpe le texte en morceaux intelligents
    chunks = split_text(text, max_chunk=4500)

    translated_chunks = []

    for chunk in chunks:
        try:
            translator = GoogleTranslator(
                source=src_code,
                target=tgt_code
            )
            result = translator.translate(chunk)
            translated_chunks.append(result if result else chunk)
        except Exception as e:
            translated_chunks.append(f"[Erreur de traduction : {e}]")

    return "\n".join(translated_chunks)


def translate_file(file_content: str, source_lang: str, target_lang: str) -> str:
    """
    Traduit le contenu complet d'un fichier .txt
    """
    return translate_text(file_content, source_lang, target_lang)
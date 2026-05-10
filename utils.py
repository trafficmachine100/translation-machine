from langdetect import detect

# Langues supportées
LANGUAGES = {
    "Anglais 🇬🇧": "en",
    "Français 🇫🇷": "fr",
    "Arabe 🇸🇦":    "ar"
}

LANG_CODE_TO_NAME = {v: k for k, v in LANGUAGES.items()}


def detect_language(text: str) -> str:
    """Détecte automatiquement la langue du texte source."""
    try:
        code = detect(text)
        return LANG_CODE_TO_NAME.get(code, "Anglais 🇬🇧")
    except Exception:
        return "Anglais 🇬🇧"


def split_text(text: str, max_chunk: int = 4500) -> list[str]:
    """
    Découpe le texte en morceaux intelligents :
    - Respecte les fins de phrases (. ! ?)
    - Ne coupe jamais un mot en plein milieu
    - Chaque morceau <= max_chunk caractères
    """
    if len(text) <= max_chunk:
        return [text]

    chunks = []
    while len(text) > max_chunk:
        # Cherche la dernière fin de phrase avant max_chunk
        cut = max_chunk
        for sep in [". ", "! ", "? ", "\n"]:
            pos = text.rfind(sep, 0, max_chunk)
            if pos != -1 and pos > cut - 500:
                cut = pos + len(sep)
                break
        else:
            # Pas de ponctuation trouvée → coupe au dernier espace
            pos = text.rfind(" ", 0, max_chunk)
            cut = pos if pos != -1 else max_chunk

        chunks.append(text[:cut].strip())
        text = text[cut:].strip()

    if text:
        chunks.append(text)

    return chunks
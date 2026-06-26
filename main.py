import langcodes
import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import DetectorFactory, LangDetectException, detect
from nltk.tokenize import TreebankWordDetokenizer, wordpunct_tokenize
from spellchecker import SpellChecker

DetectorFactory.seed = 0
MIN_INPUT_LENGTH = 3

# pyspellchecker chỉ hỗ trợ một số ngôn ngữ
SPELL_LANGS = {"en", "es", "fr", "pt", "de", "ru", "ar", "eu", "lv", "nl"}

# Ngôn ngữ đích cho App 1
TARGET_LANGS = {
    "Tiếng Việt": "vi",
    "Tiếng Anh": "en",
    "Tiếng Pháp": "fr",
    "Tiếng Nhật": "ja",
    "Tiếng Trung (Giản thể)": "zh-CN",
    "Tiếng Hàn": "ko",
    "Tiếng Tây Ban Nha": "es",
    "Tiếng Đức": "de",
}

EXAMPLES_T = [
    "Every morning, I drink a cup of coffee.",
    "Bonjour, comment allez-vous?",
    "Xin chào, hôm nay trời đẹp quá.",
]
EXAMPLES_S = [
    "Yesturday, I recieveed a mesage from my freind.",
    "Definately a great oppurtunity.",
    "Je voudraiis allerr au marchee.",
]

# ---------------- Helpers ----------------
@st.cache_resource(show_spinner=False)
def get_spellchecker(code):
    return SpellChecker(language=code)

def language_name(code):
    try:
        return langcodes.Language.get(code).display_name()
    except Exception:
        return code or "Unknown"


def detect_language(raw):
    try:
        return detect(raw)
    except LangDetectException:
        return None

def fix_typos(text, code):
    spell = get_spellchecker(code) # load model sửa lỗi cho ngôn ngữ code
    tokens = wordpunct_tokenize(text) # tách câu thành từ hello world => [hello, world]
    fixed = []
    for token in tokens:
        if token.isalpha() and len(token) > 1:
            suggestion = spell.correction(token.lower()) or token # sửa lỗi
            # chuyển đúng format ban đầu: viết hoa hoặc không
            suggestion = suggestion.title() if token.istitle() else suggestion
            suggestion = suggestion.upper() if token.isupper() else suggestion
            fixed.append(suggestion)
        else:
            # 12$
            fixed.append(token)
    return TreebankWordDetokenizer().detokenize(fixed), fixed != tokens # nối list từ => từ
    # " ".join(words)

def run_translation(text, target_code):
    raw = text.strip()
    if len(raw) < MIN_INPUT_LENGTH:
        return {"ok": False, "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."}

    source = detect_language(raw)
    if source is None:
        return {"ok": False, "error": "Không nhận diện được ngôn ngữ."}

    if source == target_code:
        return {
            "ok": True,
            "source": language_name(source),
            "target": language_name(target_code),
            "translated": raw,
            "note": "Câu đã ở ngôn ngữ đích, không cần dịch.",
        }

    try:
        translated = GoogleTranslator(source=source, target=target_code).translate(raw)
    except Exception as e:
        return {"ok": False, "error": f"Lỗi dịch: {e}"}

    return {
        "ok": True,
        "source": language_name(source),
        "target": language_name(target_code),
        "translated": translated,
    }

def run_spellcheck(text):
    raw = text.strip()
    if len(raw) < MIN_INPUT_LENGTH:
        return {"ok": False, "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."}

    code = detect_language(raw)
    if code is None:
        return {"ok": False, "error": "Không nhận diện được ngôn ngữ."}

    if code not in SPELL_LANGS:
        return {
            "ok": False,
            "error": f"pyspellchecker chưa hỗ trợ {language_name(code)} ({code}).",
        }

    fixed, changed = fix_typos(raw, code)
    return {
        "ok": True,
        "language": language_name(code),
        "fixed": fixed,
        "changed": changed,
    }

st.title("Streamlit NLP App")
st.caption("Hai ứng dụng: Dịch văn bản và sửa lỗi chính tả")
tab_t, tab_s = st.tabs(["Dịch văn bản", "Sửa lỗi chính tả"])

with tab_t:
    st.session_state.setdefault("res_t", None)

    with st.expander("Ví dụ"):
        for ex in EXAMPLES_T:
            st.markdown(f"- {ex}")

    with st.form("form_translate"):
        text_t = st.text_area("Câu cần dịch", height=90,
                              placeholder="Nhập câu ở bất kỳ ngôn ngữ nào...")
        target = st.selectbox("Dịch sang", list(TARGET_LANGS.keys()))
        submitted_t = st.form_submit_button("Dịch", type="primary")

    if submitted_t:
        st.session_state.res_t = run_translation(text_t, TARGET_LANGS[target])

    res = st.session_state.res_t
    if res:
        if res["ok"]:
            st.caption(f"Nguồn: {res['source']}  →  Đích: {res['target']}")
            st.success(res["translated"])
            if res.get("note"):
                st.info(res["note"])
        else:
            st.warning(res["error"])

with tab_s:
    st.session_state.setdefault("res_s", None)

    with st.expander("Ví dụ"):
        for ex in EXAMPLES_S:
            st.markdown(f"- {ex}")
    st.caption(f"Hỗ trợ: {', '.join(sorted(SPELL_LANGS))}")

    with st.form("form_spell"):
        text_s = st.text_area("Câu cần kiểm tra", height=90,
                              placeholder="Nhập câu để kiểm tra chính tả...")
        submitted_s = st.form_submit_button("Kiểm tra", type="primary")

    if submitted_s:
        st.session_state.res_s = run_spellcheck(text_s)

    res = st.session_state.res_s
    if res:
        if res["ok"]:
            st.caption(f"Ngôn ngữ: {res['language']}")
            st.success(res["fixed"])
            st.caption("Có sửa lỗi chính tả" if res["changed"] else "Không phát hiện lỗi")
        else:
            st.warning(res["error"])

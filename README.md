# Streamlit NLP Applications Showcase

This repository contains introductory and advanced implementations of interactive web applications built with **Streamlit** for Natural Language Processing (NLP) tasks. It serves as a comprehensive reference guide for building, testing, and deploying data science and machine learning prototypes using pure Python.

---

## 📂 Repository Structure

The repository consists of two main components:

1. **`app.py`**: A foundational script showcasing standard Streamlit UI widgets, layout options, media rendering, state management, and basic user interactions.
2. **`[Code-Class]-Streamlit.ipynb`**: An interactive Jupyter Notebook demonstrating how to configure Streamlit inside a Google Colab/Linux cloud environment, handle external tunneling via Cloudflare, and construct a multi-tab production-grade NLP suite covering **Machine Translation** and **Spell Checking / Typo Correction**.

---

## 🛠️ Detailed Architecture & Code Walkthrough

### 1. Core Core Application Elements (`app.py`)
This script showcases the primary blocks of any interactive interactive app:
* **Text & Typography Layouts:** Uses `st.title()`, `st.header()`, `st.subheader()`, `st.markdown()`, and `st.latex()` to display rich formatted text and mathematical formulas (e.g., Bayes' Theorem).
* **Media Rendering:** Exhibits standard methods for embedding branding assets or media via `st.logo()`, `st.image()`, `st.audio()`, and `st.video()`.
* **Interactive Controls:** Includes a collection of user input widgets:
  * `st.selectbox()` for single-choice operations.
  * `st.checkbox()` for conditional rendering toggles.
  * `st.slider()`, `st.text_input()`, and `st.number_input()` for collecting structured parameter inputs.
  * `st.file_uploader()` supporting dynamic file reading (`.txt`, `.csv`, `.pdf`) and partial content decoding.
* **State Management (`st.session_state`):** Implements counter mechanisms that maintain variable states across reactive widget re-runs.
* **Form Optimization (`with st.form`):** Groups widgets together so that full app execution occurs only upon pressing the `st.form_submit_button()`, minimizing intermediate loading times.
* **Resource Caching:** Employs `@st.cache_resource` to simulate and optimize loading times for computationally heavy model pipelines or assets.

### 2. Advanced Multi-Tab NLP Production Suite (`main.py` via Notebook)
The Jupyter notebook advances into a multi-purpose language toolkit using complex third-party NLP libraries. It leverages the following backends:
* **Language Detection (`langdetect`):** Automatically identifies the underlying language from a text stream.
* **Machine Translation (`deep-translator`):** Couples text streams with the Google Translation API to translate text seamlessly across standard languages (Vietnamese, English, French, Japanese, Chinese, Korean, Spanish, and German).
* **Contextual Spell-Checking (`pyspellchecker` & `nltk`):** Tokenizes incoming strings via `wordpunct_tokenize()`, runs corrections through localized vocabulary maps, handles capitalization alignment, and detokenizes back to a clean text output string via `TreebankWordDetokenizer()`.

---

## 🚀 Local Installation & Deployment

Follow these steps to configure your environment and run the apps locally:

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
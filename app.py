import streamlit as st
import time

st.title("Demo Streamlit App")
st.header("Phân tích văn bản")
st.subheader("Kết quả dịch")
st.text("I go to school")
st.markdown("**Streamlit** support *Markdown*")
st.latex(r"p(y|x) = \frac{p(x|y)p(y)}{p(x)}")

label = "Positive"
st.write(label)
st.write("I go to school")

code = """
def process(text):
    return text.lower()
"""
st.code(code, language="python")
with st.echo():
    text = "NLP Demo".lower()
    st.write("Result: ", text)

st.logo("photo.jpeg")
st.image("photo.jpeg", caption="Background image")
st.audio("photo.jpeg")
st.video("photo.jpeg")

option = st.selectbox(
    "Chọn tác vụ của NLP",
    ["Tóm tắt", "Dịch máy", "Hỏi đáp"], 
    )
st.write("You selected:", option)

status = st.checkbox("Hiển thị văn bản")
if status:
    st.write(status)

st.slider("Nguong gia tri", min_value=1.0, max_value=5.0, step=0.5)
name = st.text_input("Your name:")
st.write(name)

age = st.number_input("Your age:")
st.write(age)

if st.button("Run"):
    st.write(name, age)

uploaded_file = st.file_uploader("Tai file len", type=["txt", "csv", "pdf"])
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    st.write(content[:10])

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# prompt = st.chat_input("Nhập câu hỏi vào đây")
# if prompt:
#     st.session_state.messages.append(
#         {"role": "user", "content": prompt}
#     )
#     response = "Đây là NLP Model"
#     st.session_state.messages.append(
#         {"role": "assistant", "content": response}
#     )

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])


if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increment"):
    st.session_state.count += 1

st.write("Count: ", st.session_state.count)

with st.form("nlp_form"):
    name = st.text_area("nhập tên")
    task = st.selectbox("Tác vụ",
                        ["A", "B", "C"])
    submitted = st.form_submit_button("run")
if submitted:
    st.write(name)
    st.write(task)

@st.cache_resource(show_spinner=False)
def load_heavy_resource():
    time.sleep(3)
    return {"status": "loaded"}

resource = load_heavy_resource()
st.write("Recource:", resource)
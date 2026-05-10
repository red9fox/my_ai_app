import streamlit as st
from groq import Groq

# 1. Настройка страницы
st.set_page_config(page_title="AI Pro Studio", layout="wide", page_icon="🧬")

# 2. Визуальный стиль (Исправленный и Улучшенный)
st.markdown("""
    <style>
    @import url('https://googleapis.com');

    .stApp {
        background-color: #161621;
        color: #E0E0E0;
        font-family: 'Poppins', sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #1F1D2B !important;
        border-right: 1px solid #2D2D44;
    }

    [data-testid="stChatMessage"] {
        background-color: #1F1D2B !important;
        border-radius: 28px !important;
        border: 1px solid #2D2D44 !important;
        padding: 25px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }

    .stButton>button {
        background: linear-gradient(135deg, #8A2BE2 0%, #FF007F 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.4s ease;
    }

    .stChatInputContainer input {
        background-color: #2D2D44 !important;
        border: 1px solid #3F3F5F !important;
        border-radius: 20px !important;
        color: white !important;
    }

    h1 {
        background: linear-gradient(to right, #FF007F, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }

    img { border-radius: 25px; border: 1px solid #2D2D44; }
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Функционал
with st.sidebar:
    st.markdown("### 🎛️ ПАНЕЛЬ УПРАВЛЕНИЯ")
    api_key = st.text_input("ВВОД КЛЮЧА:", type="password")
    st.divider()
    character = st.selectbox("СТИЛЬ УЧИТЕЛЯ:", ["Дружелюбный ИИ", "Кибер-Наставник", "Профессор"])
    voice_type = st.radio("ГОЛОС:", ["Женский", "Мужской"])

def speak(text, voice):
    p = "1.2" if voice == "Женский" else "0.8"
    c_t = text.replace("'", "").replace('"', '').replace("\n", " ").replace("*", "")
    js = f"<script>var m=new SpeechSynthesisUtterance('{c_t}');m.lang='ru-RU';m.pitch={p};window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

st.title("SMART LESSON STUDIO")

if api_key:
    try:
        client = Groq(api_key=api_key)
        query = st.chat_input("Введите тему для урока...")

        if query:
            with st.spinner("🧬 СИНТЕЗ ЗНАНИЙ..."):
                chat = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Ты — эксперт. Стиль: {character}."},
                        {"role": "user", "content": query}
                    ],
                    model="llama-3.3-70b-versatile"
                )
                res = chat.choices[0].message.content
                
                with st.chat_message("assistant"):
                    st.markdown(res)
                
                img_url = f"https://pollinations.ai{query.replace(' ','-')}?width=1024&height=768&nologo=true"
                st.image(img_url)
                
                speak(res, voice_type)
                st.download_button("💾 СКАЧАТЬ ЛОГ", res, file_name="lesson.txt")
    except Exception as e:
        st.error(f"ОШИБКА: {e}")
else:
    st.info("💎 АКТИВИРУЙТЕ СИСТЕМУ КЛЮЧОМ В МЕНЮ СЛЕВА.")

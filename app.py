import streamlit as st
from groq import Groq

# 1. Настройка страницы
st.set_page_config(page_title="AI Pro Studio", layout="wide", page_icon="🧬")

# 2. Визуальный стиль "Deep Purple UI"
st.markdown("""
    <style>
    @import url('https://googleapis.com');

    /* Основной фон приложения */
    .stApp {
        background-color: #161621;
        color: #E0E0E0;
        font-family: 'Poppins', sans-serif;
    }

    /* Боковая панель */
    [data-testid="stSidebar"] {
        background-color: #1F1D2B !important;
        border-right: 1px solid #2D2D44;
    }

    /* Карточки уроков с эффектом глубины */
    [data-testid="stChatMessage"] {
        background-color: #1F1D2B !important;
        border-radius: 28px !important;
        border: 1px solid #2D2D44 !important;
        padding: 25px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }

    /* Кнопка с ярким градиентом как на референсе */
    .stButton>button {
        background: linear-gradient(135deg, #8A2BE2 0%, #FF007F 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(255, 0, 127, 0.5);
    }

    /* Поле ввода - современный темный стиль */
    .stChatInputContainer input {
        background-color: #2D2D44 !important;
        border: 1px solid #3F3F5F !important;
        border-radius: 20px !important;
        color: white !important;
        padding: 15px !important;
    }

    /* Заголовки с неоновым оттенком */
    h1 {
        font-weight: 600 !important;
        background: linear-gradient(to right, #FF007F, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 40px !important;
    }

    /* Кастомная полоска прогресса (имитация под референс) */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #8A2BE2, #FF007F) !important;
    }

    /* Изображения с мягким свечением */
    img {
        border-radius: 25px;
        border: 1px solid #2D2D44;
        box-shadow: 0 0 20px rgba(138, 43, 226, 0.2);
    }

    /* Скрываем стандартные элементы */
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Функциональная часть
with st.sidebar:
    st.markdown("### 🎛️ ПАНЕЛЬ УПРАВЛЕНИЯ")
    api_key = st.text_input("ВВОД КЛЮЧА:", type="password")
    
    st.divider()
    character = st.selectbox("СТИЛЬ УЧИТЕЛЯ:", ["Дружелюбный ИИ", "Кибер-Наставник", "Профессор"])
    voice_type = st.radio("ГОЛОС:", ["Женский", "Мужской"])
    
    st.markdown("---")
    st.markdown("🎯 Ваш прогресс обучения:")
    st.progress(65) # Статичный пример прогресса для красоты

def speak(text, voice):
    p = "1.2" if voice == "Женский" else "0.8"
    c_t = text.replace("'", "").replace('"', '').replace("\n", " ").replace("*", "")
    js = f"<script>var m=new SpeechSynthesisUtterance('{c_t}');m.lang='ru-RU';m.pitch={p};window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

st.title("SMART LESSON STUDIO")

if api_key:
    try:
        client = Groq(api_key=api_key)
        query = st.chat_input("Введите тему для мгновенного урока...")

        if query:
            with st.spinner("🧬 СИНТЕЗ ЗНАНИЙ..."):
                chat = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Ты — эксперт. Стиль: {character}. Объясни тему {query} кратко и с картинками."},

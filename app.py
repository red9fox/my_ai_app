import streamlit as st
from groq import Groq

# 1. Настройка страницы
st.set_page_config(page_title="AI Gamer Tutor", layout="wide", page_icon="🎮")

# 2. Боковая панель с палитрой
with st.sidebar:
    st.title("🕹️ Настройки UI")
    
    # ВЫБОР ЦВЕТОВ
    bg_color = st.color_picker("Цвет фона", "#000000")
    text_color = st.color_picker("Цвет текста и подсветки", "#ff5f00")
    
    st.divider()
    api_key = st.text_input("🔑 Вставь API Key:", type="password")
    character = st.selectbox("Твой Наставник:", ["Кибер-Мастер", "Друг-Геймер", "ИИ-Ассистент"])
    voice_type = st.radio("Голос:", ["Женский", "Мужской"])

# 3. Геймерский дизайн с динамическими цветами
st.markdown(f"""
    <style>
    /* Главный фон */
    .stApp {{
        background: {bg_color};
        color: {text_color};
        font-family: 'Segoe UI', sans-serif;
    }}
    
    /* Боковая панель */
    [data-testid="stSidebar"] {{
        background-color: {bg_color} !important;
        border-right: 1px solid {text_color}44;
    }}

    /* Стеклянные карточки сообщений */
    [data-testid="stChatMessage"] {{
        background: rgba(28, 28, 30, 0.6);
        border: 1px solid {text_color}66;
        border-radius: 24px;
        color: {text_color} !important;
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}

    /* Кнопки с динамическим цветом */
    .stButton>button {{
        border-radius: 16px;
        border: 2px solid {text_color};
        background: transparent;
        color: {text_color};
        font-weight: 700;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }}
    .stButton>button:hover {{
        background: {text_color};
        color: {bg_color};
        box-shadow: 0 0 20px {text_color}66;
    }}

    /* Заголовки */
    h1 {{
        color: {text_color};
        text-shadow: 0 0 15px {text_color}66;
        font-size: 3rem !important;
        font-weight: 900 !important;
        text-align: center;
    }}

    /* Поля ввода */
    .stChatInputContainer input {{
        background-color: rgba(28, 28, 30, 0.9) !important;
        border: 1px solid {text_color}44 !important;
        color: {text_color} !important;
    }}

    /* Текст в выпадающих списках и метках */
    label, p, .stSelectbox {{
        color: {text_color} !important;
    }}
    
    img {{
        border-radius: 24px;
        border: 1px solid {text_color}44;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Логика приложения
def speak(text_to_say, voice):
    pitch = "1.2" if voice == "Женский" else "0.8"
    clean_text = text_to_say.replace("'", "").replace('"', '').replace("\n", " ").replace("*", "")
    js = f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='ru-RU';m.pitch={pitch};window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

st.title("BRAIN LEVEL UP")

if api_key:
    try:
        client = Groq(api_key=api_key)
        query = st.chat_input("Введи тему для изучения...")

        if query:
            with st.spinner("💾 Синхронизация данных..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Ты — крутой учитель в стиле {character}. Объясни тему кратко, четко, используя геймерские аналогии."},
                        {"role": "user", "content": query}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                response = chat_completion.choices.message.content
                
                with st.chat_message("assistant"):
                    st.markdown(response)
                
                img_url = f"https://pollinations.ai{query.replace(' ','%20')}?width=1080&height=720&nologo=true"
                st.image(img_url)
                
                speak(response, voice_type)
                st.download_button("📥 Сохранить лог", response, file_name="lesson.txt")
    except Exception as e:
        st.error(f"Критическая ошибка: {e}")
else:
    st.info("👾 Подключи API Key в боковой панели, чтобы активировать систему.")

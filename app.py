import streamlit as st
from groq import Groq

# 1. Настройка страницы
st.set_page_config(page_title="Kimi Live", layout="wide", page_icon="🔵")

# 2. Боковая панель
with st.sidebar:
    st.title("⚙️ Настройки")
    api_key = st.text_input("Вставь Groq API Key:", type="password")
    
    st.divider()
    st.subheader("🎨 Твой стиль")
    bg_color = st.color_picker("Цвет фона", "#0A0A0A")
    accent_color = st.color_picker("Цвет блоков", "#1A1A1A")
    text_color = st.color_picker("Цвет текста", "#E5E5E5")
    
    st.divider()
    voice_on = st.toggle("Включить голос", value=True)

# 3. Дизайн с АНИМИРОВАННЫМ ассистентом
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');

    .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: 'Inter', sans-serif; }}

    /* --- АНИМАЦИЯ АССИСТЕНТА --- */
    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0px); }}
    }}
    
    @keyframes breathe {{
        0% {{ box-shadow: 0 0 15px rgba(91, 153, 255, 0.4); }}
        50% {{ box-shadow: 0 0 30px rgba(91, 153, 255, 0.8); }}
        100% {{ box-shadow: 0 0 15px rgba(91, 153, 255, 0.4); }}
    }}

    .kimi-avatar {{
        width: 55px; height: 55px;
        background: radial-gradient(circle at 30% 30%, #5B99FF, #2E5BFF);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        animation: float 4s ease-in-out infinite, breathe 3s infinite;
        margin-bottom: 25px;
    }}

    .kimi-eyes {{ color: white; font-weight: bold; font-size: 24px; letter-spacing: 2px; user-select: none; }}

    /* --- ОСТАЛЬНОЙ ДИЗАЙН --- */
    [data-testid="stChatMessage"] {{ background-color: transparent !important; color: {text_color} !important; }}
    
    .suggestion-chip {{
        background-color: {accent_color};
        border: 1px solid {text_color}22;
        border-radius: 12px;
        padding: 10px 15px;
        margin: 5px;
        font-size: 14px;
        color: {text_color}bb;
        display: inline-block;
    }}

    .stChatInputContainer input {{
        background-color: {accent_color} !important;
        border: 1px solid {text_color}22 !important;
        border-radius: 24px !important;
        color: {text_color} !important;
    }}

    header, footer {{visibility: hidden;}}
    </style>

    <div class="kimi-avatar">
        <div class="kimi-eyes">••</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Интерфейс
st.markdown(f"### Привет! Я твой живой ИИ-репетитор. \nНа какую тему создадим сегодня конспект?")

# 5. Логика работы
if api_key:
    try:
        client = Groq(api_key=api_key)
        query = st.chat_input("Спроси меня о чем угодно...")

        if query:
            with st.spinner(""):
                # ИСПРАВЛЕННЫЙ ЗАПРОС К ИИ
                chat = client.chat.completions.create(
                    messages=[{"role": "user", "content": query}],
                    model="llama-3.3-70b-versatile"
                )
                # ТУТ ДОБАВЛЕН ИНДЕКС [0]
                response = chat.choices[0].message.content
                
                with st.chat_message("assistant"):
                    st.markdown(response)
                
                # Картинка
                img_url = f"https://pollinations.ai{query.replace(' ','-')}?width=1024&height=576&nologo=true"
                st.image(img_url)

                if voice_on:
                    js_speak = f"<script>var m=new SpeechSynthesisUtterance('{response.replace(chr(39), '').replace(chr(34), '').replace(chr(10), ' ')}');m.lang='ru-RU';window.speechSynthesis.speak(m);</script>"
                    st.components.v1.html(js_speak, height=0)
    except Exception as e:
        st.error(f"Ошибка системы: {e}")
else:
    st.info("👋 Вставь свой ключ Groq в меню слева!")

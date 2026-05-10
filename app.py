import streamlit as st
from groq import Groq

# 1. Настройка страницы
st.set_page_config(page_title="AI Tutor Kimi", layout="wide", page_icon="🎓")

# 2. Боковая панель
with st.sidebar:
    st.title("⚙️ Настройки обучения")
    api_key = st.text_input("Groq API Key:", type="password")
    
    st.divider()
    level = st.select_slider("Уровень сложности:", options=["Детский", "Школьный", "Студент", "Профи"])
    voice_on = st.toggle("Озвучка урока", value=True)
    
    st.divider()
    st.subheader("🎨 Дизайн")
    bg_color = st.color_picker("Фон", "#0A0A0A")
    accent_color = st.color_picker("Элементы", "#1A1A1A")
    text_color = st.color_picker("Текст", "#FFFFFF")

# 3. Идеальный CSS (Центрирование и панель как у Kimi)
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');
    
    .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: 'Inter', sans-serif; }}

    /* Центрируем основной контейнер */
    .block-container {{
        max-width: 800px !important;
        padding-top: 2rem !important;
        margin: 0 auto !important;
    }}

    /* Анимированный Кими */
    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
    .kimi-avatar {{
        width: 50px; height: 50px; background: radial-gradient(circle at 30% 30%, #5B99FF, #2E5BFF);
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        animation: float 4s ease-in-out infinite; margin-bottom: 25px;
    }}
    .kimi-eyes {{ color: white; font-weight: bold; font-size: 22px; letter-spacing: 2px; }}

    /* Кнопки подсказок */
    .suggestion {{
        background: {accent_color}; border: 1px solid {text_color}11;
        border-radius: 12px; padding: 12px 20px; margin-bottom: 12px;
        color: {text_color}dd; font-size: 15px; cursor: pointer;
    }}

    /* Кнопки режимов над инпутом */
    .mode-container {{ display: flex; gap: 8px; margin-top: 40px; margin-bottom: 120px; flex-wrap: wrap; justify-content: center; }}
    .mode-pill {{
        background: {accent_color}; border: 1px solid {text_color}11;
        color: #A0A0A0; padding: 8px 16px; border-radius: 12px; font-size: 13px;
    }}

    /* ИСПРАВЛЕННАЯ ПАНЕЛЬ ВВОДА (Центрированная капсула) */
    [data-testid="stChatInput"] {{
        position: fixed !important; bottom: 30px !important;
        left: 50% !important; transform: translateX(-50%) !important;
        width: 90% !important; max-width: 700px !important;
        background-color: {accent_color} !important;
        border: 1px solid {text_color}22 !important;
        border-radius: 35px !important;
        z-index: 1000;
    }}
    [data-testid="stChatInput"] textarea {{ background-color: transparent !important; color: {text_color} !important; }}

    header, footer {{visibility: hidden;}}
    [data-testid="stSidebar"] {{ background-color: {bg_color} !important; border-right: 1px solid {text_color}11; }}
    </style>
    
    <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
        <div class="kimi-avatar"><div class="kimi-eyes">••</div></div>
        <h3 style="font-weight:400; margin-bottom:30px;">Привет! Давай изучим что-то новое сегодня.</h3>
    </div>
    """, unsafe_allow_html=True)

# 4. Логика ИИ-репетитора
if api_key:
    try:
        client = Groq(api_key=api_key)
        
        # Кнопки режимов для красоты
        st.markdown(f"""
        <div class="mode-container">
            <div class="mode-pill">🤖 Репетитор</div><div class="mode-pill">📊 Слайды</div>
            <div class="mode-pill">🔍 Исследование</div><div class="mode-pill">🪄 Тесты</div>
        </div>""", unsafe_allow_html=True)

        query = st.chat_input("Напиши тему урока (например: Как работают батарейки?)...")

        if query:
            with st.spinner("🧠 Подбираю материал..."):
                # Промпт для обучения
                prompt = f"""Ты — ИИ-учитель. Объясни тему '{query}' для уровня '{level}'.
                Ответ должен содержать: 
                1. 📖 Теорию. 
                2. 💡 Понятный пример. 
                3. ❓ Контрольный вопрос в конце."""
                
                chat = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": query}],
                    model="llama-3.3-70b-versatile"
                )
                res = chat.choices.message.content
                
                with st.chat_message("assistant"):
                    st.markdown(res)
                
                # Картинка-схема
                st.image(f"https://pollinations.ai{query.replace(' ','-')}?width=1000&height=500&nologo=true")
                
                if voice_on:
                    clean_res = res.replace("'", "").replace('"', '').replace("\n", " ")
                    st.components.v1.html(f"<script>var m=new SpeechSynthesisUtterance('{clean_res}');m.lang='ru-RU';window.speechSynthesis.speak(m);</script>", height=0)
                
                st.download_button("📥 Сохранить конспект", res, file_name=f"lesson_{query}.txt")
    except Exception as e:
        st.error(f"Ошибка: {e}")
else:
    st.info("👋 Чтобы начать учиться, вставь свой ключ в меню слева.")

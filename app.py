import streamlit as st
from groq import Groq

# 1. Настройка страницы
st.set_page_config(page_title="AI Tutor Studio", layout="wide", page_icon="🎓")

# 2. Боковая панель
with st.sidebar:
    st.title("⚙️ Настройки")
    ai_name = st.text_input("Имя твоего ИИ-учителя:", "ghost")
    api_key = st.text_input("Groq API Key:", type="password")
    
    st.divider()
    level = st.select_slider("Уровень сложности:", options=["Детский", "Школьный", "Студент", "Профи"])
    voice_on = st.toggle("Озвучка урока", value=True)
    
    st.divider()
    bg_color = st.color_picker("Фон", "#0A0A0A")
    accent_color = st.color_picker("Элементы", "#1A1A1A")
    text_color = st.color_picker("Текст", "#FFFFFF")

# 3. Дизайн и СТИЛИ КНОПОК
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');
    .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: 'Inter', sans-serif; }}
    .block-container {{ max-width: 800px; padding-top: 2rem; margin: 0 auto; }}

    /* Анимированный аватар */
    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
    .kimi-avatar {{
        width: 50px; height: 50px; background: radial-gradient(circle at 30% 30%, #5B99FF, #2E5BFF);
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        animation: float 4s ease-in-out infinite; margin: 0 auto 25px auto;
    }}
    .kimi-eyes {{ color: white; font-weight: bold; font-size: 22px; letter-spacing: 2px; }}

    /* Скрываем стандартные кнопки Streamlit, чтобы сделать свои */
    div.stButton > button {{
        background-color: {accent_color} !important;
        color: #A0A0A0 !important;
        border: 1px solid {text_color}11 !important;
        border-radius: 12px !important;
        font-size: 13px !important;
        padding: 8px 16px !important;
        transition: 0.3s !important;
    }}
    div.stButton > button:hover {{
        border-color: {text_color}44 !important;
        color: {text_color} !important;
    }}

    /* Панель ввода */
    [data-testid="stChatInput"] {{
        position: fixed !important; bottom: 30px !important;
        left: 50% !important; transform: translateX(-50%) !important;
        width: 90% !important; max-width: 700px !important;
        background-color: {accent_color} !important;
        border: 1px solid {text_color}22 !important;
        border-radius: 35px !important;
    }}

    header, footer {{visibility: hidden;}}
    </style>
    
    <div class="kimi-avatar"><div class="kimi-eyes">••</div></div>
    <h3 style="text-align: center; font-weight:400;">Привет! Я {ai_name}. Что изучим?</h3>
    """, unsafe_allow_html=True)

# Инициализируем сессию для хранения команд
if "mode_cmd" not in st.session_state:
    st.session_state.mode_cmd = ""

# 4. РАБОЧИЕ КНОПКИ (Элементы управления)
cols = st.columns([1,1,1,1])
with cols[0]:
    if st.button("🤖 Репетитор"):
        st.session_state.mode_cmd = "Объясни как репетитор тему: "
with cols[1]:
    if st.button("📊 Слайды"):
        st.session_state.mode_cmd = "Сделай краткий план-слайды по теме: "
with cols[2]:
    if st.button("🔍 Исследование"):
        st.session_state.mode_cmd = "Проведи глубокое исследование темы: "
with cols[3]:
    if st.button("🪄 Тесты"):
        st.session_state.mode_cmd = "Создай тест с вопросами по теме: "

# 5. Логика ИИ
if api_key:
    try:
        client = Groq(api_key=api_key)
        
        # Поле ввода (с подставленной командой, если нажата кнопка)
        query = st.chat_input(f"Напиши тему для {ai_name}...")

        # Если нажали кнопку или ввели текст
        actual_query = query
        if not query and st.session_state.mode_cmd:
            st.warning(f"Режим выбран! Теперь просто впиши тему в поле ниже.")
        
        if query:
            full_query = st.session_state.mode_cmd + query
            
            with st.spinner(f"{ai_name} обрабатывает запрос..."):
                prompt = f"Ты — ИИ-учитель {ai_name}. Твой уровень: {level}. Выполни запрос: {full_query}"
                
                chat = client.chat.completions.create(
                    messages=[{"role": "system", "content": prompt}, {"role": "user", "content": full_query}],
                    model="llama-3.3-70b-versatile"
                )
                res = chat.choices[0].message.content
                
                with st.chat_message("assistant"):
                    st.write(res)
                
                # Обнуляем режим после ответа
                st.session_state.mode_cmd = ""
                
                if voice_on:
                    clean_res = res.replace("'", "").replace('"', '').replace("\n", " ")
                    st.components.v1.html(f"<script>var m=new SpeechSynthesisUtterance('{clean_res}');m.lang='ru-RU';window.speechSynthesis.speak(m);</script>", height=0)
    except Exception as e:
        st.error(f"Ошибка: {e}")
else:
    st.info(f"👋 Чтобы начать, вставь свой ключ в меню слева.")

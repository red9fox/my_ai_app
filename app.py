import streamlit as st
from groq import Groq

# 1. Настройка страницы
st.set_page_config(page_title="Kimi K2.6", layout="wide", page_icon="🔵")

# 2. Боковая панель
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Groq API Key:", type="password")
    st.divider()
    bg_color = st.color_picker("Background", "#0A0A0A")
    accent_color = st.color_picker("Panels", "#1A1A1A")
    text_color = st.color_picker("Text", "#FFFFFF")
    voice_on = st.toggle("Voice Output", value=True)

# 3. Улучшенный дизайн
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');

    .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: 'Inter', sans-serif; }}

    /* КИМИ-ШАПКА */
    .kimi-header {{
        display: flex; justify-content: space-between; padding: 15px 5px;
        color: #888; font-size: 14px; border-bottom: 1px solid {text_color}11; margin-bottom: 40px;
    }}

    /* АНИМИРОВАННЫЙ КИМИ */
    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
    .kimi-avatar {{
        width: 50px; height: 50px; background: radial-gradient(circle at 30% 30%, #5B99FF, #2E5BFF);
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        animation: float 4s ease-in-out infinite; margin-bottom: 25px;
    }}
    .kimi-eyes {{ color: white; font-size: 22px; font-weight: bold; letter-spacing: 2px; }}

    /* ПОДСКАЗКИ */
    .suggestion {{
        background: {accent_color}; border: 1px solid {text_color}11;
        border-radius: 12px; padding: 12px 20px; margin-bottom: 12px;
        color: {text_color}dd; font-size: 15px; width: fit-content;
    }}

    /* ИСПРАВЛЕННАЯ ПАНЕЛЬ ВВОДА (Центрирование) */
    [data-testid="stChatInput"] {{
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 90% !important;
        max-width: 700px !important;
        background-color: {accent_color} !important;
        border: 1px solid {text_color}22 !important;
        border-radius: 35px !important;
        z-index: 1000;
    }}
    
    [data-testid="stChatInput"] textarea {{
        background-color: transparent !important;
        color: {text_color} !important;
        padding-left: 20px !important;
    }}

    /* КНОПКИ РЕЖИМОВ */
    .mode-container {{ display: flex; gap: 10px; margin-bottom: 100px; flex-wrap: wrap; }}
    .mode-pill {{
        background: {accent_color}; border: 1px solid {text_color}11;
        color: #A0A0A0; padding: 8px 16px; border-radius: 12px; font-size: 13px;
    }}

    header, footer {{visibility: hidden;}}
    [data-testid="stSidebar"] {{ background-color: {bg_color} !important; border-right: 1px solid {text_color}11; }}
    </style>

    <div class="kimi-header">
        <div>☰ &nbsp; Kimi &nbsp; <span style="color:#555">K2.6 Instant ></span></div>
        <div style="display:flex; gap:15px;"><span>🔊</span> <span>⊕</span></div>
    </div>

    <div class="kimi-avatar"><div class="kimi-eyes">••</div></div>
    """, unsafe_allow_html=True)

st.markdown("### Hi, Kimi sees images and videos now!")

st.markdown('<div class="suggestion">What powers Kimi K2.6?</div>', unsafe_allow_html=True)
st.markdown('<div class="suggestion">Create a 3D minimalist gallery</div>', unsafe_allow_html=True)

# 4. Логика чата
if api_key:
    try:
        client = Groq(api_key=api_key)
        
        st.markdown("""<div class="mode-container">
            <div class="mode-pill">🤖 Agent</div><div class="mode-pill">📊 Slides</div>
            <div class="mode-pill">📸 Kimi Claw</div><div class="mode-pill">✨ Agent Swarm</div>
        </div>""", unsafe_allow_html=True)

        query = st.chat_input("Ask away. Pics work too.")

        if query:
            with st.spinner(""):
                chat = client.chat.completions.create(
                    messages=[{"role": "user", "content": query}],
                    model="llama-3.3-70b-versatile"
                )
                res = chat.choices.message.content
                with st.chat_message("assistant"):
                    st.markdown(res)
                
                img_url = f"https://pollinations.ai{query.replace(' ','-')}?width=1024&height=576&nologo=true"
                st.image(img_url)
                
                if voice_on:
                    clean_res = res.replace("'", "").replace('"', '').replace("\n", " ")
                    st.components.v1.html(f"<script>var m=new SpeechSynthesisUtterance('{clean_res}');m.lang='ru-RU';window.speechSynthesis.speak(m);</script>", height=0)
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👋 Вставь свой ключ в меню слева.")

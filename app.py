import streamlit as st
from groq import Groq
import requests

# 1. Настройка страницы
st.set_page_config(page_title="Ghost Media Tutor", layout="wide", page_icon="🎬")

# Инициализация памяти
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Боковая панель (Загрузка файлов здесь!)
with st.sidebar:
    st.title("📁 Загрузка данных")
    uploaded_file = st.file_uploader("Загрузи документ (PDF, TXT)", type=["pdf", "txt"])
    api_key = st.text_input("Groq API Key:", type="password")
    
    st.divider()
    st.subheader("🎨 Настройки вывода")
    gen_image = st.checkbox("Генерировать фото к уроку", value=True)
    voice_on = st.toggle("Озвучка", value=True)

# 3. Дизайн в стиле Kimi
st.markdown("""
    <style>
    .stApp { background-color: #0A0A0A; color: #E5E5E5; }
    [data-testid="stChatInput"] { border-radius: 30px !important; background-color: #1A1A1A !important; }
    .stImage > img { border-radius: 20px; border: 1px solid #262626; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Ghost AI: Резюме и Медиа")

# 4. Обработка загруженного файла
file_context = ""
if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        file_context = str(uploaded_file.read(), "utf-8")
    else:
        file_context = "Тут должен быть текст из PDF (нужна библиотека PyPDF2)"
    st.success("Документ загружен! Теперь я могу сделать по нему резюме.")

# 5. Логика чата
if api_key:
    client = Groq(api_key=api_key)
    
    if prompt := st.chat_input("Напиши тему или нажми 'Сделай резюме файла'"):
        # Если есть файл, добавляем его в контекст
        user_input = prompt
        if file_context:
            user_input = f"Используй этот текст для ответа: {file_context[:2000]}. Запрос: {prompt}"

        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            # Запрос к ИИ
            chat = client.chat.completions.create(
                messages=[{"role": "system", "content": "Ты эксперт по резюме. Делай структурированные ответы. Если просят презентацию - пиши по пунктам."}] + st.session_state.messages,
                model="llama-3.3-70b-versatile"
            )
            response = chat.choices.message.content
            st.markdown(response)
            
            # --- ГЕНЕРАЦИЯ ФОТО ---
            if gen_image:
                st.subheader("🖼️ Визуализация:")
                img_url = f"https://pollinations.ai{prompt.replace(' ','-')}?width=1024&height=512&nologo=true"
                st.image(img_url)

            # --- ИМИТАЦИЯ ВИДЕО ---
            # На бесплатном уровне видео делать сложно, но мы можем дать ссылку на генератор
            st.info("🎥 Для создания видео из этого текста используй бесплатный сервис: [Luma Dream Machine](https://lumalabs.ai)")

            st.session_state.messages.append({"role": "assistant", "content": response})
            
            if voice_on:
                st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{response[:500].replace(chr(10), ' ')}'));</script>", height=0)

else:
    st.info("🔑 Вставь ключ API, чтобы активировать медиа-функции.")

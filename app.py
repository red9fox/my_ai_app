import streamlit as st
from groq import Groq

# 1. Настройка страницы и стилей
st.set_page_config(page_title="AI Super Tutor", layout="wide", page_icon="🚀")

# Боковая панель настроек
with st.sidebar:
    st.header("🎨 Настройки стиля")
    theme_choice = st.selectbox("Цветовая схема:", ["Стандартная", "Темная ночь", "Зеленый хакер", "Нежная пастель"])
    voice_type = st.radio("Голос учителя:", ["Женский", "Мужской"])
    character = st.selectbox("Кто тебя учит?", ["Друг-студент", "Строгий профессор", "Мастер Йода", "Киберпанк-гид"])
    
    st.divider()
    st.header("⚙️ Доступ")
    api_key = st.text_input("Вставь Groq API Key:", type="password", help="Начинается на gsk_")

# Применение выбранной темы через CSS
colors = {
    "Стандартная": ("#ffffff", "#000000", "#ff4b4b"),
    "Темная ночь": ("#0e1117", "#ffffff", "#262730"),
    "Зеленый хакер": ("#000000", "#00ff00", "#003300"),
    "Нежная пастель": ("#fff5f5", "#4a4a4a", "#ffc1c1")
}
bg, text, card = colors[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; }}
    .stButton>button {{ background-color: {card}; color: {text}; border: 1px solid {text}; border-radius: 15px; width: 100%; }}
    [data-testid="stChatMessage"] {{ background-color: {card}; color: {text}; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Твой Интерактивный Учитель")

# Функция озвучки (Web Speech API)
def speak(text_to_say, voice):
    pitch = "1.2" if voice == "Женский" else "0.8"
    # Очистка текста для корректной передачи в JS
    clean_text = text_to_say.replace("'", "").replace('"', '').replace("\n", " ").replace("*", "")
    js = f"""<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='ru-RU';m.pitch={pitch};window.speechSynthesis.speak(m);</script>"""
    st.components.v1.html(js, height=0)

# Основная логика
if api_key:
    try:
        client = Groq(api_key=api_key)
        
        query = st.chat_input("Напиши тему урока (например: Как работают черные дыры?)...")

        if query:
            with st.spinner("🧠 Учитель готовится к ответу..."):
                # Настройка личности персонажа
                system_prompt = f"Ты — уникальный учитель в роли: {character}. Твоя задача: максимально понятно и интересно объяснить тему пользователю. В конце обязательно задай один вовлекающий вопрос."
                
                # Запрос к нейросети (АКТУАЛЬНАЯ МОДЕЛЬ)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                
                response_text = chat_completion.choices.message.content
                
                # Вывод ответа в чат
                with st.chat_message("assistant"):
                    st.write(response_text)
                
                # Генерация образовательной картинки (Pollinations AI)
                st.divider()
                img_prompt = f"educational illustration about {query}, artistic style, high resolution"
                img_url = f"https://pollinations.ai{img_prompt.replace(' ','%20')}?width=800&height=500&nologo=true"
                st.image(img_url, caption=f"Визуализация темы: {query}")

                # Запуск озвучки
                speak(response_text, voice_type)
                
                # Кнопка скачивания конспекта
                st.download_button("💾 Скачать текст урока", response_text, file_name=f"lesson_{query[:10]}.txt")
                
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")
        st.info("Попробуй проверить API ключ или обновить страницу.")
else:
    st.warning("🤖 Привет! Чтобы я мог учить тебя, пожалуйста, вставь свой API Key от Groq в меню слева.")

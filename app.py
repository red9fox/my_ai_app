import streamlit as st
from groq import Groq

# Настройка страницы
st.set_page_config(page_title="AI Super Tutor", layout="wide", page_icon="🚀")

# Темы оформления (Кастомизация)
with st.sidebar:
    st.header("🎨 Настройки")
    theme_choice = st.selectbox("Цветовая схема:", ["Стандартная", "Темная ночь", "Зеленый хакер", "Нежная пастель"])
    voice_type = st.radio("Голос учителя:", ["Женский", "Мужской"])
    character = st.selectbox("Кто тебя учит?", ["Друг-студент", "Строгий профессор", "Мастер Йода", "Киберпанк-гид"])
    
    st.divider()
    st.header("⚙️ Доступ")
    api_key = st.text_input("Вставь Groq API Key:", type="password")
    st.info("Ключ начинается на gsk_")

# Применение CSS стилей
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
    .stButton>button {{ background-color: {card}; color: {text}; border-radius: 15px; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Твой Интерактивный Учитель")

# Функция озвучки
def speak(text_to_say, voice):
    pitch = "1.2" if voice == "Женский" else "0.8"
    clean_text = text_to_say.replace("'", "").replace('"', '').replace("\n", " ")
    js = f"""<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='ru-RU';m.pitch={pitch};window.speechSynthesis.speak(m);</script>"""
    st.components.v1.html(js, height=0)

if api_key:
    try:
        client = Groq(api_key=api_key)
        
        query = st.chat_input("Напиши тему урока...")

        if query:
            with st.spinner("Создаю контент..."):
                # Промпт для персонажа
                system_prompt = f"Ты в роли: {character}. Твоя задача понятно объяснить тему. В конце задай один вопрос."
                
                # Запрос к нейросети (исправленный формат)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}
                    ],
                    model="llama3-8b-8192",
                )
                
                response_text = chat_completion.choices[0].message.content
                
                # Отображение результата
                st.chat_message("assistant").write(response_text)
                
                # Генерация картинки
                img_url = f"https://pollinations.ai{query.replace(' ','%20')}?width=800&height=500&nologo=true"
                st.image(img_url, caption=f"Иллюстрация: {query}")

                # Запуск голоса
                speak(response_text, voice_type)
                
                st.download_button("💾 Сохранить урок", response_text, file_name="lesson.txt")
                
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")
        st.info("Проверь правильность API ключа или попробуй создать новый на сайте Groq.")
else:
    st.warning("⚠️ Пожалуйста, вставь API Key в меню слева, чтобы начать.")


import streamlit as st
from groq import Groq

# 1. Настройка страницы и кастомизация
st.set_page_config(page_title="AI Super Tutor", layout="wide", page_icon="🚀")

# Темы оформления
with st.sidebar:
    st.header("🎨 Настрой свой стиль")
    theme_choice = st.selectbox("Цветовая схема:", ["Стандартная", "Темная ночь", "Зеленый хакер", "Нежная пастель"])
    voice_type = st.radio("Голос учителя:", ["Женский", "Мужской"])
    character = st.selectbox("Кто тебя учит?", ["Друг-студент", "Строгий профессор", "Мастер Йода", "Киберпанк-гид"])
    
    st.divider()
    st.header("⚙️ Ключ доступа")
    api_key = st.text_input("Вставь Groq API Key:", type="password")

# CSS для кастомизации
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

if api_key:
    client = Groq(api_key=api_key)

    # Функция озвучки
    def speak(text, voice):
        pitch = "1.2" if voice == "Женский" else "0.8"
        clean_text = text.replace("'", "").replace('"', '').replace("\n", " ")
        js = f"""<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='ru-RU';m.pitch={pitch};window.speechSynthesis.speak(m);</script>"""
        st.components.v1.html(js, height=0)

    # Поле ввода
    query = st.chat_input("Какую тему сегодня разберем?")

    if query:
        with st.spinner("Создаю крутой урок..."):
            # Запрос к нейросети
            prompt = f"Ты в роли {character}. Понятно объясни тему: {query}. В конце добавь один вопрос для проверки."
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
            )
            ans = chat.choices.message.content
            
            # Текст и картинка
            st.chat_message("assistant").write(ans)
            
            img_url = f"https://pollinations.ai{query.replace(' ','%20')}?width=800&height=500&nologo=true"
            st.image(img_url, caption=f"Визуализация: {query}")

            # Озвучка
            speak(ans, voice_type)
            
            # Кнопка для сохранения
            st.download_button("💾 Сохранить конспект", ans, file_name="lesson.txt")
else:
    st.info("👋 Привет! Чтобы начать, вставь свой API ключ от Groq в меню слева. Учиться будет весело!")

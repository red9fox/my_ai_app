import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Super Tutor", layout="wide", page_icon="🚀")

with st.sidebar:
    st.header("🎨 Настройки стиля")
    theme_choice = st.selectbox("Цветовая схема:", ["Стандартная", "Темная ночь", "Зеленый хакер", "Нежная пастель"])
    voice_type = st.radio("Голос учителя:", ["Женский", "Мужской"])
    character = st.selectbox("Кто тебя учит?", ["Друг-студент", "Строгий профессор", "Мастер Йода", "Киберпанк-гид"])
    st.divider()
    api_key = st.text_input("Вставь Groq API Key:", type="password")

colors = {
    "Стандартная": ("#ffffff", "#000000", "#ff4b4b"),
    "Темная ночь": ("#0e1117", "#ffffff", "#262730"),
    "Зеленый хакер": ("#000000", "#00ff00", "#003300"),
    "Нежная пастель": ("#fff5f5", "#4a4a4a", "#ffc1c1")
}
bg, text, card = colors[theme_choice]
st.markdown(f"<style>.stApp {{ background-color: {bg}; color: {text}; }}</style>", unsafe_allow_html=True)

def speak(text_to_say, voice):
    pitch = "1.2" if voice == "Женский" else "0.8"
    clean_text = text_to_say.replace("'", "").replace('"', '').replace("\n", " ").replace("*", "")
    js = f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='ru-RU';m.pitch={pitch};window.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

st.title("🎓 Твой Интерактивный Учитель")

if api_key:
    try:
        client = Groq(api_key=api_key)
        query = st.chat_input("Напиши тему урока...")
        if query:
            with st.spinner("🧠 Учитель думает..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Ты в роли: {character}. Понятно объясни тему и задай вопрос в конце."},
                        {"role": "user", "content": query}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                # ИСПРАВЛЕННАЯ СТРОЧКА ТУТ:
                response_text = chat_completion.choices[0].message.content
                
                with st.chat_message("assistant"):
                    st.write(response_text)
                
                img_url = f"https://pollinations.ai{query.replace(' ','%20')}?width=800&height=500&nologo=true"
                st.image(img_url)
                speak(response_text, voice_type)
    except Exception as e:
        st.error(f"Ошибка: {e}")
else:
    st.info("🤖 Вставь API Key слева!")
         

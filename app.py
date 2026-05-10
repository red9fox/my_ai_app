import streamlit as st
from groq import Groq
import PyPDF2 # Теперь это будет работать

st.set_page_config(page_title="Ghost AI Studio", layout="wide", page_icon="🎓")

# 1. Боковая панель для загрузки
with st.sidebar:
    st.title("📁 Загрузка данных")
    uploaded_file = st.file_uploader("Загрузи документ (PDF, TXT)", type=["pdf", "txt"])
    api_key = st.text_input("Groq API Key:", type="password")
    st.divider()
    gen_image = st.checkbox("Генерировать фото", value=True)
    voice_on = st.toggle("Озвучка", value=True)

# 2. Дизайн Kimi
st.markdown("""<style>.stApp { background-color: #0A0A0A; color: #E5E5E5; }</style>""", unsafe_allow_html=True)
st.title("🎓 Ghost AI: Умный Репетитор")

# 3. Функция чтения PDF
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# 4. Обработка файла
context = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        context = read_pdf(uploaded_file)
    else:
        context = str(uploaded_file.read(), "utf-8")
    st.success("Документ прочитан! Можешь задавать вопросы по нему.")

# 5. Логика чата
if api_key:
    client = Groq(api_key=api_key)
    query = st.chat_input("Напиши тему или 'Сделай резюме файла'...")

    if query:
        with st.spinner("Думаю..."):
            # Формируем запрос с учетом файла
            full_prompt = f"Контекст из файла: {context[:3000]}\n\nЗапрос: {query}" if context else query
            
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": full_prompt}],
                model="llama-3.3-70b-versatile"
            )
            
            # ИСПРАВЛЕННАЯ СТРОЧКА (добавили индекс [0])
            response = chat.choices[0].message.content
            
            with st.chat_message("assistant"):
                st.write(response)
            
            if gen_image:
                img_url = f"https://pollinations.ai{query.replace(' ','-')}?width=800&height=400&nologo=true"
                st.image(img_url)

            if voice_on:
                js = f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{response[:500].replace(chr(10), ' ')}'));</script>"
                st.components.v1.html(js, height=0)
else:
    st.info("Вставь API Key слева!")

import streamlit as st
from groq import Groq
import PyPDF2

# 1. Настройка страницы
st.set_page_config(page_title="AI Study Studio", layout="wide", page_icon="🎓")

# 2. Боковая панель
with st.sidebar:
    st.title("📁 Загрузка данных")
    uploaded_file = st.file_uploader("Загрузи конспект (PDF, TXT)", type=["pdf", "txt"])
    api_key = st.text_input("Groq API Key:", type="password")
    st.divider()
    gen_image = st.checkbox("Генерировать фото", value=True)
    voice_on = st.toggle("Озвучка", value=True)

# 3. Функция для чтения PDF
def read_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        return f"Ошибка при чтении PDF: {e}"

# 4. Дизайн (Kimi Style)
st.markdown("""<style>.stApp { background-color: #0A0A0A; color: #E5E5E5; }</style>""", unsafe_allow_html=True)
st.title("🎓 Ghost AI: Умный Репетитор")

# 5. Обработка файла
file_context = ""
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        file_context = read_pdf(uploaded_file)
    else:
        file_context = str(uploaded_file.read(), "utf-8")
    
    if "Ошибка" not in file_context:
        st.success("✅ Документ успешно загружен и прочитан!")
    else:
        st.error(file_context)

# 6. Логика чата
if api_key:
    client = Groq(api_key=api_key)
    query = st.chat_input("Спроси что-нибудь по файлу или просто тему...")

    if query:
        with st.spinner("🧠 Анализирую..."):
            # Формируем запрос
            prompt_content = f"Используй этот текст: {file_context[:5000]}\n\nВопрос: {query}" if file_context else query
            
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_content}],
                model="llama-3.3-70b-versatile"
            )
            response = chat.choices[0].message.content
            
            with st.chat_message("assistant"):
                st.markdown(response)
            
            if gen_image:
                img_url = f"https://pollinations.ai{query.replace(' ','-')}?width=800&height=400&nologo=true"
                st.image(img_url)

            if voice_on:
                clean_voice = response[:500].replace("'", "").replace('"', '').replace("\n", " ")
                st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{clean_voice}'));</script>", height=0)
else:
    st.info("👋 Вставь ключ API в меню слева, чтобы начать.")

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import pdfplumber
import os
from dotenv import load_dotenv
import zipfile

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY missing in .env")
    st.stop()

os.environ["GOOGLE_API_KEY"] = API_KEY

st.set_page_config(
    page_title="Resume → AI Portfolio Website",
    page_icon="🌐",
    layout="wide"
)

# ---------------- UI HEADER ----------------
st.markdown("""
<h1 style="text-align:center;">🌐 Resume → AI Portfolio Website</h1>
<p style="text-align:center;color:#9ca3af;">
Upload your resume and instantly generate a professional dark-themed portfolio website
</p>
""", unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📄 Upload your Resume (PDF only)",
    type=["pdf"]
)

def extract_resume_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text.strip()

# ---------------- GENERATE ----------------
if uploaded_file:
    if st.button("🚀 Generate Portfolio Website", use_container_width=True):

        with st.spinner("Analyzing resume & generating website..."):

            resume_text = extract_resume_text(uploaded_file)

            prompt = f"""
You are a professional frontend web developer.

Create a PERSONAL PORTFOLIO WEBSITE using the resume below.

STRICT RULES:
1. HTML MUST link styles.css using <link rel="stylesheet" href="styles.css">
2. HTML MUST link script.js before </body>
3. Dark, modern UI (black/gray tones)
4. Skills MUST use visual progress bars
5. Projects MUST be displayed as cards
6. Header + Footer required
7. Frontend only (HTML, CSS, JS)
8. Clean, professional typography

Resume Content:
{resume_text}

FORMAT STRICTLY AS:

--html--
HTML CODE
--html--

--css--
CSS CODE
--css--

--javascript--
JAVASCRIPT CODE
--javascript--
"""

            model = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.7
            )

            response = model.invoke(prompt)
            content = response.content

            # ---------------- PARSE OUTPUT ----------------
            try:
                html = content.split("--html--")[1].split("--html--")[0].strip()
                css = content.split("--css--")[1].split("--css--")[0].strip()
                js = content.split("--javascript--")[1].split("--javascript--")[0].strip()
            except:
                st.error("❌ AI response format incorrect. Try again.")
                st.stop()

            # ---------------- SAVE FILES ----------------
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(html)

            with open("styles.css", "w", encoding="utf-8") as f:
                f.write(css)

            with open("script.js", "w", encoding="utf-8") as f:
                f.write(js)

            # ---------------- ZIP ----------------
            with zipfile.ZipFile("portfolio_website.zip", "w") as zipf:
                zipf.write("index.html")
                zipf.write("styles.css")
                zipf.write("script.js")

        # ---------------- TABS ----------------
        tab1, tab2, tab3 = st.tabs(["🌐 Live Preview", "📄 Code", "⬇️ Download"])

        # -------- LIVE PREVIEW (INLINE FIX) --------
        with tab1:
            body = html.split("<body>")[1].split("</body>")[0]

            preview_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                {css}
                </style>
            </head>
            <body>
                {body}
                <script>
                {js}
                </script>
            </body>
            </html>
            """

            st.components.v1.html(preview_html, height=700, scrolling=True)

        # -------- CODE VIEW --------
        with tab2:
            st.subheader("📄 index.html")
            st.code(html, language="html")

            st.subheader("🎨 styles.css")
            st.code(css, language="css")

            st.subheader("⚙️ script.js")
            st.code(js, language="javascript")

        # -------- DOWNLOAD --------
        with tab3:
            with open("portfolio_website.zip", "rb") as f:
                st.download_button(
                    "⬇️ Download Website Code (ZIP)",
                    f,
                    file_name="portfolio_website.zip",
                    mime="application/zip",
                    use_container_width=True
                )

        st.success("✅ Portfolio Website Generated Successfully!")

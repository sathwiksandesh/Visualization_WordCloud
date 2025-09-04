import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
import docx
from collections import Counter
from io import BytesIO

# -------------------------
# Extract text from PDF
# -------------------------
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# -------------------------
# Extract text from DOCX
# -------------------------
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = " ".join([para.text for para in doc.paragraphs])
    return text

# -------------------------
# Generate Word Cloud
# -------------------------
def generate_wordcloud(text):
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        stopwords=set(STOPWORDS),
        colormap="viridis"
    ).generate(text)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig, wordcloud

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Word Cloud Generator", layout="wide")
st.title("📊 Word Cloud Generator (PDF & Word)")

uploaded_file = st.file_uploader("Upload a PDF or Word (.docx) file", type=["pdf", "docx"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        text_data = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text_data = extract_text_from_docx(uploaded_file)
    else:
        text_data = ""

    if text_data.strip():
        # Generate word cloud
        fig, wordcloud = generate_wordcloud(text_data)

        # Show in Streamlit
        st.subheader("Generated Word Cloud")
        st.pyplot(fig)

        # -------------------------
        # Add Download Button
        # -------------------------
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="📥 Download Word Cloud as PNG",
            data=buf.getvalue(),
            file_name="wordcloud.png",
            mime="image/png"
        )

        # -------------------------
        # Show Top Frequent Words
        # -------------------------
        st.subheader("🔝 Top 10 Frequent Words")
        words = text_data.split()
        word_counts = Counter(words)
        top_words = word_counts.most_common(10)

        st.table(top_words)

    else:
        st.warning("⚠️ No text could be extracted from this file.")

st.info("Upload a PDF or DOCX file to visualize its Word Cloud, download it, and see top words.")

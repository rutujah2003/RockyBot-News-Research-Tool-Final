# 🪨 RockyBot: News Research Tool

RockyBot is an end-to-end LLM-based web application designed for efficient and user-friendly financial news analysis. Users can input article URLs and ask questions to retrieve insightful and contextually relevant answers with proper citations. It is tailored for the stock market and financial domain enthusiasts, researchers, and analysts.

---

## 🚀 Features

- 🔗 **URL-Based Research**: Paste article URLs and extract key content using `UnstructuredURLLoader`.
- 🧠 **LLM-Powered QA**: Ask questions about the article and get intelligent answers powered by large language models.
- 📚 **Citation-Supported Responses**: Responses are sourced with citations for reliability and traceability.
- 📊 **Financial Focus**: Optimized for financial and stock market-related articles.
- 🧭 **Contextual Retrieval**: Uses vector embeddings (FAISS) to ensure responses are grounded in uploaded content.
- 🎨 **Interactive UI**: Built using Streamlit for an intuitive user experience.

---

## 🛠️ Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Backend**: Python
- **LLM Integration**: LangChain + FireworksAI / OpenAI
- **Embeddings**: HuggingFace or OpenAI Embeddings
- **Vector Store**: FAISS
- **Loader**: UnstructuredURLLoader from LangChain

---

## 📦 Installation

```bash
git clone https://github.com/your-username/rockybot-news-research.git
cd rockybot-news-research
pip install -r requirements.txt

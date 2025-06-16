import os
import pickle
import time
import streamlit as st
from dotenv import load_dotenv
import langchain
from langchain_fireworks import ChatFireworks
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()
llm = ChatFireworks(
    model="accounts/fireworks/models/llama4-scout-instruct-basic",
    api_key=os.getenv("FIREWORKS_API_KEY"),
)

# 🔧 App UI
st.title("📰 News Research Tool")
st.sidebar.title("Paste News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    if url:
        urls.append(url)

process_url_clicked = st.sidebar.button("🔄 Process URLs")
file_path = "vector_index.pkl"
main_place_holder = st.empty()

# 🔍 Handle URL content and vectorization
if process_url_clicked:
    try:
        loader = WebBaseLoader(urls)
        main_place_holder.text("🔄 Loading URLs...")
        data = loader.load()

        # ✅ DEBUG: Check raw content
        for i, doc in enumerate(data):
            print(f"\n🔹 Page {i+1} Content (Preview):\n{doc.page_content[:500]}")

        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', ' '],
            chunk_size=1500,
            chunk_overlap=300
        )
        docs = text_splitter.split_documents(data)
        main_place_holder.text("✂️ Splitting text...")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={"device": "cpu"}
        )
        vector = FAISS.from_documents(docs, embeddings)
        main_place_holder.text("📦 Building vector index...")

        with open(file_path, "wb") as f:
            pickle.dump(vector, f)
        main_place_holder.success("✅ URLs processed successfully..")
    except Exception as e:
        st.error(f"Error while processing: {e}")

# 🤖 Ask a question
query = main_place_holder.text_input("🔎 Ask a question:")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vector_index = pickle.load(f)

        # 🔍 Check top results
        matches = vector_index.similarity_search(query, k=5)
        if matches:
            retriever = vector_index.as_retriever()
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=retriever)
            result = chain({"question": query}, return_only_outputs=True)
            st.header("Answer")
            st.subheader(result.get("answer", "No answer found."))

            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                for source in sources.split("\n"):
                    st.write(source)
        else:
            st.warning("⚠️ No relevant info found in the articles. Falling back to LLM.")
            response = llm.invoke(query)
            st.header("LLM Answer (Fallback)")
            st.write(response)
    else:
        st.error("❌ Vector file not found. Please process URLs first.")

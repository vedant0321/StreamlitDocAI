import os
import streamlit as st
import pickle
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import google.generativeai as genai

def show_AI_Bot():
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        st.error("Google API key is not set. Please set the GOOGLE_API_KEY environment variable in the .env file.")
        return
    
    genai.configure(api_key=google_api_key)

    st.header("Chat with PDF AI Bot 💭")
    pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if pdf is not None:
        try:
            pdf_reader = PdfReader(pdf)
            st.write("PDF file uploaded successfully")
            
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text=text)
            
            store_name = pdf.name[:-4]
            st.write(f'{store_name}')
            
            if os.path.exists(f"{store_name}.pkl"):
                with open(f"{store_name}.pkl", "rb") as f:
                    vectorstore = pickle.load(f)
                st.write('Embeddings loaded from disk')
            else:
                try:
                    embeddings = HuggingFaceEmbeddings()
                    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
                    with open(f"{store_name}.pkl", "wb") as f:
                        pickle.dump(vectorstore, f)
                    st.write('Embeddings created and saved to disk')
                except Exception as e:
                    st.error(f"Error creating embeddings: {str(e)}")
                    return
            
            query = st.text_input("Ask questions about your PDF file:")
            
            if query:
                try:
                    docs = vectorstore.similarity_search(query=query, k=3)
                    context = "\n".join([doc.page_content for doc in docs])
                    
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(f"Context: {context}\n\nQuestion: {query}\n\nAnswer:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {str(e)}")
    else:
        st.write("Please upload a PDF file")

# This is the entry point of the Streamlit app
if __name__ == "__main__":
    show_AI_Bot()
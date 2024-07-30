import os
import streamlit as st
import pickle
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter  # for splitting text into chunks 
from langchain.embeddings import OpenAIEmbeddings  
from langchain.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks.manager import get_openai_callback
from openai import OpenAIError

def show_AI_Bot():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable in the .env file.")
        return
    
    st.header("Chat with PDF AI Bot 💭")
    pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if pdf is not None:
        try:
            pdf_reader = PdfReader(pdf)
            st.write("PDF file uploaded successfully")
            
            # for extraction of text from pdf page wise 
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            # st.write(text)  # SHOWING THE TEXT 
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,  # for splitting text into chunks of 1000 characters
                chunk_overlap=200,  # for overlapping text as some text may have connection with previous text
                length_function=len
            )
            chunks = text_splitter.split_text(text=text)
            # st.write(chunks)
            
            # Embeddings
            store_name = pdf.name[:-4]
            st.write(f'{store_name}')
            
            if os.path.exists(f"{store_name}.pkl"):
                with open(f"{store_name}.pkl", "rb") as f:
                    vectorstore = pickle.load(f)
                st.write('Embeddings loaded from disk')
            else:
                try:
                    embeddings = OpenAIEmbeddings()
                    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
                    with open(f"{store_name}.pkl", "wb") as f:
                        pickle.dump(vectorstore, f)
                    st.write('Embeddings created and saved to disk')
                except OpenAIError as e:
                    st.error(f"Error creating embeddings: {str(e)}")
                    return
            
            # Accept user questions/query
            query = st.text_input("Ask questions about your PDF file:")
            # st.write(query)
            
            if query:
                try:
                    docs = vectorstore.similarity_search(query=query, k=3)
                    
                    llm = OpenAI(api_key=openai_api_key)
                    chain = load_qa_chain(llm=llm, chain_type="stuff")
                    with get_openai_callback() as cb:
                        response = chain.run(input_documents=docs, question=query)
                        print(cb)
                    st.write(response)
                except OpenAIError as e:
                    st.error(f"Error processing query: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {str(e)}")
    else:
        st.write("Please upload a PDF file")

if __name__ == "__main__":
    show_AI_Bot()

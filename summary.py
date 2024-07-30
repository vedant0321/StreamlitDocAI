import os
import streamlit as st
import pickle
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.chains.summarization import load_summarization_chain
from langchain_community.callbacks.manager import get_openai_callback
from openai import OpenAIError

def summary(pdf_text):
    """
    Summarizes the given PDF text using an OpenAI model.
    
    Parameters:
        pdf_text (str): The extracted text from the PDF document.
    """
    # Load environment variables (e.g., API key) from .env file
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        st.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable in the .env file.")
        return

    try:
        # Create a text splitter to break the PDF text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Size of each text chunk
            chunk_overlap=200,  # Overlap between chunks
            length_function=len  # Function to calculate text length
        )
        chunks = text_splitter.split_text(text=pdf_text)
        
        # Create or load embeddings and vectorstore
        store_name = "pdf_summary_store"
        if os.path.exists(f"{store_name}.pkl"):
            # Load existing vectorstore from file
            with open(f"{store_name}.pkl", "rb") as f:
                vectorstore = pickle.load(f)
        else:
            # Create embeddings and vectorstore if not already present
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(vectorstore, f)
        
        # Create an OpenAI instance for summarization
        llm = OpenAI(api_key=openai_api_key)
        chain = load_summarization_chain(llm=llm, chain_type="stuff")
        
        # Run the summarization chain to get the summary
        with get_openai_callback() as cb:
            summary = chain.run(input_documents=chunks)
            st.write(summary)
            st.write("Callback info:", cb)
    
    except OpenAIError as e:
        # Handle errors related to the OpenAI API
        st.error(f"Error creating summary: {str(e)}")
    except Exception as e:
        # Handle other errors
        st.error(f"An error occurred: {str(e)}")

def main():
    """
    Main function to create the Streamlit app interface for summarizing PDFs.
    """
    st.title("PDF Summary Generator 📄✍️")

    # File uploader widget for PDF files
    pdf_file = st.file_uploader("Upload your PDF file", type="pdf")

    if pdf_file:
        try:
            # Read the uploaded PDF file
            pdf_reader = PdfReader(pdf_file)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
            
            if pdf_text:
                st.write("PDF text extracted successfully. Generating summary...")
                summarize_pdf(pdf_text)
            else:
                st.error("No text extracted from the PDF.")
        
        except Exception as e:
            # Handle errors related to PDF processing
            st.error(f"An error occurred while processing the PDF: {str(e)}")

if __name__ == "__main__":
    main()

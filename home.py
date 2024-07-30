import streamlit as st

def show_home():
    st.markdown('''
    # Document AI Bot 💬📄

    ## Transform Your PDF Experience with AI

    Welcome to the **Document AI Bot**, your smart assistant for interacting with and extracting valuable insights from PDF documents. Whether you're dealing with research papers, business reports, or any other type of PDF, our AI-powered tool helps you easily navigate and understand your documents through natural language queries.

    ## How It Works

    1. **Upload Your PDF**: Simply drag and drop your PDF file into the upload area. Our tool supports a wide range of PDF formats.
       
    2. **AI-Driven Text Analysis**: Once uploaded, the AI reads and processes your document, breaking it down into manageable chunks and creating embeddings for efficient querying.

    3. **Ask Questions**: Type in your questions about the content of the PDF. Our AI will analyze the context and provide relevant answers, helping you quickly find the information you need.

    4. **Get Instant Answers**: Receive accurate and contextually relevant responses from the AI, powered by state-of-the-art language models. No more sifting through pages of text!

    ## Features

    - **Easy PDF Upload**: Quickly upload your PDF files with a user-friendly interface.
    - **Powerful Text Extraction**: Our tool extracts text from your PDF and processes it for efficient querying.
    - **Natural Language Queries**: Ask questions in plain language and get clear, precise answers.
    - **Efficient Document Search**: The AI performs similarity searches to ensure you get the most relevant information.
    - **User-Friendly Interface**: Built with Streamlit, our app is intuitive and easy to navigate.

    ## Getting Started

    1. **Upload a PDF**: Click on the "Upload a PDF file" button to add your document.
    2. **Ask Your Questions**: Enter your queries in the text input box and hit "Enter."
    3. **Review the Answers**: Read the AI-generated responses and find the information you need.

   
    ''')

if __name__ == "__main__":
    show_home()

# Document AI Bot 💬📄

## Overview

The **Document AI Bot** is a powerful tool designed to interact with PDF documents using advanced AI. By leveraging state-of-the-art language models, the bot extracts text, analyzes content, and provides relevant answers to user queries about the PDF documents.

## Features

- **Easy PDF Upload**: Seamlessly upload PDF files through a user-friendly interface.
- **AI-Driven Text Analysis**: Extract and process text from PDFs to enable efficient querying.
- **Natural Language Queries**: Ask questions in plain language and receive contextually relevant answers.
- **Efficient Document Search**: Perform similarity searches to retrieve the most pertinent information.
- **User-Friendly Interface**: Built with Streamlit for an intuitive and easy-to-navigate application.
- **Genrate summary**: Generate summaries of the extracted text.



## How It Works

1. **Upload Your PDF**: Drag and drop your PDF file into the upload area.
2. **AI-Driven Text Analysis**: The bot reads and processes the document, creating embeddings for querying.
3. **Ask Questions**: Enter your questions about the PDF content.
4. **Receive Answers**: Get accurate and relevant responses from the AI.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/document-ai-bot.git
   cd document-ai-bot
   ```
2. Create a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install the required packages:
```
pip install -r requirements.txt
```
4. Create a .env file in the project directory with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here 

```
5. Run the Streamlit app:
```
streamlit run app.py
```
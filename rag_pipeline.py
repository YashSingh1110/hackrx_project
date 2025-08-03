# rag_pipeline.py

import os
import requests
import io
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# IMPORTANT: Use the name of the NEW index you created with dimension 384
PINECONE_INDEX_NAME = "hackrx-free" # Or whatever you named your new index


def get_answers_from_documents(doc_url: str, questions: list) -> list:
    print("🚀 Starting the FREE RAG pipeline...")
    
    try:
        # 1. Download & Extract Text
        print("⬇️ Downloading and extracting text...")
        response = requests.get(doc_url)
        response.raise_for_status()
        pdf_file = io.BytesIO(response.content)
        reader = PdfReader(pdf_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        # 2. Chunk the text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len
        )
        chunks = text_splitter.split_text(full_text)
        print(f"✅ Split document into {len(chunks)} chunks.")
        
        # 3. Create Local Embeddings and Store in Pinecone
        # This uses a free model that runs on your computer
        print(" Creating local embeddings...")
        embeddings_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        print(" uploading embeddings to Pinecone...")
        vectorstore = PineconeVectorStore.from_texts(
            texts=chunks, 
            embedding=embeddings_model, 
            index_name=PINECONE_INDEX_NAME
        )
        print("✅ Document stored in Pinecone.")

        # 4. Initialize the Google Gemini LLM and the Retrieval-QA Chain
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )

        # 5. Ask Questions and Collect Answers
        print("❓ Answering questions with Gemini...")
        answers = []
        for question in questions:
            print(f" -> Processing: {question}")
            try:
                result = qa_chain.invoke({"query": question})
                answers.append(result["result"])
            except Exception as e:
                print(f"Error answering question '{question}': {e}")
                answers.append("Could not retrieve an answer.")
                
        print("✅ All questions processed.")
        return answers

    except Exception as e:
        print(f"❌ An error occurred in the pipeline: {e}")
        return [f"Error processing document: {e}" for q in questions]
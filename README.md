# HackRx 6.0: LLM-Powered Document Q&A System

This project is an intelligent query-retrieval system built for the HackRx 6.0 hackathon. It leverages a Retrieval-Augmented Generation (RAG) pipeline to process documents, understand natural language questions, and provide context-aware answers.

The application is built as a RESTful API using FastAPI and can be deployed as a standalone web service.

## ✨ Features

-   **Document Processing**: Ingests and processes PDF documents from a public URL.
-   **Q&A Capabilities**: Answers natural language questions based on the content of the provided document.
-   **RAG Architecture**: Uses a modern RAG pipeline for accurate, context-aware responses.
-   **RESTful API**: Exposes a simple `POST /hackrx/run` endpoint for easy integration.
-   **Cost-Effective Stack**: Built entirely on free-tier services, including Google Gemini and Hugging Face embeddings.

## 🛠️ Tech Stack

-   **Backend Framework**: **FastAPI**
-   **Vector Database**: **Pinecone**
-   **LLM (Language Model)**: **Google Gemini** (`gemini-1.5-flash-latest`)
-   **Embeddings Model**: **Hugging Face Sentence Transformers** (`all-MiniLM-L6-v2`)
-   **Core Libraries**: **LangChain**, **Pydantic**, **Uvicorn**

## ⚙️ System Architecture & Workflow

The system follows a standard Retrieval-Augmented Generation (RAG) workflow:

1.  **Ingestion**: The API receives a `POST` request with a document URL and a list of questions.
2.  **Document Loading**: The PDF document is downloaded from the URL and its text is extracted.
3.  **Chunking**: The extracted text is split into smaller, overlapping chunks to ensure semantic context is preserved.
4.  **Embedding**: A local Hugging Face model converts each text chunk into a 384-dimension vector embedding.
5.  **Indexing**: The text chunks and their corresponding embeddings are uploaded to a Pinecone index for efficient similarity searching.
6.  **Retrieval**: For each question, the system searches the Pinecone index for the most relevant text chunks.
7.  **Generation**: The retrieved chunks are passed as context—along with the original question—to the Google Gemini LLM, which generates the final answer.
8.  **Response**: The generated answers are collected and returned as a JSON response.

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

-   Python 3.9+
-   A Google AI API Key
-   A Pinecone API Key and a pre-configured index

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

### 2. Create and Activate a Virtual Environment

```powershell
# Create the environment
python -m venv venv

# Activate it (on Windows PowerShell)
.\venv\Scripts\activate

# On Mac/Linux:
# source venv/bin/activate
```

### 3. Create a `requirements.txt` File

Before installing, make sure you have a `requirements.txt` file. You can generate one from your working environment with this command:

```powershell
pip freeze > requirements.txt
```

### 4. Install Dependencies

Install all the required Python libraries from the `requirements.txt` file.

```powershell
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a file named `.env` in the root of the project folder and add your API keys.

> **Note**: Do not commit your `.env` file to GitHub. Create a `.env.example` file to show the required variables.

**`.env` file contents:**
```
# Key from Google AI Studio
GOOGLE_API_KEY="your_google_api_key_here"

# Key from your Pinecone dashboard
PINECONE_API_KEY="your_pinecone_api_key_here"
```

### 6. Run the Application

Use Uvicorn to run the FastAPI server. The `--reload` flag will automatically restart the server when you make code changes.

```powershell
python -m uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## 📖 API Usage

To use the API, send a `POST` request to the `/hackrx/run` endpoint.

-   **URL**: `http://127.0.0.1:8000/hackrx/run`
-   **Method**: `POST`
-   **Body**: `raw` (JSON)

#### Sample Request Body:

```json
{
    "documents": "[https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D](https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D)",
    "questions": [
        "What is the grace period for premium payment?",
        "Does this policy cover maternity expenses, and what are the conditions?"
    ]
}
```

#### Sample Success Response:

```json
{
    "answers": [
        "The grace period for premium payment is 30 days.",
        "Yes, the policy covers maternity expenses after a waiting period of 24 months, with a limit of two deliveries."
    ]
}
```

## 🔮 Future Improvements

-   **Support for More Document Types**: Add text extraction logic for `.docx` (using `python-docx`) and email files (`.eml`, `.msg`).
-   **Enhance Explainability**: Modify the API response to include the source text chunks used to generate each answer, fulfilling the "clause traceability" requirement.
-   **Asynchronous Processing**: Implement asynchronous handling of document processing and LLM calls to improve performance and prevent blocking.

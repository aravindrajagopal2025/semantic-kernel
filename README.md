# nirvana-agentic-orchestrator

A FastAPI + Semantic Kernel + Azure OpenAI microservice

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4-orange.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

## 📋 What's Included?

| **Module**                    | **What it does**                                         |
|-------------------------------|----------------------------------------------------------|
| `summary_agent`               | Summarizes lengthy input text into 2–3 clear sentences  |

## 🔗 API Endpoints

### Summarize Text
Transforms long text into concise, readable summaries.

```http
POST /summarize/
```

**Request Body:**
```json
{
  "text": "Your long text content here..."
}
```

**Response:**
```json
{
  "summary": "Concise 2-3 sentence summary of the input text."
}
```

**Example:**
```bash
curl -X POST "http://localhost:8084/summarize/" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your very long article or document text here..."}'
```

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```ini
azure_openai_key=a3a4cff3a5c745de851ac3c22274bcf8
azure_openai_endpoint=https://mt-openai-nonprod-eastus2.openai.azure.com/
azure_openai_model=mckopenai-gpt41-2025-04-14-preview
azure_openai_api_version=2024-06-01
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.13 or higher
- Poetry (for dependency management)
- Azure OpenAI service access

### 1️⃣ Clone the Repository
```bash
git clone <repository-url>
cd semantic-kernel
```

### 2️⃣ Install Dependencies
```bash
poetry install
```

### 3️⃣ Configure Environment
```bash
cp sample_env.txt .env
# Edit .env with your Azure OpenAI credentials
```

### 4️⃣ Start the Server
```bash
poetry run uvicorn app.main:app --reload --port 8084
```

The API will be available at:
- **API Base**: http://localhost:8084
- **Interactive Docs**: http://localhost:8084/docs
- **OpenAPI Schema**: http://localhost:8084/openapi.json

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Microsoft Semantic Kernel](https://github.com/microsoft/semantic-kernel)
- AI capabilities provided by [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

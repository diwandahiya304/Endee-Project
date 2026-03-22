\# 📄 DocQA — Document Question Answering using Endee



> Upload any PDF and ask questions about it in natural language.

> Powered by Endee vector database, sentence-transformers, and Llama3 via Groq.



\---



\## Problem Statement

Reading long documents to find specific information is time-consuming.

This project lets users upload any PDF and instantly ask questions about

it in natural language, getting accurate answers grounded in the document.



\---



\## System Design

```

User → Streamlit UI → PDF Processor → Embedder → Endee Vector DB

&#x20;                   ↘ Question Encoder → Endee Search → LLM → Answer

```

1\. PDF is extracted and split into 500-character overlapping chunks

2\. Each chunk is converted to a vector using sentence-transformers

3\. Vectors and original text are stored in Endee vector DB

4\. User question is also embedded into a vector

5\. Endee finds the 5 most semantically similar chunks

6\. Llama3 via Groq generates a grounded answer from those chunks



\---



\## How Endee Is Used

Endee serves as the vector database backbone of this project.

\- An index with 384 dimensions and cosine similarity is created in Endee

\- Document chunk embeddings are stored via `index.upsert()`

\- At query time, `index.query()` retrieves the top-k most similar chunks

\- Endee enables fast and accurate semantic search over document content



\---



\## Tech Stack

| Component | Technology |

|---|---|

| Vector Database | Endee (via Docker) |

| Embeddings | paraphrase-MiniLM-L3-v2 |

| LLM | Llama3 via Groq API |

| UI | Streamlit |

| PDF Parsing | PyPDF2 |



\---



\## Setup and Run



\### Prerequisites

\- Python 3.10+

\- Docker Desktop



\### Steps



1\. Clone this repository

```bash

&#x20;  git clone https://github.com/YOUR\_USERNAME/doc-qa-endee

&#x20;  cd doc-qa-endee

```



2\. Start Endee vector database

```bash

&#x20;  docker compose up -d

```



3\. Install dependencies

```bash

&#x20;  pip install -r requirements.txt

```



4\. Add your Groq API key — create a `.env` file:

```

&#x20;  GROQ\_API\_KEY=your\_key\_here

```



5\. Run the app

```bash

&#x20;  python -m streamlit run app.py

```



6\. Open http://localhost:8501 in your browser



\---



\## Demo

\- Upload any PDF document

\- Click Process Document

\- Ask any question about the document

\- Get accurate AI-powered answers with source passages


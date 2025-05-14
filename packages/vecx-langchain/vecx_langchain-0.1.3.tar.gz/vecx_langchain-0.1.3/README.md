# VectorX LangChain Integration

This package provides an integration between [VectorX](https://vectorxdb.ai) (an encrypted vector database) and [LangChain](https://www.langchain.com/), allowing you to use VectorX as a vector store backend for LangChain.

## Features

- **Encrypted Vector Storage**: Use VectorX's client-side encryption for your LangChain embeddings
- **Multiple Distance Metrics**: Support for cosine, L2, and inner product distance metrics
- **Metadata Filtering**: Filter search results based on metadata 
- **High Performance**: Optimized for speed and efficiency with encrypted data

## Installation

```bash
pip install vecx-langchain
```

This will install both the `vecx-langchain` package and its dependencies (`vecx`, `langchain`, and `langchain-core`).

## Quick Start

```python
import os
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from vecx.vectorx import VectorX
from vecx_langchain import VectorXVectorStore

# Configure your VectorX credentials
api_token = os.environ.get("VECTORX_API_TOKEN")
vx = VectorX(token=api_token)

# Generate a secure encryption key
encryption_key = vx.generate_key()
# The key is automatically printed with a warning to store it securely

# Initialize embedding model
embedding_model = OpenAIEmbeddings()

# Initialize the vector store
vector_store = VectorXVectorStore.from_params(
    embedding=embedding_model,
    api_token=api_token,
    encryption_key=encryption_key,
    index_name="my_langchain_vectors",
    space_type="cosine"
)

# Add documents
texts = [
    "VectorX is an encrypted vector database",
    "LangChain is a framework for developing applications powered by language models",
    "Encryption keeps your data secure"
]

metadatas = [
    {"source": "product", "category": "database"},
    {"source": "github", "category": "framework"},
    {"source": "textbook", "category": "security"}
]

vector_store.add_texts(texts=texts, metadatas=metadatas)

# Search similar documents
results = vector_store.similarity_search("How does encryption work?", k=2)

# Process results
for doc in results:
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}")
    print()
```

## How Encryption Works

When using the VectorX LangChain integration:

1. **Key Generation**: The `vx.generate_key()` method generates a secure encryption key
2. **Client-Side Encryption**: Your vectors and metadata are encrypted before being sent to the server
3. **Secure Queries**: Query vectors are also encrypted, maintaining security throughout the process
4. **Zero-Knowledge Architecture**: The VectorX server never sees your unencrypted data

## Using with LangChain

VectorX can be used anywhere a LangChain vector store is needed:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from vecx_langchain import VectorXVectorStore

# Initialize your vector store
vector_store = VectorXVectorStore.from_params(
    embedding=OpenAIEmbeddings(),
    api_token="your_api_token",
    encryption_key="your_encryption_key",
    index_name="your_index_name"
)

# Create a retriever
retriever = vector_store.as_retriever()

# Create the RAG chain
model = ChatOpenAI()
prompt = ChatPromptTemplate.from_template(
    """Answer the following question based on the provided context:
    
    Context: {context}
    Question: {question}
    """
)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# Use the chain
response = rag_chain.invoke("What is VectorX?")
print(response)
```

## API Reference

### VectorXVectorStore

The main class for integrating with LangChain. Key methods include:

- `__init__`: Initialize with a VectorX index or parameters to create a new one
- `from_params`: Create a vector store using an API token and encryption key
- `add_texts`: Add text documents with optional metadata
- `similarity_search`: Search for similar documents
- `similarity_search_with_score`: Search and return similarity scores
- `delete`: Delete documents by ID or filter

### Configuration Options

The `VectorXVectorStore` constructor and `from_params` method accept the following parameters:

- `embedding`: LangChain embedding function to use
- `api_token`: Your VectorX API token
- `encryption_key`: Your encryption key for the index
- `index_name`: Name of the VectorX index
- `dimension`: Vector dimension (can be inferred from embedding model)
- `space_type`: Distance metric, one of "cosine", "l2", or "ip" (default: "cosine")
- `text_key`: Key to use for storing text in metadata (default: "text")
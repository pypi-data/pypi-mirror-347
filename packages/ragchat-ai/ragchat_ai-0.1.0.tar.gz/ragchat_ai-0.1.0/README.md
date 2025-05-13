# RagChat

RagChat transforms unstructured data for LLM interaction. Addressing key challenges such as dynamic content updates, diverse data sources, and retrieval accuracy, it incorporates an upsert-first design, flexible filtering, and knowledge graphs alongside vector search for more capable knowledge management. Features including multi-user support, pluggable models, and self-hosting provide operational flexibility and control.

---

## Features
- **Upsert-first design:** Supports constant updates.
- **Flexible metadata filtering:** Information retrieval allows using custom fields.
- **Efficient knowledge graph:** Graph is built using small models, promoting efficiency and scalability.
- **Multiuser support:** Knowledge bases can be isolated or shared.
- **Language consistency:** Manually crafted prompts and examples ensure LLMs consistently use the same language, improving reliability.
- **Async batch processing:** Ingestion and processing of multiple documents can be done in parallel with streaming progress feedback.
- **Pluggable LLMs and Embedding models:** Supports the use of custom models or connection to API endpoints; providers are easily swappable.
- **Open source & self-hostable:** Operation occurs locally in Docker or directly on a machine, ensuring privacy.

## Use Cases
- Casual chat sessions with memories
- Technical documentation search
- Chat+file hybrid RAG with citations
- Personal use
- Multi-user setups

---

## Quick start
Docker Compose is required for the easiest setup.

Install RagChat with pip:
```bash
pip install ragchat-ai
```

Configure environment variables:
```bash
git clone https://github.com/raul3820/ragchat.git
cd ragchat
cp .env.example .env # Add API keys or check ports for local setup
```

## Example: Open Webui

Run dependencies with:
```bash
docker compose up --build
```

After startup, the web chat UI is accessible at http://localhost:3001 (refer to .env for port).

Retrieval will be applied to all models. Two flows are presented:
- Casual chat with memories (default)
- Formal RAG with citations (triggered by writing `#` in the chat and selecting a file)

For file ingestion use: http://localhost:3001/workspace/knowledge


## Example: Lihua benchmark with Python SDK

Run dependencies with:
```bash
docker compose up neo4j --build
```

Once the DB has started, run the file ingestion with:
```python
python -m examples.lihua.step0_index
```

and the Q&A with
```python
python -m examples.lihua.step1_qa
```

---

## Contributing
Contributions welcomed:
- Bug reports (issues)
- Feature suggestions
- Pull requests (inclusion of tests requested)

---

## Roadmap
- Performance:
  - [x] Quick retrieval
  - [x] Query decomposition
  - [ ] Better reranking
  - [ ] Recency weighting
  - [ ] Structured aggregates
  - [ ] Graph traversal
  - [ ] Custom tuning
- Flows:
  - [x] Chat
  - [x] File
  - [ ] Group chat
  - [ ] Web search
- Integrations:
  - [ ] Python SDK
  - [ ] REST API server
  - [x] Neo4j
  - [ ] Neo4j optimization (vector indexing, quantization)
  - [ ] Memgraph? (lower priority)
  - [ ] Docling
  - [ ] MCP
  - [x] Open-Webui (pipelines)
- Testing & Evals:
  - [x] LiHua benchmark setup
  - [ ] LiHua benchmark comparison with other libraries
  - [x] Integration test
  - [ ] Increase test coverage
- Security:
  - [x] Custom fields sanitization
- Documentation:
  - [x] Readme/Quick start
  - [ ] Library documentation
  - [ ] API documentation
  
---

## Open Source & License
RagChat is MIT-licensed (see LICENSE). Self-hosting and extension are permitted. Certain features may require user-provided LLM/API keys.

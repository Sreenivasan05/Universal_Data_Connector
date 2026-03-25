# Universal Data Connector

A production-ready **Universal Data Connector** built with FastAPI that enables LLMs to access multiple data sources through a unified, intelligent interface—optimized for **voice-based AI interactions**.

---

## Overview

This project simulates a SaaS environment where users query business data (CRM, support tickets, analytics) via an AI assistant.

The connector acts as a middleware layer that:

* Normalizes multiple data sources
* Applies business logic
* Optimizes responses for **low-latency voice conversations**
* Exposes a structured API for **LLM function calling**

---

## Features

### Multi-Source Data Connectors

* **CRM Data** – Customer profiles, activity, lifecycle stage
* **Support Tickets** – Issues, statuses, priorities
* **Analytics Data** – Metrics, trends, KPIs

---

### Intelligent Data Handling

* Automatic **data type detection**:

  * Tabular (CRM, tickets)
  * Time-series (analytics)
  * Hierarchical (customer relationships)
* Smart transformations based on data type

---

### Voice-Optimized Responses

* Default result limit: **10 items**
* Smart summarization for large datasets
* Prioritized results (recent/relevant first)
* Context-aware metadata:

  * `"showing 5 of 42 results"`
* Data freshness indicators:

  * `"data as of 2 hours ago"`

---

### Business Rules Engine

* Pagination for large datasets
* Filtering by relevance and recency
* Aggregation for metrics
* Lightweight responses for low bandwidth

---

### LLM Function Calling Ready

* Auto-generated **OpenAPI schema**
* Structured request/response formats
* Strong parameter validation (Pydantic v2)
* Metadata-rich responses for LLM reasoning

---

### Technical Stack

* **Python 3.11+**
* **FastAPI**
* **Pydantic v2**
* **Uvicorn**
* **Docker**

---

## Project Structure

```
app/
│── main.py              # FastAPI entrypoint
│── api/                 # Route definitions
│── models/              # Pydantic schemas
│── services/            # Business logic layer
│── connectors/          # Data source connectors
│── utils/               # Helpers (pagination, summarization)
│── config/              # Settings & environment config
│── mock_data/           # Mock data generators
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Sreenivasan05/Universal_Data_Connector.git
cd universal-data-connector
```

---

### 2. Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3. Run with Docker

```bash
docker-compose up --build
```

---

## API Endpoints

### Health Check

```
GET /health
```

---

### Unified Data Query

```
POST /query
```

#### Example Request:

```json
{
  "source": "crm",
  "query": "recent active customers",
  "limit": 5
}
```

#### Example Response:

```json
{
  "data": [...],
  "metadata": {
    "total_results": 42,
    "returned_results": 5,
    "data_type": "tabular",
    "freshness": "2 hours ago"
  },
  "summary": "Top 5 most recent active customers"
}
```

---

## Mock Data

The project includes mock data generators for:

* Customers
* Support tickets
* Analytics metrics

This allows easy testing without external dependencies.

---

## Design Principles

* **Consistency**: Unified interface across all data sources
* **Performance**: Optimized for low latency and small payloads
* **Extensibility**: Easily add new connectors
* **LLM-Friendly**: Structured outputs with rich metadata
* **Voice-First**: Concise, relevant responses

---






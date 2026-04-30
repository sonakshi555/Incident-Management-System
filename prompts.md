# Development Specifications & Prompt History

## 📋 System Design Plan
1. **Infrastructure:** Orchestrate the environment using Docker Compose for portability.
2. **Reliability:** Implement "Debouncing" logic to suppress alert fatigue (10,000 signals → 1 incident).
3. **Observability:** Print throughput metrics and provide a `/health` endpoint for monitoring.

## 💬 Prompts & Iterations
*   **Initial Build:** "Build a resilient IMS with FastAPI and Docker that can handle 10k signals/sec using a Producer-Consumer pattern."
*   **Database Debugging:** "Refine the PostgreSQL startup logic to include retries until the container is ready to accept connections."
*   **MongoDB Optimization:** "Optimize the background worker to batch signals and convert Pydantic models to JSON-compatible dictionaries for MongoDB insertion."
*   **Troubleshooting:** "Debug MongoDB connection counts and namespace issues where `mongosh` showed 0 count due to default database selection."
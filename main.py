from fastapi import FastAPI
from api.endpoints import documents, question, health

app = FastAPI(title="Industrial RAG API")

app.include_router(health.router)
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(question.router, prefix="/question", tags=["Question"])

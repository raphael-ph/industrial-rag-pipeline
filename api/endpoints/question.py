import os
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

# google imports
from google import genai

# internal imports
from app.pipeline.retrieve import ElasticRetriever
from app.pipeline.generate import RAGAgent
from app.utils.logger import Logger

load_dotenv()
_log = Logger.get_logger(__name__)
google_client = genai.Client()

elastic_url = os.environ["ELASTIC_SEARCH_URL"]
elastic_api_key = os.environ["ELASTIC_SEARCH_API_KEY"]

router = APIRouter()

class QuestionRequest(BaseModel):
    user_id: str
    session_id: str
    index_name: str
    question: str

@router.post("/")
def generate_answer(req: QuestionRequest):
    """Generate answer using RAG with session/user context"""
    retriever = ElasticRetriever(
        elastic_url=elastic_url,
        api_key=elastic_api_key,
        index_name=req.index_name
    )

    agent = RAGAgent(model="gemini-2.5-flash", retriever=retriever)
    response = agent.run(req.question)

    return response

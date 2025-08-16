import time
from typing import Optional
from dotenv import load_dotenv

# google imports
from google import genai
from google.genai import types

# internal imports
from .retrieve import ElasticRetriever
from ..utils.logger import Logger
from ..prompts.rag  import DEFAULT_RAG_PROMPT_TEMPLATE

# set-ups
load_dotenv()
_log = Logger.get_logger(__name__)
google_client = genai.Client()

class RAGAgent:
    def __init__(self,  
                 model: str, 
                 retriever: ElasticRetriever,
                 similarity_threshold: float = 0,
                 name: Optional[str] = "RAG Agent",
                 system_instructions: Optional[str] = "You are a Retrieval-Augmented Generation (RAG) Assistant",
                 additional_instructions: Optional[str] = "",
                 rag_prompt: str = DEFAULT_RAG_PROMPT_TEMPLATE
                 ):
        
        self.model = model
        self.retriever = retriever
        self.similarity_threshold = similarity_threshold
        self.name = name
        self.system_instructions = system_instructions
        self.additional_instructions = additional_instructions
        self.rag_prompt = rag_prompt
    
    def run(self, user_query: str) -> str:
        """Agent run method for generating completions based on documents.
        
        The run method retrieves relevant documents based on the user query and generates
        a completion based on it.

        Arguments:
            user_query (str): The user request for retrieve and generation
        
        Returns:
            string with the agent response.
        """
        # begin by retrieving context
        _log.info(f"Agent '{self.name} is searching for relevant documents'")
        retrieved_documents = self.retriever.retrieve(user_query)
        
        # checking for document relevancy through similarity score
        relevant_documents = [doc for doc in retrieved_documents if doc['score'] >= self.similarity_threshold]
        _log.info(f"Agent '{self.name}' found {len(relevant_documents)} relevant documents from {len(retrieved_documents)} retrieved")

        # defining the formatted context for generation
        formatted_context = "\n\n".join(
            f"Title: {doc['title']}\nScore: {doc['score']}\nContent: {doc['text']}"
            for doc in relevant_documents
        )
        _log.debug(f"Final formatted context from retrieved documents")
        _log.debug(
            f"\n==== FORMATTED CONTEXT START ====\n"
            f"{formatted_context}\n"
            f"==== FORMATTED CONTEXT END ===="
        )

        # prompt formatting
        prompt = self.rag_prompt.format(
            context=formatted_context,
        )
        _log.debug(f"Final formatted prompt for '{self.name}'")
        _log.debug(
            f"\n==== FORMATTED PROMPT START ====\n"
            f"{prompt}\n"
            f"==== FORMATTED PROMPT END ===="
        )

        # creating completion object for Gemini Generation
        contents = [
            types.Content(
                role="model",
                parts=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_text(text=self.additional_instructions)
                ]
            ),
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=user_query)
                ]
            )
        ] 
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=1,
            seed=0,
            max_output_tokens=65535,
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
            ],
            system_instruction=[types.Part.from_text(text=self.system_instructions)],
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )

        # generating response
        # developed a retry loop for the 429 resource exhausted problem
        # the loop has exponential backoff
        max_retries = 3
        backoff = 1  # initial delay in seconds

        for attempt in range(max_retries):
            try:
                _log.info(f"Agent '{self.name}' generating response")
                response = google_client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=generate_content_config,
                )
                _log.info(f"Response generated successfully: {response.text[:50]}...")
                break 
            except Exception as e:
                if attempt < max_retries - 1:
                    sleep_time = backoff * (2 ** attempt)
                    _log.warning(f"Could not generate response due to {e}")
                    _log.warning(f"Retrying in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                else:
                    _log.error("Max retries reached. Raising exception.")
                    raise

        return response.text
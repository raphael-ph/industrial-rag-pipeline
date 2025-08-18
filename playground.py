import streamlit as st
import os
from dotenv import load_dotenv
from app.pipeline.retrieve import ElasticRetriever
from app.pipeline.generate import RAGAgent
from app.utils.logger import Logger

# Load environment variables
load_dotenv(override=True)
_log = Logger.get_logger(__name__)

# Configuration
elastic_url = os.environ["ELASTIC_SEARCH_URL"]
elastic_api_key = os.environ["ELASTIC_SEARCH_API_KEY"]
# Replace with your actual populated index name
index_name = os.environ.get("INDEX_NAME", "default-evaluation-index")

# Page configuration
st.set_page_config(
    page_title="RAG Demo",
    page_icon="🔍",
    layout="wide"
)

# Initialize components (with caching for better performance)
@st.cache_resource
def initialize_rag_system():
    """Initialize the RAG system components."""
    try:
        retriever = ElasticRetriever(
            elastic_url=elastic_url,
            api_key=elastic_api_key,
            index_name=index_name,
        )
        
        agent = RAGAgent(model="gemini-2.5-flash", retriever=retriever)
        return agent, True
    except Exception as e:
        st.error(f"Failed to initialize RAG system: {e}")
        _log.error(f"Initialization error: {e}")
        return None, False

def main():
    # Header
    st.title("🔍 RAG System Demo")
    st.markdown("---")
    
    # Instructions
    st.markdown(f"""
    ### 📋 Instructions
                
    You are connected to ´{index_name}´
    
    This is a simple demo of our RAG (Retrieval-Augmented Generation) system. 
    Ask questions about the indexed documents and get AI-powered answers.
    
    **Try asking questions like:**
    
    > *"What are the general safety guidelines and initial inspection procedures for AC & DC motors upon receiving them and before installation?"*
    
    > *"What is the process before accepting a motor?"*
    
    > *"What are the maintenance requirements?"*
    """)
    
    st.markdown("---")
    
    # Initialize RAG system
    with st.spinner("Initializing RAG system..."):
        agent, success = initialize_rag_system()
    
    if not success:
        st.stop()
    
    # Query interface
    st.subheader("💬 Ask your question")
    
    # Text area for user query
    user_query = st.text_area(
        "Enter your question:",
        placeholder="Type your question here...",
        height=100,
        key="query_input"
    )
    
    # Query button
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        query_button = st.button("🔍 Ask", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.rerun()
    
    # Process query
    if query_button and user_query.strip():
        with st.spinner("Searching and generating answer..."):
            try:
                # Get response from RAG agent
                response = agent.run(user_query)
                
                if response and isinstance(response, dict):
                    st.markdown("---")
                    st.subheader("📖 Answer")
                    
                    # Display the main answer
                    if "answer" in response:
                        st.markdown(response["answer"])
                    elif "response" in response:
                        st.markdown(response["response"])
                    else:
                        st.markdown(str(response))
                    
                    # Show additional information if available
                    with st.expander("🔍 Additional Information", expanded=False):
                        col_left, col_right = st.columns(2)
                        
                        with col_left:
                            if "sources" in response:
                                st.markdown("**📄 Sources:**")
                                for i, source in enumerate(response["sources"], 1):
                                    st.markdown(f"{i}. {source}")
                        
                        with col_right:
                            if "metadata" in response:
                                st.markdown("**ℹ️ Metadata:**")
                                st.json(response["metadata"])
                        
                        # Show full response structure
                        st.markdown("**🔧 Full Response Structure:**")
                        st.json(response)
                
                else:
                    st.error("❌ Received an invalid response from the RAG agent")
                    
            except Exception as e:
                st.error(f"❌ Error processing your question: {e}")
                _log.error(f"Query processing error: {e}")
    
    elif query_button and not user_query.strip():
        st.warning("⚠️ Please enter a question before clicking 'Ask'")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
        RAG System Demo | Powered by Elasticsearch + Gemini
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
from app.agents.state import AgentState
from app.services.chromadb_service import chroma_service


### So based on classifier agent query_type it retrives the cimilar document
class RetrieverAgent:
    def __init__(self):
        self.default_results = 5
    
    def retrieve(self, state: AgentState) -> AgentState:
        query = state["query"]
        query_type = state.get("query_type", "factual")
        
        # Adjust number of results based on query type
        n_results = 7 if query_type in ["comparison", "analysis"] else 5
        
        results = chroma_service.query_documents(query, n_results=n_results)
        
        if results and results["documents"]:
            state["retrieved_docs"] = results["documents"][0]
            state["sources"] = [
                f"Source {i+1}: {doc[:100]}..." 
                for i, doc in enumerate(results["documents"][0])
            ]
            state["steps"].append(f"Retrieved {len(state['retrieved_docs'])} relevant documents")
        else:
            state["retrieved_docs"] = []
            state["sources"] = []
            state["steps"].append("No relevant documents found")
        
        return state

retriever_agent = RetrieverAgent()
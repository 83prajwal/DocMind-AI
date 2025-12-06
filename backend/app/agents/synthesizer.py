from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config import settings
from app.agents.state import AgentState


### From Retriever agent we retrieve the document and based on agent_type we make  sentence concise and we join all documents and provide the answer
class SynthesizerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.3,
            model="gpt-3.5-turbo",
            api_key=settings.openai_api_key
        )
    
    def synthesize(self, state: AgentState) -> AgentState:
        query = state["query"]
        docs = state.get("retrieved_docs", [])
        query_type = state.get("query_type", "factual")
        
        if not docs:
            state["answer"] = "I couldn't find relevant information to answer your question."
            state["steps"].append("Generated fallback response")
            return state
        
        ### Combine all 5 documents into one big text
        context = "\n\n".join(docs)
        
        prompt_templates = {
            "factual": "Answer this question concisely based on the context:\n\nContext: {context}\n\nQuestion: {query}",
            "summary": "Provide a comprehensive summary based on the context:\n\nContext: {context}\n\nFocus: {query}",
            "comparison": "Compare and contrast based on the context:\n\nContext: {context}\n\nComparison request: {query}",
            "analysis": "Provide a detailed analysis based on the context:\n\nContext: {context}\n\nAnalysis request: {query}"
        }
        
        template = prompt_templates.get(query_type, prompt_templates["factual"])
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Use only the provided context to answer."),
            ("user", template)
        ])
        
        chain = prompt | self.llm
        result = chain.invoke({"context": context, "query": query})
        
        state["answer"] = result.content
        state["steps"].append(f"Generated {query_type} response")
        return state

synthesizer_agent = SynthesizerAgent()
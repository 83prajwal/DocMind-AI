from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config import settings
from app.agents.state import AgentState


#### Classifies the question whether it is factual, summary or etc
class QueryAnalyzerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            api_key=settings.openai_api_key
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Analyze the user query and classify it into one of these types:
            - factual: Simple fact-based questions
            - summary: Requests for summaries or overviews
            - comparison: Comparing multiple items or documents
            - analysis: Deep analysis or explanation requests
            
            Return only the type name, nothing else."""),
            ("user", "{query}")
        ])
    
    def analyze(self, state: AgentState) -> AgentState:
        chain = self.prompt | self.llm
        result = chain.invoke({"query": state["query"]})
        
        state["query_type"] = result.content.strip().lower()
        state["steps"].append(f"Query analyzed as: {state['query_type']}")
        return state

query_analyzer = QueryAnalyzerAgent()
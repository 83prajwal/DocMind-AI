from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.query_analyzer import query_analyzer
from app.agents.retriever import retriever_agent
from app.agents.synthesizer import synthesizer_agent

def create_agent_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("analyze", query_analyzer.analyze) ### Agent 1
    workflow.add_node("retrieve", retriever_agent.retrieve)  ### Agent 2
    workflow.add_node("synthesize", synthesizer_agent.synthesize)  ### Agent 3
    
    # Define edges
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "retrieve")
    workflow.add_edge("retrieve", "synthesize")
    workflow.add_edge("synthesize", END)
    
    return workflow.compile()

agent_graph = create_agent_graph()
from typing import TypedDict, List

class AgentState(TypedDict):
    query: str
    query_type: str
    retrieved_docs: List[str]
    answer: str
    sources: List[str]
    steps: List[str]
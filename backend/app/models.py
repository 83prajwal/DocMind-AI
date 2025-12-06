from pydantic import BaseModel
from typing import List, Optional

class UploadRequest(BaseModel):
    content: str
    filename: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    query_type: str
    agent_steps: List[str]
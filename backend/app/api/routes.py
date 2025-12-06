from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models import QueryRequest, QueryResponse
from app.services.chromadb_service import chroma_service
from app.services.document_processor import document_processor
from app.agents.graph import agent_graph
from app.agents.state import AgentState
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload document file (PDF, TXT, DOCX)"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Extract text based on file type
        text = document_processor.process_file(file_content, file.filename)
        
        # Chunk the text
        chunks = document_processor.chunk_text(text)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No text content found in file")
        
        # Generate IDs and metadata
        ids = [f"{file.filename}_{i}_{uuid.uuid4()}" for i in range(len(chunks))]
        metadatas = [{"filename": file.filename, "chunk_id": i} for i in range(len(chunks))]
        
        # Store in ChromaDB
        chroma_service.add_documents(chunks, metadatas, ids)
        
        return {
            "message": "Document uploaded successfully",
            "filename": file.filename,
            "chunks": len(chunks),
            "total_characters": len(text)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query uploaded documents"""
    try:
        initial_state: AgentState = {
            "query": request.query,
            "query_type": "",
            "retrieved_docs": [],
            "answer": "",
            "sources": [],
            "steps": []
        }
        
        result = agent_graph.invoke(initial_state)
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            query_type=result["query_type"],
            agent_steps=result["steps"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    try:
        # Get all documents from ChromaDB
        collection = chroma_service.collection
        all_data = collection.get()
        
        # Extract unique filenames
        filenames = set()
        if all_data and all_data.get("metadatas"):
            for metadata in all_data["metadatas"]:
                if metadata and "filename" in metadata:
                    filenames.add(metadata["filename"])
        
        return {
            "total_documents": len(filenames),
            "total_chunks": len(all_data.get("ids", [])),
            "documents": list(filenames)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_database():
    """Reset the entire database"""
    try:
        chroma_service.reset()
        return {"message": "Database reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
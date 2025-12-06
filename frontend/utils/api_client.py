import requests
from typing import Optional, Dict, Any
from config import config

class APIClient:
    def __init__(self):
        self.base_url = config.BACKEND_URL
    
    def upload_file(self, file) -> Dict[str, Any]:
        """Upload a file to the backend"""
        try:
            files = {"file": (file.name, file, file.type)}
            response = requests.post(f"{self.base_url}/api/upload", files=files)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def upload_text(self, content: str, filename: str = "direct_input.txt") -> Dict[str, Any]:
        """Upload text content directly"""
        try:
            response = requests.post(
                f"{self.base_url}/api/upload-text",
                params={"filename": filename},
                json={"content": content}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def query(self, query: str) -> Dict[str, Any]:
        """Send a query to the backend"""
        try:
            response = requests.post(
                f"{self.base_url}/api/query",
                json={"query": query}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_documents(self) -> Dict[str, Any]:
        """Get list of uploaded documents"""
        try:
            response = requests.get(f"{self.base_url}/api/documents")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def reset_database(self) -> Dict[str, Any]:
        """Reset the database"""
        try:
            response = requests.post(f"{self.base_url}/api/reset")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

api_client = APIClient()
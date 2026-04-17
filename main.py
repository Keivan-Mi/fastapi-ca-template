"""
Entry point to run the Task Manager API.
Usage (from project root):
  python main.py
  or
  uvicorn src.app:app --reload --host 0.0.0.0
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

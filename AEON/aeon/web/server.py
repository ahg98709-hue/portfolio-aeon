import sys
import os

# Ensure project root is in path
path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(path))))

import uvicorn
import threading
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from aeon.core.engine import Engine

from contextlib import asynccontextmanager

app = FastAPI(title="AEON Interface")

# Global Engine
engine = None
lock = threading.Lock()

class ChatRequest(BaseModel):
    message: str

def log_output(text: str):
    print(f"\033[96m[AEON]\033[0m {text}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global engine
    print("[INFO] Initializing AEON Engine...")
    try:
        engine = Engine(output_handler=log_output)
    except Exception as e:
        print(f"[ERROR] Failed to start engine: {e}")
    yield
    # Shutdown
    print("[INFO] Shutting down AEON Engine...")

app = FastAPI(title="AEON Interface", lifespan=lifespan)

@app.post("/api/chat")
async def chat(request: ChatRequest):
    global engine
    if not engine:
        return JSONResponse(status_code=500, content={"error": "Engine not initialized"})
    
    with lock:
        response = engine.chat(request.message)
    
    return {"response": response}

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

def start():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    start()

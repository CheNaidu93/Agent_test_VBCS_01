from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.models import ChatRequest, ChatResponse
from app.chatbot import bot_instance


app = FastAPI(
    title="Python Web Chatbot API",
    description="REST API and Website interface for AI Chatbot.",
    version="1.0.0"
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the HTML UI at root URL
@app.get("/", response_class=FileResponse)
def serve_website():
    return FileResponse(os.path.join("static", "index.html"))

# ---------------- REST ENDPOINTS ----------------

@app.post("/api/v1/chat", response_model=ChatResponse)
def handle_chat(payload: ChatRequest):
    """
    POST Endpoint: Accepts user prompt, processes response, returns JSON payload.
    """
    try:
        #reply = bot_instance.get_response(payload.user_id, payload.message)
        reply = bot_instance.get_response(payload.user_id, payload.message, 
                                          payload.context.model_dump() if payload.context else None 
                                         )
        
        history = bot_instance.get_history(payload.user_id)
        
        return ChatResponse(
            user_id=payload.user_id,
            response=reply,
            history_length=len(history)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/history/{user_id}")
def get_chat_history(user_id: str):
    """
    GET Endpoint: Fetches full JSON chat history for the given user session.
    """
    history = bot_instance.get_history(user_id)
    return {"user_id": user_id, "history": history}

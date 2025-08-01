from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from .services.rag import RAGService
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
rag_service = RAGService()

@app.post("/webhook", response_class=PlainTextResponse)
async def whatsapp_webhook(
    request: Request,
    Body: str = Form(None),
    From: str = Form(...),
    MediaContentType0: str = Form(None),
    MediaUrl0: str = Form(None)
):
    print(f"Incoming message from {From}")
    
    response = MessagingResponse()
    
    if Body:
        print(f"Text message: {Body}")
        # Use RAG to get relevant context
        context = await rag_service.query(Body)
        print(context)
        response.message(f"Here's what I found:\n\n{context}")
    elif MediaContentType0 and "audio" in MediaContentType0:
        print(f"Received voice message at: {MediaUrl0}")
        response.message("Received your voice message! Processing...")
    elif MediaContentType0 and "image" in MediaContentType0:
        print(f"Received image message at: {MediaUrl0}")
        response.message("Received your image! Processing...")
    else:
        response.message("Unsupported message type.")

    return str(response)
from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

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
        response.message(f"You said: {Body}")
    elif MediaContentType0 and "audio" in MediaContentType0:
        print(f"Received voice message at: {MediaUrl0}")
        response.message("Received your voice message! Processing...")
    else:
        response.message("Unsupported message type.")

    return str(response)

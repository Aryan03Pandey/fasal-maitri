# from .context_manager import append_message, get_recent
# from .services.embedding import get_embedding
import re
from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select
from app.models import Base, User, AgriculturalData
from app.database import AsyncSessionLocal  # Add this import if not present


load_dotenv("../.env")
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
    number = re.search(r'\+91(\d{10})', From).group(0)
    print(number)
    exists = await user_exists(number)
    if exists == False:
        # Create new user with default details
        new_user = await create_user(
            phone_number=number,
            name="New User",  # You can modify this or get from user input
            language="en",    # Default language
            location="India"  # Default location
        )
        print(f"Created new user: {new_user.name}")
    
    print(f"User exists: {exists}")
    
    response = MessagingResponse()
    
    if Body:
        print(f"Text message: {Body}")
        response.message(f"You said and we are processing it: {Body}")
    elif MediaContentType0 and "audio" in MediaContentType0:
        print(f"Received voice message at: {MediaUrl0}")
        response.message("Received your voice message! Processing...")
    elif MediaContentType0 and "image" in MediaContentType0:
        print(f"Received image message at: {MediaUrl0}")
        response.message("Received your voice message! Processing...")
    else:
        response.message("Unsupported message type.")

    xml_str = str(response)

    # Extract meaningful message text
    root = ET.fromstring(xml_str)
    message = ""
    for message in root.findall('Message'):
        if message.text and message.text.strip():
            
            message = message.text

    return str(message)

async def user_exists(phone_number: str) -> bool:
    """
    Check if a user exists in the database with the given phone number.
    Returns True if exists, False otherwise.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.phone_number == phone_number)
        )
        user = result.scalar_one_or_none()
        return user is not None

async def create_user(phone_number: str, name: str = None, language: str = "en", location: str = None) -> User:
    """
    Create a new user in the database with the given details.
    Returns the created user object.
    """
    async with AsyncSessionLocal() as session:
        try:
            new_user = User(
                phone_number=phone_number,
                name=name,
                language=language,
                location=location
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            print(f"✅ User created successfully: {new_user.name} ({new_user.phone_number})")
            return new_user
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            await session.rollback()
            raise e
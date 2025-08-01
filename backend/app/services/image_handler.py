import os
import requests
from .gemini import process_image_prompt

def handle_incoming_image(form, caption):
    media_url = form.get("MediaUrl0")
    media_content_type = form.get("MediaContentType0")
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
    response = requests.get(media_url, auth=(twilio_sid, twilio_token))
    if response.status_code == 200:
        image_bytes = response.content
        if media_content_type and media_content_type.startswith("image/"):
            return process_image_prompt(image_bytes, media_content_type, caption)
        else:
            return f"Received a {media_content_type.split('/')[0]} message. Processing..."
    else:
        return "Sorry, could not download the media."
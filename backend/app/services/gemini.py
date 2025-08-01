import os
import requests
import base64


def process_image_prompt(image_bytes, content_type, caption):
    """
    Sends the image and caption to the Gemini API and returns the response.
    """
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"

    if not GEMINI_API_KEY:
        return "Gemini API key not set."

    # Encode image as base64
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # Gemini expects a JSON payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": caption
                    },
                    {
                        "inline_data": {
                            "mime_type": content_type,
                            "data": image_b64
                        }
                    }
                ]
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response from Gemini.")
        else:
            return f"Gemini API error: {response.status_code} {response.text}"
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"
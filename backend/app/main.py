from fastapi import FastAPI, Request
from .context_manager import append_message, get_recent
from .services.embedding import get_embedding

app = FastAPI()

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    from_number = form.get("From")
    body = form.get("Body", "")
    session_id = from_number  # simple session key

    # store user message
    append_message(session_id, "user", body)

    # simplistic processing: get embedding (could be used to retrieve context)
    emb = get_embedding(body)  # placeholder usage

    # build context text
    recent = get_recent(session_id)
    context_text = "\n".join([f"{m['role']}: {m['text']}" for m in recent])

    # create prompt for Gemini (pseudo)
    prompt = f"Conversation history:\n{context_text}\nUser: {body}\nAnswer the question, debunk any myths, in simple code-switched Indian style."

    # call Gemini API here (stub)
    answer = f"Echoing: {body} (would call Gemini with prompt)"

    append_message(session_id, "assistant", answer)

    # respond in format Twilio expects (simple text)
    from fastapi.responses import PlainTextResponse
    response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{answer}</Message>
</Response>"""
    return PlainTextResponse(content=response_xml, media_type="application/xml")

import os
import httpx
import json
import uvicorn
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv

# Wczytanie zmiennych z .env
load_dotenv()

app = FastAPI()

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "WhatsApp Bot is running"}

@app.head("/")
async def health_check_head():
    return Response(status_code=200)

@app.head("/webhook")
async def webhook_head():
    return Response(status_code=200)

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    print("\n PRÓBA WERYFIKACJI WEBHOOKA:")
    print(f"   Token z zapytania: '{params.get('hub.verify_token')}'")
    print(f"   Oczekiwany token: '{VERIFY_TOKEN}'")
    print(f"   Czy się zgadzają: {params.get('hub.verify_token') == VERIFY_TOKEN}")
    
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        print("✅ WERYFIKACJA UDANA!")
        return Response(content=params.get("hub.challenge"), media_type="text/plain")
    print(" BŁĄD WERYFIKACJI: Tokeny się nie zgadzają!")
    return "Błąd weryfikacji"

@app.post("/webhook")
async def handle_whatsapp_message(request: Request):
    data = await request.json()
    # DODAJ TĘ LINIĘ:
    print("--- OTRZYMANO DANE ---")
    print(data)
    
    try:
        if "messages" in data["entry"][0]["changes"][0]["value"]:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message["from"]
            
            if message["type"] == "text":
                text = message["text"]["body"]
                print(f" Wiadomość od {sender}: {text}")
                
                await send_whatsapp_message(sender, f"Otrzymałem: {text}. Bot działa!")
    except Exception as e:
        print(f"🔥 Błąd: {e}")
        
    return {"status": "ok"}

async def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, json=payload)
        print(f"🚀 Status wysyłki: {res.status_code}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
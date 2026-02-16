import os
import httpx
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")
# WPISZ SWÓJ NUMER TUTAJ (z 48 na początku, same cyfry)
MY_PHONE = "48515000702" 

url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}
data = {
    "messaging_product": "whatsapp",
    "to": MY_PHONE,
    "type": "text",
    "text": {"body": "Cześć! To ja, Twój bot RAG. Słyszę Cię!"}
}

with httpx.Client() as client:
    response = client.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.json())
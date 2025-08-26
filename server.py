from flask import Flask, request
import requests
import openai

app = Flask(__name__)

# === CONFIG ===
TELEGRAM_TOKEN = "8374647796:AAGJK6SiU610jsIti6wuXKs4QKomwdrvAO8"
CHAT_ID = "1588912383"  
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

def send_telegram(msg):
    """Send a message to your Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

@app.route("/cursor-task", methods=["POST"])
def cursor_task():
    """Receive POST request with a prompt and send result to Telegram."""
    data = request.json
    if not data or "prompt" not in data:
        return {"status": "error", "message": "Missing 'prompt' in JSON body"}, 400

    prompt = data["prompt"]

    # Query OpenAI (or replace later with Cursor local API if needed)
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = completion.choices[0].message["content"]

    # Send reply to Telegram
    send_telegram(f"📢 Reply for your request:\n\n{reply}")

    return {"status": "ok", "reply": reply}

if __name__ == "__main__":
    # Listen on all interfaces for Render deployment
    app.run(host="0.0.0.0", port=5000)

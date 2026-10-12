import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="/static")

HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct")
HF_URL = "https://router.huggingface.co/v1/chat/completions"

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.get("/health")
def health():
    return jsonify({"status": "ok", "ai_configured": bool(HF_TOKEN)})

@app.post("/api/chat")
def chat():
    if not HF_TOKEN:
        return jsonify({"error": "सर्वर पर HF_TOKEN सेट नहीं है। Hugging Face token को hosting की Environment Variables में जोड़ें।"}), 503

    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"error": "कृपया पहले अपना सवाल लिखें।"}), 400
    if len(message) > 4000:
        return jsonify({"error": "मैसेज बहुत लंबा है। कृपया 4000 अक्षरों से छोटा मैसेज भेजें।"}), 400

    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    body = {
        "model": HF_MODEL,
        "messages": [
            {"role": "system", "content": "You are VISHAL AI, a friendly and helpful assistant. Reply in the language the user uses, especially natural Hindi/Hinglish when appropriate. Be honest about uncertainty."},
            {"role": "user", "content": message}
        ],
        "max_tokens": 700,
        "temperature": 0.7
    }
    try:
        r = requests.post(HF_URL, headers=headers, json=body, timeout=60)
        if r.status_code >= 400:
            # Avoid exposing token or raw upstream internals to visitors.
            if r.status_code in (401, 403):
                return jsonify({"error": "AI token सही नहीं है या इस मॉडल की अनुमति उपलब्ध नहीं है। Hugging Face token/model access जाँचें।"}), 502
            if r.status_code == 429:
                return jsonify({"error": "AI की मुफ्त सीमा या rate limit पूरी हो गई है। कुछ देर बाद फिर कोशिश करें।"}), 429
            return jsonify({"error": "AI सेवा ने अनुरोध स्वीकार नहीं किया। HF_MODEL की उपलब्धता और token access जाँचें।"}), 502
        data = r.json()
        choices = data.get("choices", [])
        reply = choices[0].get("message", {}).get("content", "") if choices else ""
        if not reply:
            return jsonify({"error": "AI से खाली जवाब मिला। बाद में फिर कोशिश करें।"}), 502
        return jsonify({"reply": reply})
    except requests.Timeout:
        return jsonify({"error": "AI जवाब देने में समय ले रही है। कृपया फिर कोशिश करें।"}), 504
    except requests.RequestException:
        return jsonify({"error": "AI सेवा से कनेक्ट नहीं हो पाया। इंटरनेट या AI सेवा की स्थिति जाँचें।"}), 502

if __name__ == "__main__":
    port = int(os.getenv("PORT", "7860"))
    app.run(host="0.0.0.0", port=port)

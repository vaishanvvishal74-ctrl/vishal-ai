# VISHAL AI — शुरुआती प्रोजेक्ट

यह responsive website UI और Flask backend है। AI जवाब पाने के लिए Hugging Face Inference Providers API token और उपलब्ध मॉडल access की जरूरत होगी। मुफ्त उपयोग/मॉडल की उपलब्धता बदल सकती है; ₹0 में असीमित AI की गारंटी नहीं है।

## फाइलें
- `index.html` — वेबसाइट का पेज
- `static/style.css` — डिजाइन
- `static/app.js` — चैट इंटरफेस
- `app.py` — सुरक्षित backend; token ब्राउज़र में नहीं जाता
- `requirements.txt` — Python packages

## मोबाइल पर स्थानीय रूप से चलाना (Termux)
1. Python install करें।
2. ZIP extract करें और इस folder में जाएँ।
3. चलाएँ: `pip install -r requirements.txt`
4. Hugging Face token को environment variable में रखें:
   `export HF_TOKEN='अपना_टोकन_यहाँ'`
5. चलाएँ: `python app.py`
6. ब्राउज़र में `http://127.0.0.1:7860` खोलें।

## ऑनलाइन deploy
किसी Python web host पर इस project को deploy करें। Build/install command: `pip install -r requirements.txt`; start command: `gunicorn app:app`.
Environment Variables में:
- `HF_TOKEN` = Hugging Face access token (secret)
- `HF_MODEL` = ऐसा chat model जो आपके खाते के Inference Providers के माध्यम से उपलब्ध हो; default `Qwen/Qwen2.5-7B-Instruct` है, पर इसकी उपलब्धता/प्रदाता बदल सकते हैं।

**सुरक्षा:** token को `index.html`, `static/app.js`, GitHub public code, या APK में न डालें। उसे केवल hosting की server-side secret/environment variable में रखें। किसी token को चैट में साझा न करें।

## सीमाएँ
- अभी login, persistent chat history, image generation और file upload शामिल नहीं हैं।
- एक request में एक user message भेजा जाता है; multi-turn memory अभी शामिल नहीं है।
- यह शुरुआती demo है; public launch से पहले rate limiting, abuse protection, privacy policy और usage monitoring जोड़ें।

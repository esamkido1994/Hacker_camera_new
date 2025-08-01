from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # تحميل متغيرات البيئة من ملف .env

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise Exception("يجب ضبط TELEGRAM_BOT_TOKEN و TELEGRAM_CHAT_ID في ملف .env")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_photo", methods=["POST"])
def upload_photo():
    if "photo" not in request.files:
        return jsonify({"success": False, "error": "لم يتم رفع صورة"}), 400
    
    photo = request.files["photo"]
    files = {"photo": (photo.filename, photo.stream, photo.mimetype)}
    data = {"chat_id": CHAT_ID}

    resp = requests.post(f"{TELEGRAM_API_URL}/sendPhoto", data=data, files=files)
    if resp.status_code == 200:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": resp.text}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
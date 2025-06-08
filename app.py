from flask import Flask, request, jsonify, send_file, render_template
from pytube import YouTube
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download', methods=['POST'])
def download_audio():
    try:
        data = request.get_json(silent=True)
        if not data or 'url' not in data:
            return jsonify({"error": "Brak poprawnego JSON lub URL"}), 400

        url = data['url'].strip()
        if not url.startswith('http'):
            return jsonify({"error": "Nieprawidłowy link"}), 400

        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True, file_extension='webm').first()
        if not audio_stream:
            return jsonify({"error": "Nie znaleziono audio"}), 404

        filename = f"{uuid.uuid4()}.webm"
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        audio_stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print("❌ Błąd backendu:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

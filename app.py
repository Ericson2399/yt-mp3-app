from flask import Flask, render_template, request, send_file
import yt_dlp, os

app = Flask(__name__)

# Carpeta temporal donde se guardarán los archivos descargados
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
    }
    
    # Descarga y convierte a MP3
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
        # Buscar archivos .mp3 y seleccionar estrictamente el más reciente
        mp3_files = [os.path.join(DOWNLOAD_FOLDER, f) for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith(".mp3")]
        if not mp3_files:
            return "Error al crear el MP3", 500
        
        latest_mp3 = max(mp3_files, key=os.path.getmtime)
        
    return send_file(latest_mp3, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
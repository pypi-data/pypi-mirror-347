from flask import Flask, request, send_file, jsonify
from .mdl import download
from pathlib import Path

app = Flask(__name__)

@app.route("/api/download", methods=["POST"])
def handle():
    d = request.get_json(force=True)
    url  = d.get("url")
    acc  = d.get("mullvad_account")
    res  = d.get("resolution")
    ext  = d.get("extension")
    if not url or not acc:
        return jsonify(error="url and mullvad_account required"), 400
    try:
        path = download(url, acc, res, ext)
    except Exception as e:
        return jsonify(error=str(e)), 500
    return send_file(path, as_attachment=True)

def main():
    app.run(host="0.0.0.0", port=5000)

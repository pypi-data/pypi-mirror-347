#!/usr/bin/env python3
from flask import Flask, request, send_file, jsonify
import subprocess
from pathlib import Path

# import helper from your existing code
from .mdl import ensure_venv_with_packages

app = Flask(__name__)

@app.route("/api/download", methods=["POST"])
def download_route():
    data = request.get_json(force=True)
    url  = data.get("url")
    acc  = data.get("mullvad_account")
    res  = data.get("resolution")
    ext  = data.get("extension")

    if not url or not acc:
        return jsonify(error="url and mullvad_account required"), 400

    cmd = ["python3", "-m", "ytp_dl.mdl", url, acc]
    if res: cmd += ["--resolution", res]
    if ext: cmd += ["--extension", ext]

    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        return jsonify(error="download failed", output=proc.stdout), 500

    filename = next((l.split("DOWNLOADED_FILE:")[1].strip()
                     for l in proc.stdout.splitlines()
                     if l.startswith("DOWNLOADED_FILE:")), None)

    if not filename or not Path(filename).exists():
        return jsonify(error="file not found"), 404

    # --- critical change: add download_name so curl -O -J works ---
    return send_file(
        filename,
        as_attachment=True,
        download_name=Path(filename).name   # Flask ≥3
    )

def main():
    # optional: create venv inside /opt if you still want that behaviour
    # ensure_venv_with_packages("/opt/yt-dlp-mullvad/venv")
    app.run(host="0.0.0.0", port=5000)

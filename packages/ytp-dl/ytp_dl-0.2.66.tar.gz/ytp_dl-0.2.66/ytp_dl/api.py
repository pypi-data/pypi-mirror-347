#!/usr/bin/env python3
from flask import Flask, request, send_file, jsonify
import subprocess
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def handle_download():
    data = request.get_json(force=True)
    url = data.get("url")
    mullvad_account = data.get("mullvad_account")
    resolution = data.get("resolution")
    extension = data.get("extension")

    if not url or not mullvad_account:
        return jsonify(error="url and mullvad_account required"), 400

    # Run mdl.py via -m to avoid PATH issues
    cmd = ["python3", "-m", "ytp_dl.mdl", url, mullvad_account]
    if resolution:
        cmd.extend(["--resolution", resolution])
    if extension:
        cmd.extend(["--extension", extension])

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output = result.stdout

    if result.returncode != 0:
        return jsonify(error="Download failed", output=output), 500

    filename = next((l.split("DOWNLOADED_FILE:")[1].strip()
                     for l in output.splitlines()
                     if l.startswith("DOWNLOADED_FILE:")), None)

    if filename and os.path.exists(filename):
        return send_file(filename, as_attachment=True, download_name=Path(filename).name)
    return jsonify(error="No downloaded file found", output=output), 404

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()

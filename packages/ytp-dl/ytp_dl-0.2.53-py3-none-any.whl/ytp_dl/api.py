#!/usr/bin/env python3
from flask import Flask, request, send_file, jsonify
import subprocess
import os
import tempfile
import shutil

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def handle_download():
    data = request.get_json(force=True)
    url = data.get("url")
    mullvad_account = data.get("mullvad_account")
    resolution = data.get("resolution")
    extension = data.get("extension")

    if not url:
        return jsonify(error="Missing 'url'"), 400
    if not mullvad_account:
        return jsonify(error="Missing 'mullvad_account'"), 400

    temp_dir = tempfile.mkdtemp()
    try:
        # Use full path to ytp-dl for reliability
        cmd = ["/usr/local/bin/ytp-dl", url, mullvad_account, "--output-dir", temp_dir]
        if resolution:
            cmd.extend(["--resolution", resolution])
        if extension:
            cmd.extend(["--extension", extension])

        result = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output = result.stdout

        if result.returncode != 0:
            return jsonify(error="Download failed", output=output), 500

        filename = None
        for line in output.splitlines():
            if line.startswith("DOWNLOADED_FILE:"):
                filename = line.split("DOWNLOADED_FILE:")[1].strip()
                break

        if filename and os.path.exists(filename):
            return send_file(filename, as_attachment=True)
        else:
            return jsonify(error="No downloaded file found", output=output), 404
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
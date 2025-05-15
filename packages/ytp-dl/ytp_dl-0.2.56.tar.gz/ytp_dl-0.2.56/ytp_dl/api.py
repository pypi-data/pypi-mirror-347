#!/usr/bin/env python3
from flask import Flask, request, send_file, jsonify
import subprocess
import os
import sys
import shutil

# Add the package directory to sys.path
package_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(package_dir)

from mdl import main as mdl_main

app = Flask(__name__)
DOWNLOAD_DIR = "/root"

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

    # Prepare arguments for mdl.py
    args = [url, mullvad_account]
    if resolution:
        args.extend(["--resolution", resolution])
    if extension:
        args.extend(["--extension", extension])

    # Run mdl.py directly
    try:
        # Capture output by redirecting stdout
        import io
        stdout = io.StringIO()
        sys.stdout = stdout
        mdl_main(args)
        output = stdout.getvalue()
        sys.stdout = sys.__stdout__
    except SystemExit:
        output = stdout.getvalue()
        sys.stdout = sys.__stdout__

    filename = None
    for line in output.splitlines():
        if line.startswith("DOWNLOADED_FILE:"):
            filename = line.split("DOWNLOADED_FILE:")[1].strip()
            break

    if filename and os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    else:
        return jsonify(error="No downloaded file found", output=output), 404

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
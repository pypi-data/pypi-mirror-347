#!/usr/bin/env python3
from flask import Flask, request, send_file, jsonify
import yt_dlp
import subprocess
import os
import shutil
import tempfile
import time

app = Flask(__name__)

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Command failed: {cmd}\nError: {e.output}")

@app.route('/api/download', methods=['POST'])
def handle_download():
    data = request.get_json(force=True)
    url = data.get("url")
    mullvad_account = data.get("mullvad_account")
    resolution = data.get("resolution")
    extension = data.get("extension")

    if not url or not mullvad_account:
        return jsonify(error="Missing 'url' or 'mullvad_account'"), 400

    # Connect to VPN
    run_command(f"mullvad account login {mullvad_account}")
    run_command("mullvad connect")
    time.sleep(10)

    temp_dir = tempfile.mkdtemp()
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        if resolution:
            ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]'
        if extension:
            if extension in ["mp3", "m4a", "aac", "wav", "flac", "opus", "ogg"]:
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': extension,
                }]
            else:
                ydl_opts['merge_output_format'] = extension or 'mp4'

        # Download the content
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if os.path.exists(filename):
            return send_file(filename, as_attachment=True)
        else:
            return jsonify(error="Download failed: File not found"), 500
    finally:
        # Disconnect VPN and clean up
        run_command("mullvad disconnect")
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
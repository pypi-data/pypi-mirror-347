#!/usr/bin/env python3
import subprocess, sys, os, time, shutil, argparse

def run_command(cmd, check=True):
    try:
        result = subprocess.run(
            cmd, shell=True, check=check,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}\nError: {e.output}")
        raise

def ensure_venv_with_packages(venv_path):
    if not os.path.exists(f"{venv_path}/bin/yt-dlp") or not os.path.exists(f"{venv_path}/bin/flask"):
        print("Creating virtual environment and installing required packages…")
        run_command(f"python3 -m venv {venv_path}")
        run_command(f"{venv_path}/bin/pip install --upgrade pip yt-dlp flask")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("mullvad_account")
    parser.add_argument("--resolution")
    parser.add_argument("--extension")
    args = parser.parse_args()

    venv_path = "/opt/yt-dlp-mullvad/venv"
    ensure_venv_with_packages(venv_path)

    if not shutil.which("mullvad"):
        sys.exit("Mullvad CLI not found.")

    run_command(f"mullvad account login {args.mullvad_account}")
    run_command("mullvad connect")
    time.sleep(10)

    audio_exts = {"mp3","m4a","aac","wav","flac","opus","ogg"}
    if args.extension and args.extension in audio_exts:
        ytdlp_cmd = (
            f"{venv_path}/bin/yt-dlp -x --audio-format {args.extension} "
            f"--embed-metadata "
            f"--output '/root/%(title)s.%(ext)s' "
            f"--user-agent 'Mozilla/5.0' {args.url}"
        )
    else:
        filt = "bestvideo+bestaudio"
        if args.resolution:
            filt = f"bestvideo[height<={args.resolution}]+bestaudio/best[height<={args.resolution}]"
        merge = args.extension or "mp4"
        ytdlp_cmd = (
            f"{venv_path}/bin/yt-dlp -f '{filt}' --merge-output-format {merge} "
            f"--embed-thumbnail --embed-metadata "
            f"--output '/root/%(title)s.%(ext)s' "
            f"--user-agent 'Mozilla/5.0' {args.url}"
        )

    try:
        output = run_command(ytdlp_cmd)
        filename = None
        for line in output.splitlines():
            if line.startswith("[download]") and "Destination:" in line:
                filename = line.split("Destination: ")[1].strip(); break
            if "has already been downloaded" in line:
                start = line.find("] ")+2; end=line.find(" has"); filename=line[start:end].strip(); break
        if filename and os.path.exists(filename):
            print(f"DOWNLOADED_FILE:{filename}")
        else:
            print("Download failed: File not found")
    except subprocess.CalledProcessError as e:
        print(f"yt-dlp failed: {e.output}")

    run_command("mullvad disconnect")

if __name__ == "__main__":
    main()

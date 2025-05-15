#!/usr/bin/env python3
import subprocess, sys, os, time, shutil, argparse

def run_command(cmd, check=True):
    try:
        return subprocess.run(cmd, shell=True, check=check,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              text=True).stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}\n{e.output}", file=sys.stderr)
        raise

def ensure_venv_with_packages(path):
    if not os.path.exists(f"{path}/bin/yt-dlp"):
        print("Creating venv & installing deps…")
        run_command(f"python3 -m venv {path}")
        run_command(f"{path}/bin/pip install -U pip yt-dlp flask")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("url"); p.add_argument("mullvad_account")
    p.add_argument("--resolution"); p.add_argument("--extension")
    a = p.parse_args()

    venv = "/opt/yt-dlp-mullvad/venv"
    ensure_venv_with_packages(venv)

    if not shutil.which("mullvad"):
        sys.exit("Mullvad CLI not found")

    run_command(f"mullvad account login {a.mullvad_account}")
    run_command("mullvad connect"); time.sleep(10)

    audio = {"mp3","m4a","aac","wav","flac","opus","ogg"}
    if a.extension and a.extension in audio:
        ytdlp_cmd = (f"{venv}/bin/yt-dlp -x --audio-format {a.extension} "
                     f"--embed-metadata "
                     f"--output '/root/%(title)s.%(ext)s' "
                     f"--user-agent 'Mozilla/5.0' {a.url}")
    else:
        filt = "bestvideo+bestaudio"
        if a.resolution:
            filt = (f"bestvideo[height<={a.resolution}]"
                    f"+bestaudio/best[height<={a.resolution}]")
        merge = a.extension or "mp4"
        ytdlp_cmd = (f"{venv}/bin/yt-dlp -f '{filt}' --merge-output-format {merge} "
                     f"--embed-thumbnail --embed-metadata "
                     f"--output '/root/%(title)s.%(ext)s' "
                     f"--user-agent 'Mozilla/5.0' {a.url}")

    out = run_command(ytdlp_cmd)
    name = None
    for line in out.splitlines():
        if "Destination:" in line:
            name = line.split("Destination: ")[1].strip(); break
        if "has already been downloaded" in line:
            start=line.find("] ")+2; end=line.find(" has")
            name=line[start:end].strip(); break
    if name and os.path.exists(name):
        print(f"DOWNLOADED_FILE:{name}")
    else:
        print("Download failed: file not found")

    run_command("mullvad disconnect")

if __name__ == "__main__":
    main()

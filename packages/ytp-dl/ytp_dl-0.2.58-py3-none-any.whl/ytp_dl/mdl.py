#!/usr/bin/env python3
"""
Core downloader.

download(url, mullvad_account, resolution=None, extension=None) ➜ pathlib.Path
"""

import subprocess, sys, os, time, shutil
from pathlib import Path
from typing import Optional

def _run(cmd: str) -> str:
    return subprocess.check_output(cmd, shell=True, text=True).strip()

def _check():
    for prog in ("yt-dlp", "ffmpeg", "mullvad"):
        if shutil.which(prog) is None:
            sys.exit(f"{prog} not found – install it first.")

def download(url: str, mullvad_account: str,
             resolution: Optional[str] = None,
             extension: Optional[str] = None) -> Path:
    _check()
    _run(f"mullvad account login {mullvad_account}")
    _run("mullvad connect")
    time.sleep(5)

    audio_exts = {"mp3","m4a","aac","wav","flac","opus","ogg"}
    out_tpl = "%(title)s.%(ext)s"
    if extension and extension.lower() in audio_exts:
        cmd = (f"yt-dlp -x --audio-format {extension} --embed-metadata "
               f"--output '{out_tpl}' --user-agent 'Mozilla/5.0' {url}")
    else:
        fmt = "bestvideo+bestaudio"
        if resolution:
            fmt = (f"bestvideo[height<={resolution}]+bestaudio/"
                   f"best[height<={resolution}]")
        merge = extension or "mp4"
        cmd = (f"yt-dlp -f '{fmt}' --merge-output-format {merge} "
               f"--embed-thumbnail --embed-metadata "
               f"--output '{out_tpl}' --user-agent 'Mozilla/5.0' {url}")

    output = _run(cmd)
    _run("mullvad disconnect")

    fname = next(
        (l.split("Destination:")[1].strip() for l in output.splitlines()
         if "Destination:" in l),
        None
    )
    if not fname or not Path(fname).exists():
        raise RuntimeError("Download failed.")
    print(f"DOWNLOADED_FILE:{fname}", flush=True)
    return Path(fname).resolve()

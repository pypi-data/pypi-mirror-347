#!/usr/bin/env python3
"""
ytp-dl  – CLI client for ytp-dl API
"""
import requests, argparse, os, sys

CHUNK = 1024 * 64

def human(n):
    for u in ("B","KB","MB","GB"):
        if n < 1024: return f"{n:,.1f}{u}"
        n /= 1024
    return f"{n:.1f}TB"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--api", required=True,
                   help="Base URL, e.g. http://1.2.3.4:5000")
    p.add_argument("--mullvad", required=True,
                   help="16-digit Mullvad account number")
    p.add_argument("url")
    p.add_argument("--resolution")
    p.add_argument("--extension")
    a = p.parse_args()

    endpoint = a.api.rstrip("/") + "/api/download"
    payload  = {"url": a.url, "mullvad_account": a.mullvad}
    if a.resolution: payload["resolution"] = a.resolution
    if a.extension:  payload["extension"]  = a.extension

    with requests.post(endpoint, json=payload, stream=True) as r:
        if r.status_code != 200:
            print("Error:", r.text); sys.exit(1)

        cd = r.headers.get("Content-Disposition", "")
        fname = cd.split("filename=")[1].strip('"') if "filename=" in cd else "download"
        if os.path.exists(fname):
            print("File exists – abort."); sys.exit(0)

        total = int(r.headers.get("Content-Length", 0)); done = 0
        with open(fname, "wb") as f:
            for chunk in r.iter_content(chunk_size=CHUNK):
                if chunk:
                    f.write(chunk); done += len(chunk)
                    if total:
                        pct=done/total*100; bar=int(pct//2)*"█"
                        sys.stdout.write(f"\r[{bar:<50}] {pct:6.2f}% "
                                         f"{human(done)}/{human(total)}")
                    else:
                        sys.stdout.write(f"\rDownloaded {human(done)}")
                    sys.stdout.flush()
        print(f"\nSaved → {fname}")

if __name__ == "__main__":
    main()

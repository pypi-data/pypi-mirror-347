# Not exposed to users, but handy for debugging
if __name__ == "__main__":
    from .mdl import download
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("mullvad")
    p.add_argument("--resolution")
    p.add_argument("--extension")
    a = p.parse_args()
    download(a.url, a.mullvad, a.resolution, a.extension)

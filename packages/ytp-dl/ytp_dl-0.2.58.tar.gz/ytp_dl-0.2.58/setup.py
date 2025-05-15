from setuptools import setup, find_packages

setup(
    name="ytp-dl",                # <‑‑ final PyPI name
    version="0.2.58",
    description="YouTube downloader (yt‑dlp) routed through Mullvad VPN",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="dumgum82",
    author_email="dumgum42@gmail.com",
    license="MIT",
    packages=find_packages(),     # finds ytp_dl
    python_requires=">=3.8",
    install_requires=[
        "yt-dlp>=2024.4",
        "flask>=3.0",
        "requests>=2.32"
    ],
    entry_points={
        "console_scripts": [
            "ytp-dl-api = ytp_dl.api:main"   # only API server is exposed
        ],
    },
)

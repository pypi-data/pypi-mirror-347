from setuptools import setup, find_packages

setup(
    name="ytp-dl",
    version="0.2.62",
    description="yt-dlp + Mullvad VPN downloader (API server + CLI client)",
    author="dumgum82",
    author_email="dumgum42@gmail.com",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "yt-dlp>=2024.4",
        "flask>=3.0",
        "requests>=2.32"
    ],
    entry_points={
        "console_scripts": [
            "ytp-dl-api = ytp_dl.api:main",     # server
            "ytp-dl     = ytp_dl.client:main",  # client
        ],
    },
)

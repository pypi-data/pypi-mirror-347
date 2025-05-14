from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ytp-dl',
    version='0.2.5',
    packages=find_packages(),
    install_requires=['yt-dlp', 'flask'],
    entry_points={
        'console_scripts': [
            'ytp-dl = ytp_dl.mdl:main',
            'ytp-dl-api = ytp_dl.api:main',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
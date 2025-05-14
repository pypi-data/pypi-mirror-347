from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ytp-dl',
    version='0.2.54',  # Update this for each release
    packages=find_packages(),
    install_requires=['yt-dlp', 'flask'],
    entry_points={
        'console_scripts': [
            'ytp-dl = ytp_dl.mdl:main',
            'ytp-dl-api = ytp_dl.api:main',
        ],
    },
    author='dumgum82',  # Replace with your name
    author_email='dumgum42@gmail.com',  # Replace with your email
    description='A YouTube downloader with Mullvad VPN and Flask API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust as needed
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
)
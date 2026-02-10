# TouYube Downloader
Batch downloader with automatic metadata embedding. Downloads audio using yt-dlp, converts it to MP3, and embeds title, artist, year, and album cover via FFmpeg based on video metadata. Supports batch processing from a text file of URLs.

This script downloads audio from YouTube links, converts it to MP3, and automatically embeds metadata (title, artist, year, and cover image) using yt-dlp and FFmpeg.

It supports batch downloading from a text file.



## Requirements

Make sure you have the following installed:

- Python 3.8+
- FFmpeg
- yt-dlp

### Install Dependencies

#### Python dependency
```bash
pip install yt-dlp

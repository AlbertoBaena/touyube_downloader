# TouYube Downloader

Batch downloader that converts YouTube videos to MP3 and automatically adds title, artist, year, and cover image using yt-dlp and FFmpeg.

Supports downloading multiple links from a text file.

## Requirements

Install the following:

- Python 3.8+
- FFmpeg
- yt-dlp

### Install yt-dlp
```bash
pip install yt-dlp
```

### Install FFmpeg

**Linux**

```bash
sudo apt install ffmpeg
```

**Windows / macOS**

Download from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

Make sure FFmpeg is added to PATH.

## Quick Start (For Dummies)

### 1. Create a Links File

Create a file called `links.txt`.

Inside it, put one YouTube link per line:

```txt
https://www.youtube.com/watch?v=xxxx
https://www.youtube.com/watch?v=yyyy
```

Save the file.

### 2. Run the Script

Open a terminal in the project folder and run:

```bash
python download_mp3.py links.txt
```

### 3. Get Your Music

Your MP3 files will appear in:

```txt
mp3_downloads/
```

Each file includes:

* Song title
* Artist
* Year
* Cover image

## Copy to Phone (Optional Scripts)

Helper scripts are included to copy music to your phone.

Useful if you sync music often.

### Requirements

* USB cable
* Phone in File Transfer (MTP) mode
* ADB (for some scripts)

Install ADB (Linux):

```bash
sudo apt install adb
```

---

### Usage

1. Connect your phone via USB
2. Enable File Transfer mode
3. Run:

```bash
python copy_to_phone.py
```

(or the provided script)

MP3 files will be copied to your phone’s Music folder.

## Troubleshooting

### FFmpeg Not Found

Check:

```bash
ffmpeg -version
```

If it fails, reinstall FFmpeg.

### Download Fails

Some videos may be blocked or unavailable. They will be skipped.

## Notes

* Playlists are disabled
* Existing files are overwritten
* Temporary files are deleted automatically

## License

Use responsibly and respect copyright laws.

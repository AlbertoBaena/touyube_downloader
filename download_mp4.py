import os
import sys
import json
import shutil
import subprocess
import yt_dlp

def download_mp4(url, destination_folder="mp4_downloads"):
    os.makedirs(destination_folder, exist_ok=True)

    options = {
        'extractor_args': {'youtube': {'player_client': ['android']}},
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080][ext=mp4]/best[height<=1080]/best',
        'hls_prefer_native': True,
        'allow_unplayable_formats': False,
        'force_generic_extractor': False,
        'no_check_certificate': True,
        'ignoreerrors': True,
        'outtmpl': os.path.join(destination_folder, '%(title)s.%(ext)s'),
        'quiet': False,
        'noplaylist': True,
        'concurrent_fragment_downloads': 1,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'writesubtitles': False,
        'writeautomaticsub': False,
        'writethumbnail': False,
        'writeinfojson': False,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            if info:
                output_file = ydl.prepare_filename(info)
                if os.path.exists(output_file):
                    mp4_file = output_file
                else:
                    mp4_file = os.path.splitext(output_file)[0] + ".mp4"
                    if not os.path.exists(mp4_file):
                        webm_file = os.path.splitext(output_file)[0] + ".webm"
                        if os.path.exists(webm_file):
                            mp4_file = webm_file
                        else:
                            print("⚠️ Video file not found:", output_file)
                            return
                
                if not os.path.exists(mp4_file):
                    print("⚠️ Video file not found:", mp4_file)
        except Exception as e:
            print(f"❌ Error at downloading {url}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Use: python download_mp4.py links.txt")
        return

    file = sys.argv[1]

    if not os.path.isfile(file):
        print(f"The file {file} doesn't exist.")
        return

    with open(file, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]

    for link in links:
        print(f"\n⬇️ Downloading: {link}")
        download_mp4(link)

if __name__ == "__main__":
    main()
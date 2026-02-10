import os
import sys
import json
import shutil
import subprocess
import yt_dlp

def embed_metadata(mp3_path, url, destination_folder):
    base_name = os.path.splitext(os.path.basename(mp3_path))[0]
    temp_dir = os.path.join(destination_folder, "temp_" + base_name)
    os.makedirs(temp_dir, exist_ok=True)

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writeinfojson': True,
        'writethumbnail': True,
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"❌ Error at obtaining metadata of {url}: {e}")
        return

    files = os.listdir(temp_dir)
    thumb_file = next((f for f in files if f.lower().endswith(('.jpg', '.webp', '.png'))), None)
    json_file = next((f for f in files if f.lower().endswith('.info.json')), None)

    if not thumb_file or not json_file:
        print("⚠️ Thumbnail or metadata not found for:", mp3_path)
        return

    path_thumb = os.path.join(temp_dir, thumb_file)
    path_json = os.path.join(temp_dir, json_file)

    with open(path_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    title = data.get('title', base_name)
    artist = data.get('uploader', '')
    date = data.get('upload_date', '')
    year = date[:4] if date else ''

    temp_output = mp3_path + ".temp.mp3"

    # FFMPEG options
    command = [
        "ffmpeg", "-y",
        "-i", mp3_path,
        "-i", path_thumb,
        "-map", "0:a",
        "-map", "1",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-id3v2_version", "3",
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        "-metadata", f"date={year}",
        "-metadata:s:v", "title=Album cover",
        "-metadata:s:v", "comment=Cover (front)",
        temp_output
    ]

    try:
        subprocess.run(command, check=True)
        shutil.move(temp_output, mp3_path)
        print(f"✅ Added metadata: {os.path.basename(mp3_path)}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error at adding metadata: {e}")
        if os.path.exists(temp_output):
            os.remove(temp_output)

    shutil.rmtree(temp_dir, ignore_errors=True)

def download_mp3(url, destination_folder="mp3_downloads"):
    os.makedirs(destination_folder, exist_ok=True)

    options = {
        'extractor_args': {'youtube': {'player_client': ['android']}},
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'hls_prefer_native': True,
        'allow_unplayable_formats': False,
        'force_generic_extractor': False,
        'no_check_certificate': True,
        'ignoreerrors': True,
        'outtmpl': os.path.join(destination_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'noplaylist': True,
        'concurrent_fragment_downloads': 1,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            if info:
                output_file = ydl.prepare_filename(info)
                mp3_file = os.path.splitext(output_file)[0] + ".mp3"
                if os.path.exists(mp3_file):
                    embed_metadata(mp3_file, url, destination_folder)
                else:
                    print("⚠️ .mp3 file not found:", mp3_file)
        except Exception as e:
            print(f"❌ Error at downloading {url}: {e}")


def main():
    if len(sys.argv) != 2:
        print("Use: python download_mp3.py links.txt")
        return

    file = sys.argv[1]

    if not os.path.isfile(file):
        print(f"The file {file} doesn't exist.")
        return

    with open(file, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]

    for link in links:
        print(f"\n⬇️ Downloading: {link}")
        download_mp3(link)

if __name__ == "__main__":
    main()

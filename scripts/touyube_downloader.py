import os
import sys
import json
import shutil
import subprocess
import importlib

def import_or_install(package_name):
    try:
        module = importlib.import_module(package_name)
        return module
    except ImportError:
        print(f"{package_name} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name.replace('_', '-')])
        return importlib.import_module(package_name)

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
        print(f"Error at obtaining metadata of {url}: {e}")
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
        print(f"Added metadata: {os.path.basename(mp3_path)}")
    except subprocess.CalledProcessError as e:
        print(f"Error at adding metadata: {e}")
        if os.path.exists(temp_output):
            os.remove(temp_output)

    shutil.rmtree(temp_dir, ignore_errors=True)

def download_mp3(url, destination_folder):
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

def download_mp4(url, destination_folder):
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
    # Import YT-DLP and FFMPEG
    global yt_dlp, ffmpeg
    yt_dlp = import_or_install("yt_dlp")
    ffmpeg = import_or_install("ffmpeg")

    # Check arguments
    if len(sys.argv) < 4:
        print("Use: python touyoube_downloader.py format links_file output_folder")
        return

    format = sys.argv[1].lower()
    links_file = sys.argv[2]
    destination_folder = sys.argv[3]

    if not os.path.isfile(links_file):
        print(f"The file {links_file} doesn't exist.")
        return

    with open(links_file, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]

    # Download
    if(format == "mp3"):
        print(f"MP3 DOWNLOAD\n")
        for link in links:
            print(f"\nDownloading: {link}")
            download_mp3(link, destination_folder)
    elif(format == "mp4"):
        print(f"MP4 DOWNLOAD\n")
        for link in links:
                print(f"\nDownloading: {link}")
                download_mp4(link, destination_folder)
    else:
        print("Error: format must be either mp3 or mp4")
        return
    
    return


if __name__ == "__main__":
    main()

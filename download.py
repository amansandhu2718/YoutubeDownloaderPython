

from yt_dlp import YoutubeDL
import string
import os

def get_playlist_videos(playlist_url):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        if "entries" in info:
            return [(entry["url"], entry["title"]) for entry in info["entries"] if "url" in entry and "title" in entry]
    return []

def get_alphabet_prefix(index):
    """ Converts an index to an alphabetical sequence like A, B, ..., Z, AA, AB, ..., ZZ, AAA """
    prefix = ""
    while index >= 0:
        prefix = string.ascii_uppercase[index % 26] + prefix
        index = (index // 26) - 1
    return prefix

def download_videos(video_data, output_folder="DownloadsLevel1", quality="bestvideo[height=1080]+bestaudio/best"):
    quality = "bv*[height<=1080]+ba/b"  # Tries 1080p, falls back to lower resolutions if unavailable
    ydl_opts = {
        "format": quality,  # Select 1080p video + best audio
        "merge_output_format": "mp4",  # Ensure proper merging
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4"
            }
        ],
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s")  # Correct output pattern
    }

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    total_videos = len(video_data)
    print(f"Total videos found: {total_videos}")

    for index, (url, title) in enumerate(video_data):
        prefix = get_alphabet_prefix(index)  # Generate unique prefix
        safe_title = "".join(c for c in title if c.isalnum() or c in " -_")  # Remove special characters
        filename = f"{prefix} - {safe_title}.mp4"
        filepath = os.path.join(output_folder, filename)

        # Check if file already exists
        if os.path.exists(filepath):
            print(f"Skipping {filename} (Already downloaded)")
            continue

        ydl_opts["outtmpl"] = filepath  # Set the correct output template

        print(f"Downloading {filename}...")

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

# Replace with your playlist link
# playlist_url = "https://www.youtube.com/playlist?list=PL-Jc9J83PIiE-181crLG1xSIWhTGKFiMY"
playlist_url=""

# Step 1: Get all video links
videos = get_playlist_videos(playlist_url)

# Step 2: Download all videos in 1080p with unique alphabetical prefixes, skipping existing ones
if videos:
    download_videos(videos)
else:
    print("No videos found in the playlist.")

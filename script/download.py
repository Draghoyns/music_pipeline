import subprocess
from pathlib import Path

from constant import (
    OUTPUT_DIR,
    PLAYLIST_URL,
    FORMAT,
    BIT_RATE,
    AUDIO_PROVIDERS,
    MAX_METADATA_RETRIES,
    DOWNLOAD_THREADS,
    YT_DLP_ARGS,
)


def download_playlist():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    command = [
        "uv",
        "run",
        "spotdl",
        "download",
        PLAYLIST_URL,
        "--output",
        OUTPUT_DIR,
        "--format",
        FORMAT,
        "--bitrate",
        BIT_RATE,
        "--threads",
        DOWNLOAD_THREADS,
        "--max-retries",
        MAX_METADATA_RETRIES,
        "--audio",
        *AUDIO_PROVIDERS,
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        subprocess.run([*command, "--yt-dlp-args", YT_DLP_ARGS], check=True)


if __name__ == "__main__":
    print("Starting the download of the playlist...\n---\n")
    download_playlist()
    print("\n---\nDownload completed.")

import subprocess
from pathlib import Path
from constant import OUTPUT_DIR, PLAYLIST_URL, FORMAT, BIT_RATE


def download_playlist():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
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
            "4",
        ]
    )


if __name__ == "__main__":
    print("Starting the download of the playlist...\n---\n")
    download_playlist()
    print("\n---\nDownload completed.")

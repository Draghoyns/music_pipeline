import subprocess
import sys
from pathlib import Path

# Allow running this file directly without requiring manual PYTHONPATH tweaks.
if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

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

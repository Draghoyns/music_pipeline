import os
import sys
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

# Allow running this file directly without requiring manual PYTHONPATH tweaks.
if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from constant import OUTPUT_DIR


def clean_metadata(file_path: Path):
    """
    Cleans the metadata for all downloaded audio files in the OUTPUT_DIR.
    """
    audio = MP3(file_path, ID3=EasyID3)

    artist = audio.get("artist")
    title = audio.get("title")

    # Remove all existing tags
    audio.delete()

    # Set the cleaned metadata
    audio["artist"] = artist
    audio["title"] = title

    # Save the changes
    audio.save()


def rename_file(file_path: Path):
    """
    Renames the title metadata for all downloaded audio files in the OUTPUT_DIR.
    """
    audio = MP3(file_path, ID3=EasyID3)

    title = audio.get("title")

    if not title:
        print(f"No title metadata found for {file_path}. Skipping rename.")
        return

    # Rename the file based on the title metadata
    new_file_name = f"{title[0]}.mp3"
    new_file_path = file_path.parent / new_file_name

    # Rename the file
    file_path.rename(new_file_path)


def main():
    """
    Main function to set artist and rename title metadata for downloaded audio files.
    """
    print("Starting the cleaning of metadata for downloaded audio files...\n---\n")
    for file_name in os.listdir(OUTPUT_DIR):
        if file_name.endswith(".mp3"):
            file_path = Path(os.path.join(OUTPUT_DIR, file_name))
            clean_metadata(file_path)
            rename_file(file_path)
    print("\n---\nMetadata cleaning completed.")


if __name__ == "__main__":
    main()

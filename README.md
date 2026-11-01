# Music Pipeline

A Python pipeline to download a Spotify playlist as MP3 files with clean metadata. It fetches each track from YouTube (via `spotdl`), converts to 128 kbps MP3, strips all non-essential ID3 tags, and renames each file to its track title.

# Installation and requirements

This project uses `uv`. Run `uv sync` to install dependencies.

Install the `just` command (better version of `make`).

# Pipeline

## Step 1

Set the constants in `constant.py`. The most important one is `PLAYLIST_URL`.
The others can be customized as you want.

## Step 2

Run `just download`. It downloads the mp3 files in the set output directory (default `output/`).

## Step 3 (optional)

This step is manual. If you want to clip and remove intros / outros, feel free to do so here.
This can be done [here](https://audiotrimmer.com/) for example.

## Step 4

Run `just rename`. It cleans all the metadata and only sets `artist` and `title`. It renames the file to `<title>.mp3`. Just be careful if you have songs with the same title.

## Step 5

Verify that everything went well. Chnage anything manually if it semes relevant to you !

Then move the tracks into your backup playlist (e.g. in Spotify, select all the tracks of the source playlist, then right-click > Add to playlist).

And that's it :star:



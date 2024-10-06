# YouTube Video Downloader (Mac Desktop Application)

This application is a YouTube video downloader built with Python, using `yt-dlp` and `ffmpeg` for downloading videos and converting formats. The graphical interface is created using `Tkinter` to make it easy for users to download YouTube videos by simply pasting the video URL, selecting the quality, and choosing the download location.

## Features

- Download videos from YouTube by providing the video URL.
- Select desired video quality (default: best available).
- Choose the download location for the video file.
- Progress bar showing the download progress.
- Multi-threaded to avoid freezing the UI during downloads.

## Prerequisites
- **FFmpeg**: This application requires `ffmpeg` for video conversion. To install `ffmpeg`, use the following command:
  ```bash
  brew install ffmpeg

## Run the app
Run the build command(in build_cmd.txt) in the terminal. This will create a dist/ , build/ dirs and YT_Download.spec. The executable app will be in dist dir

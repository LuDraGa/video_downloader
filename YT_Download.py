import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import yt_dlp
import os
import sys
import threading

def get_ffmpeg_path():
    ffmpeg_executable = 'ffmpeg'
    if sys.platform == 'win32':
        ffmpeg_executable += '.exe'

    if getattr(sys, 'frozen', False):
        ffmpeg_dir = sys._MEIPASS
    else:
        ffmpeg_dir = os.path.dirname(os.path.abspath(__file__))

    ffmpeg_path = os.path.join(ffmpeg_dir, 'ffmpeg', ffmpeg_executable)
    return ffmpeg_path

def download_success():
    # Re-enable the download button and reset its text
    download_button.config(state=tk.NORMAL, text="Download")
    messagebox.showinfo("Success", f"Successfully downloaded video to {save_path}")

def download_failure(error_message):
    # Re-enable the download button and reset its text
    download_button.config(state=tk.NORMAL, text="Download")
    progress_var.set(0)  # Reset progress bar on error
    messagebox.showerror("Error", f"Failed to download the video.\n{error_message}")

def download_video():
    global save_path
    url = url_entry.get().strip()
    quality = quality_var.get()
    save_path = save_path_var.get().strip()

    if not url or not save_path:
        messagebox.showerror("Error", "Please enter a URL and select a save location.")
        return

    # Remove any existing extension from the save path
    base, ext = os.path.splitext(save_path)
    save_path = base

    # Disable the download button and change its text
    download_button.config(state=tk.DISABLED, text="Downloading...")
    
    status_var.set("Starting download...")
    progress_var.set(0)  # Reset the progress bar

    def progress_hook(d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            if total > 0:
                percent = downloaded / total * 100
                progress_var.set(percent)
                status_var.set(f"Downloading... {percent:.1f}%")
        elif d['status'] == 'finished':
            progress_var.set(100)
            status_var.set("Download finished.")

    ffmpeg_path = get_ffmpeg_path()

    ydl_opts = {
        'outtmpl': save_path + '.%(ext)s',
        'format': quality,
        'ffmpeg_location': ffmpeg_path,
        'progress_hooks': [progress_hook],
    }

    def run_download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            # Schedule success message on main thread
            root.after(0, download_success)
        except Exception as e:
            # Schedule failure message on main thread
            root.after(0, download_failure, str(e))

    threading.Thread(target=run_download).start()

def select_save_location():
    file_types = [("All files", "*.*")]
    file_path = filedialog.asksaveasfilename(defaultextension="",
                                             filetypes=file_types,
                                             title="Choose save location")
    if file_path:
        save_path_var.set(file_path)

def create_main_window():
    global root, url_entry, save_path_var, quality_var, download_button, progress_var, status_var
    # Create the main application window
    root = tk.Tk()
    root.title("YouTube Video Downloader")
    root.geometry("600x400")
    root.resizable(True, True)
    try:
        root.iconbitmap('app_icon.ico')  # Set the window icon
    except Exception:
        pass  # Ignore if icon is not found or unsupported

    # URL input
    url_label = tk.Label(root, text="Enter video URL:")
    url_label.pack(pady=(20, 5))
    url_entry = tk.Entry(root, width=60)
    url_entry.pack(pady=5, padx=10, fill=tk.X, expand=True)

    # Save location
    save_label = tk.Label(root, text="Save location:")
    save_label.pack(pady=5)

    save_frame = tk.Frame(root)
    save_frame.pack(pady=5, padx=10, fill=tk.X, expand=True)

    save_path_var = tk.StringVar()
    save_entry = tk.Entry(save_frame, textvariable=save_path_var, width=50)
    save_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

    browse_button = tk.Button(save_frame, text="Browse", command=select_save_location, width=10)
    browse_button.pack(side=tk.LEFT)

    # Quality selection
    quality_label = tk.Label(root, text="Select video quality:")
    quality_label.pack(pady=5)

    quality_var = tk.StringVar(value='bestvideo+bestaudio/best')
    
    # Download button
    download_button = tk.Button(root, text="Download", command=download_video, width=20)
    download_button.pack(pady=20)

    # Progress bar
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.pack(pady=10, fill=tk.X, padx=20, expand=True)

    # Status label
    status_var = tk.StringVar()
    status_label = tk.Label(root, textvariable=status_var, fg="green")
    status_label.pack(pady=5)

    return root

if __name__ == "__main__":
    try:
        root = create_main_window()
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Critical Error", f"An unexpected error occurred: {str(e)}")

import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser  # <-- Added for the hyperlink

try:
    import imageio_ffmpeg
except ImportError:
    messagebox.showerror("Missing Library", "Please run: pip install imageio-ffmpeg")
    exit()

class VideoMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video & Audio Merger")
        self.root.geometry("650x360")  # Made slightly taller to fit the footer
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')

        self.video_path = tk.StringVar()
        self.audio_path = tk.StringVar()
        self.output_path = tk.StringVar()

        # --- UI Elements ---
        ttk.Label(root, text="Video File (MP4):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(root, textvariable=self.video_path, width=50).grid(row=0, column=1, padx=5, pady=10)
        ttk.Button(root, text="Browse", command=self.select_video).grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(root, text="Audio File (MP4/M4A):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(root, textvariable=self.audio_path, width=50).grid(row=1, column=1, padx=5, pady=10)
        ttk.Button(root, text="Browse", command=self.select_audio).grid(row=1, column=2, padx=10, pady=10)

        ttk.Label(root, text="Save As:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(root, textvariable=self.output_path, width=50).grid(row=2, column=1, padx=5, pady=10)
        ttk.Button(root, text="Browse", command=self.select_output).grid(row=2, column=2, padx=10, pady=10)

        self.merge_btn = ttk.Button(root, text="▶ MERGE VIDEO & AUDIO", command=self.start_merge)
        self.merge_btn.grid(row=3, column=0, columnspan=3, pady=20, ipadx=20, ipady=10)

        self.status_label = ttk.Label(root, text="Ready.", foreground="blue")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)

        # --- Footer Section ---
        footer_frame = tk.Frame(root)
        footer_frame.grid(row=5, column=0, columnspan=3, pady=(15, 10))  # Add some padding at the bottom

        # "Created by " label
        tk.Label(footer_frame, text="Created by ", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # "Sibany.com" hyperlink label
        link_label = tk.Label(footer_frame, text="Sibany.com", font=("Arial", 9, "underline"), fg="blue", cursor="hand2")
        link_label.pack(side=tk.LEFT)
        
        # Bind the click event to open the web browser
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://sibany.com"))

        # Get the FFmpeg executable path from the imageio-ffmpeg package
        try:
            self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception as e:
            self.ffmpeg_exe = None
            messagebox.showerror("Error", f"Could not load FFmpeg from imageio-ffmpeg.\n{e}")

    def select_video(self):
        path = filedialog.askopenfilename(title="Select Video File", filetypes=[("MP4 Video", "*.mp4"), ("All Files", "*.*")])
        if path:
            self.video_path.set(path)
            if not self.output_path.get():
                dir_name = os.path.dirname(path)
                base_name = os.path.splitext(os.path.basename(path))[0]
                self.output_path.set(os.path.join(dir_name, f"{base_name}_merged.mp4"))

    def select_audio(self):
        path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("MP4 Audio", "*.mp4"), ("M4A Audio", "*.m4a"), ("All Files", "*.*")])
        if path:
            self.audio_path.set(path)

    def select_output(self):
        path = filedialog.asksaveasfilename(title="Save Merged File As", defaultextension=".mp4", filetypes=[("MP4 Video", "*.mp4")])
        if path:
            self.output_path.set(path)

    def start_merge(self):
        video = self.video_path.get()
        audio = self.audio_path.get()
        output = self.output_path.get()

        if not video or not audio or not output:
            messagebox.showwarning("Missing Information", "Please select both a video and audio file, and specify an output location.")
            return
        if not os.path.exists(video):
            messagebox.showerror("Error", "The selected video file does not exist.")
            return
        if not os.path.exists(audio):
            messagebox.showerror("Error", "The selected audio file does not exist.")
            return
        if not self.ffmpeg_exe:
            messagebox.showerror("Error", "FFmpeg is not available. Please run 'pip install imageio-ffmpeg' in your terminal.")
            return

        self.merge_btn.config(state="disabled")
        self.status_label.config(text="Merging... Please wait.", foreground="orange")

        threading.Thread(target=self.run_ffmpeg, args=(video, audio, output), daemon=True).start()

    def run_ffmpeg(self, video, audio, output):
        # We use the exact path to the FFmpeg executable provided by imageio-ffmpeg
        cmd = [
            self.ffmpeg_exe,
            "-y", 
            "-i", video, 
            "-i", audio, 
            "-c", "copy", 
            output
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.root.after(0, self.merge_success, output)
        except subprocess.CalledProcessError as e:
            self.root.after(0, self.merge_error, e.stderr)
        except Exception as e:
            self.root.after(0, self.merge_error, str(e))

    def merge_success(self, output):
        self.merge_btn.config(state="normal")
        self.status_label.config(text="✅ Merge Completed Successfully!", foreground="green")
        messagebox.showinfo("Success", f"Video and audio merged successfully!\n\nSaved to:\n{output}")

    def merge_error(self, error_msg):
        self.merge_btn.config(state="normal")
        self.status_label.config(text="❌ Merge Failed.", foreground="red")
        messagebox.showerror("Error", f"An error occurred during merging:\n\n{error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoMergerApp(root)
    root.mainloop()

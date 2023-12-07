import tkinter as tk
import customtkinter as ctk
import threading
import queue
from tkinter import messagebox
from dialogs import DialogFactory
from downloader import SpotifyDownloader

CLIENT_ID = "23b7b90282474e83bcf575d878363856"
CLIENT_SECRET = "761fa77077e74c959e84d4c6cf6b5426"


class SpotifyDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spotify Playlist Downloader")
        self.geometry("720x480")
        self.create_widgets()
        self.spotify_downloader = SpotifyDownloader(CLIENT_ID, CLIENT_SECRET)
        self.queue = queue.Queue()

    def create_widgets(self):
        ctk.CTkLabel(self, text="URL da Playlist Spotify").pack()
        self.url_entry = ctk.CTkEntry(self, width=400)
        self.url_entry.pack()

        ctk.CTkLabel(self, text="Diretório de Saída").pack()
        self.output_dir_entry = ctk.CTkEntry(self, width=400)
        self.output_dir_entry.pack()
        ctk.CTkButton(self, text="Navegar", command=self.browse_folder).pack()

        ctk.CTkLabel(self, text="Região").pack()
        self.region_entry = ctk.CTkEntry(self, width=400)
        self.region_entry.pack()

        ctk.CTkButton(self, text="Download", command=self.start_download).pack()

        self.progress_label = tk.Label(self, text="")
        self.progress_label.pack()

    def browse_folder(self):
        dialog = DialogFactory.create_folder_dialog(self)
        self.wait_window(dialog)
        if dialog.folder_path:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, dialog.folder_path)

    def start_download(self):
        playlist_url = self.url_entry.get()
        output_dir = self.output_dir_entry.get()
        region = self.region_entry.get()

        if not playlist_url or not output_dir or not region:
            messagebox.showwarning("Aviso", "Todos os campos são necessários!")
            return

        threading.Thread(
            target=self.download_playlist,
            args=(playlist_url, output_dir, region),
            daemon=True,
        ).start()

    def download_playlist(self, playlist_url, output_dir, region):
        self.spotify_downloader.download_playlist(
            playlist_url,
            output_dir,
            region,
            progress_callback=self.update_progress,
            error_callback=self.handle_error,
        )

    def update_progress(self, track):
        self.queue.put(lambda: self.progress_label.config(text=f"Baixando: {track}"))

    def handle_error(self, message):
        self.queue.put(lambda: messagebox.showinfo("Informação", message))

    def process_queue(self):
        while self.queue.qsize():
            try:
                callback = self.queue.get(0)
                callback()
            except queue.Empty:
                pass
        self.after(100, self.process_queue)


if __name__ == "__main__":
    app = SpotifyDownloaderApp()
    app.process_queue()
    app.mainloop()

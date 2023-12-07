import os
import tkinter as tk
import customtkinter as ctk
import threading
from dotenv import load_dotenv
from tkinter import messagebox, ttk, filedialog
from artifact.downloader import SpotifyDownloader

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

class SpotifyDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("gtmp3")
        self.geometry("720x480")
        self.create_widgets()
        self.spotify_downloader = SpotifyDownloader(CLIENT_ID, CLIENT_SECRET)
        self.author_label = tk.Label(self, text="by: gtagliani")
        self.author_label.place(relx=1.0, rely=1.0, x=-2, y=-2, anchor="se")


    def create_widgets(self):
        ctk.set_appearance_mode("light")

        self.create_labels_and_entries()
        self.create_buttons()
        self.create_progress_bar()

    def create_labels_and_entries(self):
        ctk.CTkLabel(self, text="URL da Playlist Spotify").pack()
        self.url_entry = ctk.CTkEntry(self, width=400)
        self.url_entry.pack(pady=10)

        ctk.CTkLabel(self, text="Diretório de Saída").pack()
        self.output_dir_entry = ctk.CTkEntry(self, width=400)
        self.output_dir_entry.pack(pady=10)

        # Botão para selecionar diretório
        self.select_dir_button = ctk.CTkButton(
            self, text="Selecionar Diretório", command=self.select_directory
        )
        self.select_dir_button.pack(pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, directory)

    def create_buttons(self):
        ctk.CTkButton(
            self,
            text="Download",
            command=self.start_download,
            fg_color="black",
            text_color="white",
            hover_color="green",
        ).pack(pady=10)

    def create_progress_bar(self):
        style = ttk.Style(self)
        style.theme_use("default")

        self.progress_label = ctk.CTkLabel(self, text="Pronto para iniciar o download.")
        self.progress_label.pack(pady=10)
        self.progress_label.pack_forget()  # Esconder inicialmente

        self.progress = ttk.Progressbar(
            self,
            style="green.Horizontal.TProgressbar",
            length=300,
            mode="determinate",
            maximum=100,
        )
        self.progress.pack(pady=10)
        self.progress.pack_forget()

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
        self.progress_label.configure(text="Preparando para baixar...")
        self.progress_label.pack()
        self.progress.pack()

    def download_playlist(self, playlist_url, output_dir, region):
        def progress_callback(track, progress, progress_bar):
            self.update_progress(track, progress, progress_bar)

        try:
            self.show_progress()
            self.spotify_downloader.download_playlist(
                playlist_url,
                output_dir,
                region,
                progress_callback=progress_callback,
                error_callback=self.handle_error,
                progress_bar=self.progress,
            )
        except Exception as e:
            self.handle_error(str(e))
            

    def update_progress(self, track, progress, progress_bar):
        self.progress_label.configure(text=f"Baixando: {track}")
        progress_bar["value"] = progress

    def handle_error(self, message):
        self.progress_label.pack_forget()
        self.progress.pack_forget()
        messagebox.showinfo("Informação", message)

    def show_progress(self):
        self.progress_label.pack()
        self.progress.pack()

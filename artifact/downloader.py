import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from tkinter import ttk
from artifact.core import (
    extract_playlist_id,
    get_spotify_tracks,
    search_youtube,
    convert_to_mp3,
)

class SpotifyDownloader:
    def __init__(self, client_id, client_secret):
        self.spotify_client = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(client_id, client_secret)
        )

    def download_playlist(
            self, playlist_url, output_dir, region, progress_callback, error_callback, progress_bar
        ):
            playlist_id = extract_playlist_id(playlist_url)
            if not playlist_id:
                error_callback("URL da playlist inválida.")
                return

            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            try:
                tracks = get_spotify_tracks(playlist_id, self.spotify_client)
                total_tracks = len(tracks)
                for index, track in enumerate(tracks):
                    # Atualizar a interface com o nome da música atual antes do download
                    progress = (index + 1) / total_tracks * 100
                    progress_callback(track, progress, progress_bar)

                    video_url = search_youtube(track)
                    if not video_url:
                        continue

                    yt = YouTube(video_url)
                    audio_stream = yt.streams.filter(
                        only_audio=True, file_extension="mp4"
                    ).first()
                    if not audio_stream:
                        continue

                    audio_path = audio_stream.download(output_path=output_dir)
                    convert_to_mp3(audio_path, output_dir)

                    # Chamar novamente o progress_callback após a conclusão do download
                    progress_callback(track, progress, progress_bar)

                error_callback("Download concluído.")
            except Exception as e:
                error_callback(str(e))

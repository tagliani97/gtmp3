import os
import spotipy
import re
import time
import click
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
from moviepy.editor import *
from youtube_search import YoutubeSearch

CLIENT_ID = ''
CLIENT_SECRET = ''

def extract_playlist_id_from_url(url):
    """
    Extract the playlist ID from a Spotify URL.
    
    :param url: Spotify playlist URL
    :return: Playlist ID or None if not found
    """
    match = re.search(r"playlist/([a-zA-Z0-9]+)", url)
    return match.group(1) if match else None

def get_tracks_from_playlist(playlist_id):
    """
    Get tracks from a specific playlist.
    
    :param playlist_id: ID of the Spotify playlist
    :return: List of track names and their artists
    """
    return [
        item['track']['name'] + " - " + item['track']['artists'][0]['name']
        for item in sp.playlist_tracks(playlist_id)['items']
    ]

def get_youtube_url(query, region):
    """
    Get the YouTube URL for a given song query.
    
    :param query: Song name to search for
    :param region: Language or region code (used to decide lyrics keyword)
    :return: YouTube URL or None if not found
    """
    search_type = "LYRICS" if "en" in region else "letra"
    search_results = YoutubeSearch(f"{query} {search_type}", max_results=1).to_dict()
    return "https://www.youtube.com" + search_results[0]['url_suffix'] if search_results else None

def convert_and_save_audio(audio_file_path, output_directory):
    """
    Convert an audio file to mp3 and save to a directory.
    
    :param audio_file_path: Path to the original audio file
    :param output_directory: Directory to save the converted audio file
    :return: Path to the converted mp3 file
    """
    mp3_file_path = os.path.join(output_directory, os.path.splitext(os.path.basename(audio_file_path))[0] + ".mp3")
    audio_clip = AudioFileClip(audio_file_path)
    audio_clip.write_audiofile(mp3_file_path)
    audio_clip.close()
    os.remove(audio_file_path)
    return mp3_file_path

def download_audio_by_name(track_name, output_directory, region):
    """
    Download audio from YouTube by track name.
    
    :param track_name: Name of the track to search and download
    :param output_directory: Directory to save the downloaded audio
    :param region: Language or region code
    """
    video_url = get_youtube_url(track_name, region)

    if not video_url:
        print(f"No video found for {track_name}")
        return

    time.sleep(3)
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
    if not audio_stream:
        print(f"No audio stream found for {track_name}")
        return

    audio_file_path = audio_stream.download(output_path=output_directory)
    convert_and_save_audio(audio_file_path, output_directory)
    print(f"Audio for '{track_name}' successfully downloaded and converted!")

@click.command()
@click.option("--region", prompt="Language")
@click.option("--output_directory", prompt="Output Directory Name", default="downloads")
@click.option("--url", prompt="Spotify Playlist URL")
def cli(url, output_directory, region):
    """
    Command-line interface to download tracks from a Spotify playlist from YouTube.
    """
    playlist_id = extract_playlist_id_from_url(url)
    
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        )
        validate_auth = sp.user_playlists('spotify')
    except Exception as e:
        raise(e)
    else:
        if playlist_id:
            if not os.path.exists(output_directory):
                os.mkdir(output_directory)

            tracks = get_tracks_from_playlist(playlist_id)
            for track_name in tracks:
                download_audio_by_name(track_name, output_directory, region)
        else:
            print("Unable to extract the playlist ID from the provided link.")

if __name__ == '__main__':
    cli()

import os
import re
from moviepy.editor import AudioFileClip
from youtube_search import YoutubeSearch


def extract_playlist_id(url):
    """Extract playlist ID from Spotify URL."""
    match = re.search(r"playlist/([a-zA-Z0-9]+)", url)
    return match.group(1) if match else None


def get_spotify_tracks(playlist_id, spotify_client):
    """Retrieve track names and artists from a Spotify playlist."""
    return [
        f"{item['track']['name']} - {item['track']['artists'][0]['name']}"
        for item in spotify_client.playlist_tracks(playlist_id)["items"]
    ]


def search_youtube(query, region):
    """Search for a YouTube URL based on a query."""
    search_type = "LYRICS" if "en" in region else "letra"
    results = YoutubeSearch(f"{query} {search_type}", max_results=1).to_dict()
    return f"https://www.youtube.com{results[0]['url_suffix']}" if results else None


def convert_to_mp3(audio_path, output_dir):
    """Convert an audio file to MP3 and save it to the output directory."""
    mp3_path = os.path.join(
        output_dir, os.path.splitext(os.path.basename(audio_path))[0] + ".mp3"
    )
    audio_clip = AudioFileClip(audio_path)
    audio_clip.write_audiofile(mp3_path)
    audio_clip.close()
    os.remove(audio_path)
    return mp3_path

import os
import re
import pytest
from artifact.core import extract_playlist_id, search_youtube, convert_to_mp3


def test_extract_playlist_id():
    url = "https://open.spotify.com/playlist/37i9dQZF1DX7QOv5kjbU68?si=a0a896395c644933"
    playlist_id = extract_playlist_id(url)
    assert playlist_id == "37i9dQZF1DX7QOv5kjbU68"

    invalid_url = "https://open.spotify.com/show/4rOoJ6Egrf8K2IrywzwOMk?si=c9f8598ef0ac4bdc"
    value_playlist = extract_playlist_id(invalid_url)
    assert value_playlist is None


def test_search_youtube():
    query = "Rich Flex"
    youtube_url = search_youtube(query)
    assert youtube_url is not None
    assert youtube_url.startswith("https://www.youtube.com/")


def test_convert_to_mp3(tmpdir):
    audio_path = "test_audio.wav"
    output_dir = tmpdir.mkdir("output")

    mp3_path = convert_to_mp3(audio_path, str(output_dir))
    assert os.path.exists(mp3_path)
    assert mp3_path.endswith(".mp3")


if __name__ == "__main__":
    pytest.main()

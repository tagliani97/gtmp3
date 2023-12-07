import pytest
from unittest.mock import Mock, patch
from artifact.main import SpotifyDownloaderApp

playlist = "https://open.spotify.com/playlist/37i9dQZF1DX7QOv5kjbU68?si=6209f2a1dfb24e74"
output = "C:\\Users\\gabri\\OneDrive\\Documentos\\gtmp3\\output_test\\"

@pytest.fixture
def app():
    app = SpotifyDownloaderApp()
    yield app
    app.destroy()

@pytest.fixture
def mock_spotify_downloader():
    with patch('artifact.main.SpotifyDownloader') as mock:
        yield mock

def test_initial_state(app):
    assert app.url_entry.get() == ""
    assert app.output_dir_entry.get() == ""
    assert app.region_entry.get() == ""

def test_input_url(app):
    test_url = playlist
    app.url_entry.insert(0, test_url)
    assert app.url_entry.get() == test_url

def test_input_output_dir(app):
    test_dir = output
    app.output_dir_entry.insert(0, test_dir)
    assert app.output_dir_entry.get() == test_dir

def test_input_region(app):
    test_region = region
    app.region_entry.insert(0, test_region)
    assert app.region_entry.get() == test_region

def test_start_download(mock_spotify_downloader, app):
    app.url_entry.insert(0, playlist)
    app.output_dir_entry.insert(0, output)
    app.region_entry.insert(0, region)

    app.start_download()
    mock_spotify_downloader.return_value.download_playlist.assert_called_once_with(
        playlist, output, region, progress_callback=app.update_progress, error_callback=app.handle_error)
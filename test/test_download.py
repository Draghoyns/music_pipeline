from unittest.mock import patch, call

from script.download import download_playlist
from constant import OUTPUT_DIR, PLAYLIST_URL, FORMAT, BIT_RATE


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_creates_output_dir(mock_path_cls, mock_run):
    download_playlist()

    mock_path_cls.assert_called_once_with(OUTPUT_DIR)
    mock_path_cls.return_value.mkdir.assert_called_once_with(
        parents=True, exist_ok=True
    )


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_runs_subprocess(mock_path_cls, mock_run):
    download_playlist()

    mock_run.assert_called_once()


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_command_starts_with_uv_run_spotdl(mock_path_cls, mock_run):
    download_playlist()

    cmd = mock_run.call_args[0][0]
    assert cmd[:4] == ["uv", "run", "spotdl", "download"]


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_command_includes_playlist_url(mock_path_cls, mock_run):
    download_playlist()

    cmd = mock_run.call_args[0][0]
    assert PLAYLIST_URL in cmd


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_command_includes_output_dir(mock_path_cls, mock_run):
    download_playlist()

    cmd = mock_run.call_args[0][0]
    assert "--output" in cmd
    assert OUTPUT_DIR in cmd


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_command_includes_format(mock_path_cls, mock_run):
    download_playlist()

    cmd = mock_run.call_args[0][0]
    assert "--format" in cmd
    assert FORMAT in cmd


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_command_includes_bitrate(mock_path_cls, mock_run):
    download_playlist()

    cmd = mock_run.call_args[0][0]
    assert "--bitrate" in cmd
    assert BIT_RATE in cmd


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_command_includes_threads(mock_path_cls, mock_run):
    download_playlist()

    cmd = mock_run.call_args[0][0]
    assert "--threads" in cmd
    assert "4" in cmd

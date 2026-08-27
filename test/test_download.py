import subprocess
from unittest.mock import patch

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


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_command_includes_max_retries(mock_path_cls, mock_run):
    download_playlist()

    cmd = mock_run.call_args[0][0]
    assert "--max-retries" in cmd
    assert "5" in cmd


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_command_includes_audio_provider_fallbacks(
    mock_path_cls, mock_run
):
    download_playlist()

    cmd = mock_run.call_args[0][0]
    audio_index = cmd.index("--audio")
    assert cmd[audio_index + 1 : audio_index + 3] == ["youtube", "youtube-music"]


@patch("script.download.subprocess.run")
@patch("script.download.Path")
def test_download_playlist_uses_android_profile_after_failure(mock_path_cls, mock_run):
    mock_run.side_effect = [subprocess.CalledProcessError(1, "spotdl"), None]

    download_playlist()

    normal_cmd = mock_run.call_args_list[0].args[0]
    fallback_cmd = mock_run.call_args_list[1].args[0]
    assert "--yt-dlp-args" not in normal_cmd
    assert fallback_cmd[-2:] == [
        "--yt-dlp-args",
        "--extractor-args youtube:player_client=android",
    ]

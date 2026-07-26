from pathlib import Path
from unittest.mock import patch, MagicMock, call

from script.add_metadata import clean_metadata, rename_file, main


def _make_audio_mock(artist=None, title=None):
    audio = MagicMock()
    audio.get.side_effect = lambda key: artist if key == "artist" else title
    return audio


# --- clean_metadata ---


@patch("script.add_metadata.MP3")
def test_clean_metadata_preserves_artist_and_title(mock_mp3_cls):
    artist = ["Test Artist"]
    title = ["Test Title"]
    audio = _make_audio_mock(artist=artist, title=title)
    mock_mp3_cls.return_value = audio

    clean_metadata(Path("fake.mp3"))

    audio.__setitem__.assert_any_call("artist", artist)
    audio.__setitem__.assert_any_call("title", title)


@patch("script.add_metadata.MP3")
def test_clean_metadata_deletes_before_setting_tags(mock_mp3_cls):
    call_log = []
    audio = MagicMock()
    audio.get.side_effect = lambda key: ["Artist"] if key == "artist" else ["Title"]
    audio.delete.side_effect = lambda: call_log.append("delete")

    original_setitem = MagicMock(side_effect=lambda k, v: call_log.append(f"set_{k}"))
    audio.__setitem__ = original_setitem

    mock_mp3_cls.return_value = audio

    clean_metadata(Path("fake.mp3"))

    assert "delete" in call_log
    assert f"set_artist" in call_log
    assert call_log.index("delete") < call_log.index("set_artist")


@patch("script.add_metadata.MP3")
def test_clean_metadata_saves_after_setting_tags(mock_mp3_cls):
    audio = _make_audio_mock(artist=["A"], title=["T"])
    mock_mp3_cls.return_value = audio

    clean_metadata(Path("fake.mp3"))

    audio.save.assert_called_once()


@patch("script.add_metadata.MP3")
def test_clean_metadata_with_none_values_does_not_raise(mock_mp3_cls):
    audio = _make_audio_mock(artist=None, title=None)
    mock_mp3_cls.return_value = audio

    clean_metadata(Path("fake.mp3"))  # should not raise

    audio.save.assert_called_once()


@patch("script.add_metadata.MP3")
def test_clean_metadata_passes_file_path_to_mp3(mock_mp3_cls):
    audio = _make_audio_mock()
    mock_mp3_cls.return_value = audio
    file_path = Path("some/path/song.mp3")

    clean_metadata(file_path)

    assert mock_mp3_cls.call_args[0][0] == file_path


# --- rename_file ---


@patch("script.add_metadata.MP3")
def test_rename_file_renames_to_title(mock_mp3_cls, tmp_path):
    original = tmp_path / "original_name.mp3"
    original.write_bytes(b"")

    audio = MagicMock()
    audio.get.return_value = ["My Song"]
    mock_mp3_cls.return_value = audio

    rename_file(original)

    assert (tmp_path / "My Song.mp3").exists()
    assert not original.exists()


@patch("script.add_metadata.MP3")
def test_rename_file_skips_when_title_is_none(mock_mp3_cls, tmp_path):
    original = tmp_path / "keep_me.mp3"
    original.write_bytes(b"")

    audio = MagicMock()
    audio.get.return_value = None
    mock_mp3_cls.return_value = audio

    rename_file(original)

    assert original.exists()  # file not renamed


@patch("script.add_metadata.MP3")
def test_rename_file_skips_when_title_is_empty_list(mock_mp3_cls, tmp_path):
    original = tmp_path / "keep_me.mp3"
    original.write_bytes(b"")

    audio = MagicMock()
    audio.get.return_value = []
    mock_mp3_cls.return_value = audio

    rename_file(original)

    assert original.exists()


# --- main ---


@patch("script.add_metadata.rename_file")
@patch("script.add_metadata.clean_metadata")
@patch("script.add_metadata.os.listdir")
def test_main_processes_mp3_files(mock_listdir, mock_clean, mock_rename):
    mock_listdir.return_value = ["track1.mp3", "track2.mp3"]

    main()

    assert mock_clean.call_count == 2
    assert mock_rename.call_count == 2


@patch("script.add_metadata.rename_file")
@patch("script.add_metadata.clean_metadata")
@patch("script.add_metadata.os.listdir")
def test_main_skips_non_mp3_files(mock_listdir, mock_clean, mock_rename):
    mock_listdir.return_value = ["track.mp3", "cover.jpg", "notes.txt"]

    main()

    assert mock_clean.call_count == 1
    assert mock_rename.call_count == 1


@patch("script.add_metadata.rename_file")
@patch("script.add_metadata.clean_metadata")
@patch("script.add_metadata.os.listdir")
def test_main_with_no_mp3_files(mock_listdir, mock_clean, mock_rename):
    mock_listdir.return_value = ["cover.jpg", "info.txt"]

    main()

    mock_clean.assert_not_called()
    mock_rename.assert_not_called()


@patch("script.add_metadata.rename_file")
@patch("script.add_metadata.clean_metadata")
@patch("script.add_metadata.os.listdir")
def test_main_passes_correct_path_to_functions(mock_listdir, mock_clean, mock_rename):
    mock_listdir.return_value = ["song.mp3"]

    main()

    called_path = mock_clean.call_args[0][0]
    assert called_path.name == "song.mp3"

from collections import abc
from typing import Any, cast

import pytest

from seminar08.tasks.task01_playlist.playlist import Playlist


def test_length_and_integer_indices() -> None:
    playlist: Any = Playlist(["Intro", "Verse", "Outro"])

    assert len(playlist) == 3
    assert playlist[0] == "Intro"
    assert playlist[-1] == "Outro"
    with pytest.raises(IndexError):
        playlist[3]
    with pytest.raises(IndexError):
        playlist[-4]


def test_empty_playlist_ends_iteration_immediately() -> None:
    playlist: Any = Playlist([])

    assert len(playlist) == 0
    assert list(playlist) == []
    with pytest.raises(IndexError):
        playlist[0]


def test_slices_return_independent_playlists() -> None:
    playlist: Any = Playlist(["Intro", "Verse", "Chorus", "Outro"])

    middle = playlist[1:3]
    backward = playlist[::-1]

    assert isinstance(middle, Playlist)
    assert list(cast(Any, middle)) == ["Verse", "Chorus"]
    assert cast(Any, middle)[0] == "Verse"
    assert isinstance(backward, Playlist)
    assert list(cast(Any, backward)) == ["Outro", "Chorus", "Verse", "Intro"]


def test_iteration_and_reversed_use_sequence_methods() -> None:
    playlist: Any = Playlist(["Intro", "Verse", "Outro"])

    assert list(playlist) == ["Intro", "Verse", "Outro"]
    assert list(reversed(playlist)) == ["Outro", "Verse", "Intro"]
    assert "__iter__" not in Playlist.__dict__
    assert "__reversed__" not in Playlist.__dict__
    assert not isinstance(playlist, abc.Iterable)


def test_membership_ignores_case_only_for_strings() -> None:
    playlist: Any = Playlist(["Intro", "Straße", "Outro"])

    assert "INTRO" in playlist
    assert "STRASSE" in playlist
    assert "unknown" not in playlist
    assert 42 not in playlist


def test_source_list_changes_do_not_change_playlist() -> None:
    tracks = ["Intro", "Outro"]
    playlist: Any = Playlist(tracks)
    tracks.append("Bonus")
    tracks[0] = "Changed"

    assert list(playlist) == ["Intro", "Outro"]


def test_representation_shows_tracks() -> None:
    assert repr(Playlist(["Intro", "Outro"])) == "Playlist(['Intro', 'Outro'])"
    assert repr(Playlist([])) == "Playlist([])"

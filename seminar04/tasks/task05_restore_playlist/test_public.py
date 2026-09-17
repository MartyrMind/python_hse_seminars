from collections.abc import Callable

from seminar04.tasks.task05_restore_playlist.restore_playlist import (
    Playlist,
    restore_playlist,
    snapshot_playlist,
)


def sample() -> Playlist:
    return [
        {"title": "A", "tags": ["rock"]},
        {"title": "B", "tags": ["live"]},
    ]


def test_snapshot_has_equal_content_but_no_shared_mutable_objects() -> None:
    playlist = sample()
    saved = snapshot_playlist(playlist)
    assert saved == playlist
    assert saved is not playlist
    assert saved[0] is not playlist[0]
    assert saved[0]["tags"] is not playlist[0]["tags"]


def test_changes_after_snapshot_do_not_affect_saved_copy() -> None:
    playlist = sample()
    saved = snapshot_playlist(playlist)
    playlist[0]["tags"].append("favorite")
    playlist.append({"title": "C", "tags": []})
    assert saved == [
        {"title": "A", "tags": ["rock"]},
        {"title": "B", "tags": ["live"]},
    ]


def test_restore_changes_contents_of_the_same_outer_list() -> None:
    playlist = sample()
    saved = snapshot_playlist(playlist)
    alias = playlist
    playlist.clear()
    playlist.append({"title": "C", "tags": ["new"]})

    operation: Callable[[Playlist, Playlist], object] = restore_playlist
    result = operation(playlist, saved)
    assert result is None
    assert playlist == saved
    assert alias is playlist
    assert alias == saved


def test_restored_playlist_does_not_share_mutable_objects_with_snapshot() -> None:
    playlist = sample()
    saved = snapshot_playlist(playlist)
    playlist[0]["tags"].append("changed")
    restore_playlist(playlist, saved)

    assert playlist is not saved
    assert playlist[0] is not saved[0]
    assert playlist[0]["tags"] is not saved[0]["tags"]

    playlist[0]["tags"].append("new")
    assert saved[0]["tags"] == ["rock"]


def test_snapshot_and_restore_preserve_internal_shared_references() -> None:
    shared_tags = ["rock"]
    playlist: Playlist = [
        {"title": "A", "tags": shared_tags},
        {"title": "B", "tags": shared_tags},
    ]
    saved = snapshot_playlist(playlist)
    assert saved[0]["tags"] is saved[1]["tags"]
    assert saved[0]["tags"] is not shared_tags

    playlist.clear()
    restore_playlist(playlist, saved)
    assert playlist[0]["tags"] is playlist[1]["tags"]
    assert playlist[0]["tags"] is not saved[0]["tags"]


def test_empty_playlist_can_be_saved_and_restored() -> None:
    playlist: Playlist = []
    saved = snapshot_playlist(playlist)
    playlist.append({"title": "temporary", "tags": []})
    restore_playlist(playlist, saved)
    assert playlist == []

from typing import TypedDict


class Track(TypedDict):
    title: str
    tags: list[str]


Playlist = list[Track]


def snapshot_playlist(playlist: Playlist) -> Playlist:
    raise NotImplementedError("Implement me")


def restore_playlist(playlist: Playlist, saved: Playlist) -> None:
    raise NotImplementedError("Implement me")

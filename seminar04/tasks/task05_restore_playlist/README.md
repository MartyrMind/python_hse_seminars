# Задача 5. restore_playlist — 9/10

Плейлист представлен списком словарей. У каждой записи есть название и список
тегов:

```python
playlist = [
    {"title": "A", "tags": ["rock"]},
    {"title": "B", "tags": ["live"]},
]
```

Нужно уметь сохранить независимый снимок плейлиста и позднее восстановить
содержимое исходного объекта.

Реализуйте две функции:

- `snapshot_playlist` возвращает независимый снимок всего плейлиста;
- `restore_playlist` восстанавливает переданный плейлист на месте и возвращает
  `None`.

## Сигнатуры

```python
from typing import TypedDict


class Track(TypedDict):
    title: str
    tags: list[str]


Playlist = list[Track]


def snapshot_playlist(playlist: Playlist) -> Playlist: ...


def restore_playlist(playlist: Playlist, saved: Playlist) -> None: ...
```

## Требования к снимку

- снимок равен исходному плейлисту по содержимому;
- внешний список, словари записей и списки тегов являются новыми объектами;
- последующие изменения исходного плейлиста не влияют на снимок;
- если две записи исходного плейлиста ссылались на один список тегов, в снимке
  соответствующие записи тоже ссылаются на один общий новый список тегов.

## Требования к восстановлению

- после вызова плейлист равен снимку по содержимому;
- внешний объект плейлиста остаётся тем же;
- восстановленный плейлист не разделяет изменяемые объекты со снимком;
- внутренние общие ссылки снимка сохраняются в восстановленном плейлисте;
- функция возвращает `None`.

## Примеры

```python
playlist = [{"title": "A", "tags": ["rock"]}]
saved = snapshot_playlist(playlist)

saved == playlist  # True
saved is playlist  # False
saved[0] is playlist[0]  # False
saved[0]["tags"] is playlist[0]["tags"]  # False

playlist[0]["tags"].append("favorite")
saved  # [{"title": "A", "tags": ["rock"]}]
```

```python
playlist = [
    {"title": "A", "tags": ["rock"]},
    {"title": "B", "tags": ["live"]},
]
saved = snapshot_playlist(playlist)
view = playlist

playlist.clear()
playlist.append({"title": "C", "tags": ["new"]})
restore_playlist(playlist, saved)  # None

playlist == saved  # True
view == saved  # True
view is playlist  # True
playlist[0]["tags"] is saved[0]["tags"]  # False
```

```python
shared_tags = ["rock"]
playlist = [
    {"title": "A", "tags": shared_tags},
    {"title": "B", "tags": shared_tags},
]

saved = snapshot_playlist(playlist)
saved[0]["tags"] is saved[1]["tags"]  # True
saved[0]["tags"] is shared_tags  # False
```

## Проверка

```bash
uv run pytest seminar04/tasks/task05_restore_playlist -v
```

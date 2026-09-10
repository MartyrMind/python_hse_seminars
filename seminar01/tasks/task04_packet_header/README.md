# Задача 4. packet_header

Сетевой протокол хранит три небольших числа в одном 16-битном заголовке:

```text
бит:  15           13 12              8 7                 0
     +---------------+-----------------+-------------------+
     | version: 3 бита| kind: 5 битов   | payload_size: 8   |
     +---------------+-----------------+-------------------+
```

Поле `version` занимает три старших бита, `kind` — следующие пять,
`payload_size` — восемь младших.

Реализуйте две обратные функции:

```python
def pack_header(version: int, kind: int, payload_size: int) -> int: ...

def unpack_header(header: int) -> tuple[int, int, int]: ...
```

`pack_header` собирает поля в одно число. `unpack_header` возвращает их в
порядке `version`, `kind`, `payload_size`.

## Примеры

```python
pack_header(0, 0, 0)       # 0x0000
pack_header(5, 17, 200)    # 0xB1C8
pack_header(7, 31, 255)    # 0xFFFF

unpack_header(0xB1C8)      # (5, 17, 200)
unpack_header(0xFFFF)      # (7, 31, 255)
```

Гарантируется, что `0 <= version < 8`, `0 <= kind < 32`,
`0 <= payload_size < 256`, а заголовок находится между `0` и `0xFFFF`.
Проверять диапазоны не нужно. Используйте битовые сдвиги, `|` и `&`, а не
умножение, деление или возведение в степень.

## Проверка

```bash
uv run pytest seminar01/tasks/task04_packet_header -v
```

# Семинар 8. Протоколы и интерфейсы

Первые две задачи показывают, как специальные методы определяют поведение
объекта: плейлист перебирается без наследования, а колода получает метод во
время выполнения. Третья задача сравнивает проверку интерфейса с попыткой
выполнить операцию. Затем студенты используют готовый ABC, создают собственный
ABC и описывают структурный интерфейс через `Protocol` и `TypeVar`.

Задачи можно решать независимо: ни одна не импортирует код другой задачи.

## Задачи

1. **5/10 — [`playlist`](tasks/task01_playlist/README.md):** построить плейлист
   на неформальном протоколе последовательности и настроить поиск через `in`.
2. **6/10 — [`shuffle_deck`](tasks/task02_shuffle_deck/README.md):** расширить
   готовый класс колоды методом, нужным для перемешивания на месте.
3. **7/10 — [`inspect_capabilities`](tasks/task03_inspect_capabilities/README.md):**
   сравнить `hasattr`, стандартные ABC и реальный вызов `iter` и `hash`.
4. **8/10 — [`route`](tasks/task04_route/README.md):** реализовать минимальный
   контракт `MutableSequence` и получить остальные операции от ABC.
5. **9/10 — [`card_sources`](tasks/task05_card_sources/README.md):** создать
   собственный ABC с двумя реализациями и общими готовыми методами.
6. **10/10 — [`repeat_to_length`](tasks/task06_repeat_to_length/README.md):**
   типизировать структурный протокол и проверять смысловой контракт повторения.

## Проверка

```bash
uv run pytest seminar08/tasks/task01_playlist -v
uv run pytest seminar08/tasks/task02_shuffle_deck -v
uv run pytest seminar08/tasks/task03_inspect_capabilities -v
uv run pytest seminar08/tasks/task04_route -v
uv run pytest seminar08/tasks/task05_card_sources -v
uv run pytest seminar08/tasks/task06_repeat_to_length -v
```

Пока задачи не решены, тесты ожидаемо падают на незаполненных заготовках.
Реализуйте методы в файлах задач и запустите тесты соответствующего каталога.

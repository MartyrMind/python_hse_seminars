# Задача 4. participant — 8/10

Результаты участников хранятся в словаре. Участника определяет постоянный
числовой идентификатор, а отображаемое имя может меняться.

Реализуйте класс `Participant(student_id, name)`. Два экземпляра с одним
идентификатором должны обозначать одного участника независимо от имени.

## Требования

- `student_id` — свойство только для чтения;
- `name` — обычное поле, которое можно менять;
- два экземпляра `Participant` равны, когда совпадают их идентификаторы;
- равные участники имеют равные хеши;
- участника можно использовать ключом словаря и элементом множества;
- изменение имени не меняет равенство, хеш и результат поиска по ключу;
- для объекта другого типа `__eq__` возвращает `NotImplemented`.

Напишите `__eq__` и `__hash__` самостоятельно, без `dataclass`.
Идентификатор — целое число, имя — строка; проверять типы не требуется.
Наследование `Participant` в этой задаче не рассматривается. Защищать
внутренние поля от намеренного изменения в обход публичного свойства не нужно.

## Примеры

```python
anna = Participant(17, "Анна")
same_student = Participant(17, "Аня")
another_student = Participant(18, "Анна")

anna == same_student  # True
anna == another_student  # False
anna is same_student  # False

results = {anna: 8}
results[same_student]  # 8

anna.name = "Анна Петрова"
results[anna]  # 8
results[same_student]  # 8
```

```python
len({anna, same_student, another_student})  # 2
hash(anna) == hash(same_student)  # True
anna == 17  # False
anna.__eq__(17) is NotImplemented  # True

results[same_student] = 9
len(results)  # 1
results[anna]  # 9

anna.student_id = 99  # AttributeError
Participant(0, "").name  # ""
```

## Проверка

```bash
uv run pytest seminar06/tasks/task04_participant -v
```

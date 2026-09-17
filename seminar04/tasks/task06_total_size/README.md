# Задача 6. total_size — 10/10

Данные состоят из целых чисел, строк, списков и словарей. Размер отдельного
объекта определяется вызовом `value.__sizeof__()`.

Реализуйте функцию `total_size`, которая возвращает сумму размеров всех разных
объектов, входящих во вложенную структуру.

## Сигнатура

```python
Data = int | str | list["Data"] | dict[str, "Data"]


def total_size(data: Data) -> int: ...
```

## Требования

- исходный объект тоже входит в сумму;
- для списка учитываются все его элементы;
- для словаря учитываются его ключи и значения;
- один и тот же объект учитывается ровно один раз независимо от числа ссылок
  на него;
- равные по содержимому, но разные объекты учитываются отдельно;
- правило однократного учёта относится и к контейнерам, и к числам, и к
  строкам;
- структура конечна и не содержит циклических ссылок;
- исходные данные не изменяются.

## Примеры

```python
total_size(1000)
# (1000).__sizeof__()

word = "прокси"
total_size(word)
# word.__sizeof__()

empty = []
total_size(empty)
# empty.__sizeof__()
```

```python
inner = [1000]
outer = [inner]

total_size(outer)
# outer.__sizeof__() + inner.__sizeof__() + (1000).__sizeof__()
```

```python
record = {"путь": "/api"}

total_size(record)
# record.__sizeof__()
# + "путь".__sizeof__()
# + "/api".__sizeof__()
```

Один внутренний объект может встречаться несколько раз:

```python
shared = [1000]
data = [shared, shared]

total_size(data)
# data.__sizeof__() + shared.__sizeof__() + (1000).__sizeof__()
```

Равные независимые объекты учитываются отдельно:

```python
left = [1000]
right = [1000]

left == right  # True
left is right  # False
total_size([left, right]) > total_size([left, left])  # True
```

Правило однократного учёта распространяется на неизменяемые объекты:

```python
number = int("1000")
data = [number, number]

total_size(data)
# data.__sizeof__() + number.__sizeof__()
```

## Проверка

```bash
uv run pytest seminar04/tasks/task06_total_size -v
```

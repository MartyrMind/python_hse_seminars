# Задача 1. message_factory — 5/10

Сообщения хранят текст, но показывают его по-разному. `Message` возвращает
исходный текст, `LoudMessage` переводит его в верхний регистр, а `QuotedMessage`
окружает кавычками `«…»`. Конструкторы и методы `render` уже написаны.

Реализуйте метод `from_line(text)`. Он убирает пробельные символы по краям
строки и создаёт новый экземпляр того класса, через который вызван.

## Требования

- фабрика объявлена только в `Message`;
- вызов через наследника создаёт экземпляр этого наследника;
- новые наследники с конструктором от одного текстового аргумента тоже
  используют эту фабрику без её изменения;
- вызов через экземпляр создаёт новый объект его класса, не меняя исходный;
- пробелы внутри текста сохраняются, пустой текст допустим;
- каждый вызов создаёт отдельный объект.


## Примеры

```python
plain = Message.from_line("  привет  ")
loud = LoudMessage.from_line("  привет  ")
quoted = QuotedMessage.from_line("  привет  ")

plain.render()  # "привет"
loud.render()  # "ПРИВЕТ"
quoted.render()  # "«привет»"

type(loud) is LoudMessage  # True
type(quoted) is QuotedMessage  # True

Message.from_line(" два  слова ").text  # "два  слова"
QuotedMessage.from_line(" \t\n").render()  # "«»"
```

```python
original = LoudMessage("старое")
new = original.from_line(" новое ")
new.render()  # "НОВОЕ"
original.text  # "старое"
new is original  # False
```

До решения объясните, какой объект вернула бы фабрика с телом
`return Message(text.strip())` при вызове через `LoudMessage`.

## Проверка

```bash
uv run pytest seminar06/tasks/task01_message_factory -v
```

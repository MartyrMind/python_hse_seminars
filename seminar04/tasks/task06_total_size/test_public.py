from seminar04.tasks.task06_total_size.total_size import Data, total_size


def test_atomic_values_weigh_themselves() -> None:
    assert total_size(1000) == (1000).__sizeof__()
    word = "прокси"
    assert total_size(word) == word.__sizeof__()


def test_empty_containers_weigh_themselves() -> None:
    empty_list: list[Data] = []
    empty_dict: dict[str, Data] = {}
    assert total_size(empty_list) == empty_list.__sizeof__()
    assert total_size(empty_dict) == empty_dict.__sizeof__()


def test_counts_nested_lists_at_every_depth() -> None:
    innermost: list[Data] = [1000]
    middle: list[Data] = [innermost]
    outer: list[Data] = [middle]
    assert total_size(outer) == (
        outer.__sizeof__() + middle.__sizeof__() + innermost.__sizeof__() + (1000).__sizeof__()
    )


def test_same_list_twice_is_counted_once() -> None:
    inner: list[Data] = [1000, 2000]
    twice: list[Data] = [inner, inner]
    once: list[Data] = [inner]
    assert total_size(twice) - twice.__sizeof__() == total_size(once) - once.__sizeof__()


def test_same_atomic_object_twice_is_counted_once() -> None:
    number = int("1000")
    data: list[Data] = [number, number]
    assert total_size(data) == data.__sizeof__() + number.__sizeof__()


def test_equal_but_distinct_lists_are_counted_separately() -> None:
    left: list[Data] = [1000, 2000]
    right: list[Data] = [1000, 2000]
    shared: list[Data] = [left, left]
    separate: list[Data] = [left, right]
    assert total_size(separate) - total_size(shared) == right.__sizeof__()


def test_dictionary_counts_keys_and_values() -> None:
    record: dict[str, Data] = {"путь": "/api"}
    assert total_size(record) == (record.__sizeof__() + "путь".__sizeof__() + "/api".__sizeof__())


def test_dictionary_inside_list() -> None:
    record: dict[str, Data] = {"путь": "/api"}
    log: list[Data] = [record]
    assert total_size(log) == (
        log.__sizeof__() + record.__sizeof__() + "путь".__sizeof__() + "/api".__sizeof__()
    )


def test_shared_values_across_dictionary_keys_are_counted_once() -> None:
    shared: list[Data] = [1000]
    data: dict[str, Data] = {"left": shared, "right": shared}
    expected = (
        data.__sizeof__()
        + "left".__sizeof__()
        + "right".__sizeof__()
        + shared.__sizeof__()
        + (1000).__sizeof__()
    )
    assert total_size(data) == expected


def test_input_is_unchanged() -> None:
    data: dict[str, Data] = {"a": [1000, 2000]}
    total_size(data)
    assert data == {"a": [1000, 2000]}

from collections import abc
from typing import Any

import pytest

from seminar08.tasks.task04_route.route import Route

route_type: Any = Route


def test_creation_from_generator_normalizes_stops_and_shows_repr() -> None:
    route: Any = route_type(stop for stop in [" Москва ", "Тверь", " Бологое "])

    assert len(route) == 3
    assert list(route) == ["Москва", "Тверь", "Бологое"]
    assert repr(route) == "Route(['Москва', 'Тверь', 'Бологое'])"


def test_source_list_is_not_used_as_route_storage() -> None:
    stops = ["Москва", "Тверь"]
    route: Any = route_type(stops)
    stops[0] = "Химки"
    stops.append("Клин")

    assert list(route) == ["Москва", "Тверь"]


def test_indexing_assignment_deletion_and_insertion() -> None:
    route: Any = route_type(["Москва", "Тверь"])

    assert route[-1] == "Тверь"
    route[0] = " Химки "
    route.insert(1, " Клин ")
    del route[-1]

    assert list(route) == ["Химки", "Клин"]
    with pytest.raises(IndexError):
        route[2]
    with pytest.raises(IndexError):
        route[2] = "Тверь"
    with pytest.raises(IndexError):
        del route[2]


def test_insert_uses_list_boundary_rules() -> None:
    route: Any = route_type(["Москва", "Тверь"])

    route.insert(99, " Бологое ")
    route.insert(-99, " Химки ")

    assert list(route) == ["Химки", "Москва", "Тверь", "Бологое"]


def test_inherited_methods_work_through_required_methods() -> None:
    route: Any = route_type(["Москва", "Тверь"])

    route.append(" Новгород ")
    route.extend([" Бологое "])
    route += [" Ярославль "]
    assert list(route) == ["Москва", "Тверь", "Новгород", "Бологое", "Ярославль"]
    assert route.index("Тверь") == 1
    assert route.count("Москва") == 1
    assert "Новгород" in route
    assert list(reversed(route)) == ["Ярославль", "Бологое", "Новгород", "Тверь", "Москва"]

    route.reverse()
    assert route.pop() == "Москва"
    route.remove("Новгород")
    assert list(route) == ["Ярославль", "Бологое", "Тверь"]


def test_empty_stop_is_rejected_by_all_write_paths() -> None:
    with pytest.raises(ValueError):
        route_type(["Москва", "   "])

    route: Any = route_type(["Москва"])
    with pytest.raises(ValueError):
        route.insert(0, "   ")
    with pytest.raises(ValueError):
        route.append("   ")
    with pytest.raises(ValueError):
        route[0] = "   "
    assert list(route) == ["Москва"]


def test_route_declares_abc_and_inherits_ready_methods() -> None:
    route: Any = route_type()

    assert isinstance(route, abc.MutableSequence)
    assert issubclass(Route, abc.MutableSequence)
    inherited = {"append", "extend", "pop", "remove", "reverse", "index", "count"}
    assert not inherited.intersection(Route.__dict__)

import traceback

import pytest

from seminar07.tasks.task03_build_exception_tree.build_exception_tree import (
    ErrorNode,
    build_exception_tree,
)


def test_top_level_errors_become_ordered_group_members() -> None:
    first = ValueError("первая операция")
    second = RuntimeError("вторая операция")

    root = build_exception_tree([first, second])

    assert isinstance(root.error, ExceptionGroup)
    assert root.error.message == "Ошибки операций"
    assert root.error.exceptions == (first, second)
    assert root.frames == []
    assert [relation for relation, _ in root.children] == ["member", "member"]
    assert [node.error for _, node in root.children] == [first, second]


def test_nested_group_members_are_expanded_recursively() -> None:
    inner = ExceptionGroup("внутренняя", [ValueError("а"), TypeError("б")])
    outer = ExceptionGroup("внешняя", [inner, LookupError("в")])

    root = build_exception_tree([outer])

    outer_node = root.children[0][1]
    inner_node = outer_node.children[0][1]
    assert [relation for relation, _ in outer_node.children] == ["member", "member"]
    assert [relation for relation, _ in inner_node.children] == ["member", "member"]
    assert [node.error for _, node in inner_node.children] == list(inner.exceptions)
    assert outer_node.children[1][1].error is outer.exceptions[1]


def test_explicit_cause_takes_priority_over_context() -> None:
    context = ValueError("контекст")
    cause = OSError("причина")
    error = RuntimeError("итог")
    error.__context__ = context
    error.__cause__ = cause

    node = build_exception_tree([error]).children[0][1]

    assert [(kind, child.error) for kind, child in node.children] == [("cause", cause)]
    assert error.__context__ is context


def test_unsuppressed_context_is_followed_recursively() -> None:
    deepest = KeyError("глубина")
    middle = ValueError("середина")
    outer = RuntimeError("снаружи")
    middle.__context__ = deepest
    outer.__context__ = middle

    node = build_exception_tree([outer]).children[0][1]

    assert node.children[0][0] == "context"
    assert node.children[0][1].error is middle
    assert node.children[0][1].children[0][0] == "context"
    assert node.children[0][1].children[0][1].error is deepest


def test_suppressed_context_is_hidden_even_without_cause() -> None:
    error = RuntimeError("итог")
    error.__context__ = ValueError("скрыто")
    error.__suppress_context__ = True

    node = build_exception_tree([error]).children[0][1]

    assert node.children == []


def test_raise_from_none_hides_real_context() -> None:
    try:
        raise ValueError("исходная")
    except ValueError:
        try:
            raise RuntimeError("новая") from None
        except RuntimeError as error:
            assert error.__context__ is not None
            assert error.__cause__ is None
            assert error.__suppress_context__
            node = build_exception_tree([error]).children[0][1]

    assert node.children == []


def test_group_members_come_before_groups_own_cause() -> None:
    member = ValueError("в группе")
    group = ExceptionGroup("группа", [member])
    cause = OSError("источник")
    group.__cause__ = cause

    node = build_exception_tree([group]).children[0][1]

    assert [(kind, child.error) for kind, child in node.children] == [
        ("member", member),
        ("cause", cause),
    ]


def test_base_exception_group_in_cause_chain_is_expanded() -> None:
    control = KeyboardInterrupt()
    ordinary = ValueError("ошибка")
    group = BaseExceptionGroup("группа", [control, ordinary])
    outer = RuntimeError("снаружи")
    outer.__cause__ = group

    node = build_exception_tree([outer]).children[0][1]
    group_node = node.children[0][1]

    assert node.children[0][0] == "cause"
    assert group_node.error is group
    assert [(kind, child.error) for kind, child in group_node.children] == [
        ("member", control),
        ("member", ordinary),
    ]


def test_each_node_gets_its_own_traceback_snapshot() -> None:
    def fail_origin() -> None:
        raise ValueError("исходная ошибка")

    def fail_wrapper() -> None:
        try:
            fail_origin()
        except ValueError as original:
            raise RuntimeError("обёртка") from original

    try:
        fail_wrapper()
    except RuntimeError as error:
        root = build_exception_tree([error])
        wrapper = root.children[0][1]
        original = wrapper.children[0][1]

        assert wrapper.children[0][0] == "cause"
        assert isinstance(wrapper.frames[0], traceback.FrameSummary)
        assert [frame.name for frame in wrapper.frames][-1] == "fail_wrapper"
        assert [frame.name for frame in original.frames][-1] == "fail_origin"
        assert wrapper.frames == list(traceback.extract_tb(error.__traceback__))
        assert original.frames == list(traceback.extract_tb(original.error.__traceback__))


def test_frame_summaries_survive_removing_original_traceback() -> None:
    failure = ValueError("ошибка")
    try:
        raise failure
    except ValueError:
        node = build_exception_tree([failure]).children[0][1]

    failure.__traceback__ = None
    assert node.frames
    assert node.frames[-1].name == "test_frame_summaries_survive_removing_original_traceback"
    assert all(isinstance(frame, traceback.FrameSummary) for frame in node.frames)


def test_unraised_error_has_no_frames() -> None:
    node = build_exception_tree([ValueError("создано")]).children[0][1]
    assert node.frames == []


def test_cycle_ends_with_leaf_but_keeps_its_edge() -> None:
    first = ValueError("а")
    second = TypeError("б")
    first.__context__ = second
    second.__context__ = first

    node = build_exception_tree([first]).children[0][1]

    assert node.children[0][0] == "context"
    second_node = node.children[0][1]
    assert second_node.error is second
    assert second_node.children[0][0] == "context"
    repeated_first = second_node.children[0][1]
    assert repeated_first.error is first
    assert repeated_first.children == []


def test_same_error_in_separate_branches_is_expanded_each_time() -> None:
    shared = ValueError("общая")
    shared.__context__ = KeyError("ниже")
    first = RuntimeError("первая")
    second = TypeError("вторая")
    first.__cause__ = shared
    second.__cause__ = shared

    root = build_exception_tree([first, second])

    for _, branch in root.children:
        shared_node = branch.children[0][1]
        assert shared_node.error is shared
        assert shared_node.children[0][0] == "context"
        assert isinstance(shared_node.children[0][1].error, KeyError)


def test_empty_input_is_rejected() -> None:
    with pytest.raises(ValueError):
        build_exception_tree([])


def test_input_exceptions_are_not_modified() -> None:
    original = ValueError("исходная")
    error = RuntimeError("итог")
    error.__context__ = original
    before = (error.__cause__, error.__context__, error.__suppress_context__, error.__traceback__)

    result = build_exception_tree([error])

    assert isinstance(result, ErrorNode)
    assert (
        error.__cause__,
        error.__context__,
        error.__suppress_context__,
        error.__traceback__,
    ) == before

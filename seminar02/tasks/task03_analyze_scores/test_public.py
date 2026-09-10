from seminar02.tasks.task03_analyze_scores.analyze_scores import analyze_scores


def test_selects_passing_scores_and_finds_perfect_score() -> None:
    assert analyze_scores([3, 4, 10]) == ([4, 10], True, True)


def test_invalid_scores_do_not_enter_passing_list() -> None:
    assert analyze_scores([12, -1, 7]) == ([7], False, False)


def test_empty_input_uses_any_and_all_semantics() -> None:
    assert analyze_scores([]) == ([], False, True)


def test_valid_scores_can_all_be_failing() -> None:
    assert analyze_scores([0, 1, 2, 3]) == ([], False, True)

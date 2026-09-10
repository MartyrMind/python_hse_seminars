from seminar02.tasks.task06_pack_batches.pack_batches import pack_batches


def test_greedily_packs_items_in_order() -> None:
    assert pack_batches([4, 3, 5, 2, 2], 7) == [[4, 3], [5, 2], [2]]


def test_exact_capacity_stays_in_one_batch() -> None:
    assert pack_batches([2, 3, 5], 10) == [[2, 3, 5]]


def test_full_item_starts_its_own_batch() -> None:
    assert pack_batches([5, 1, 4], 5) == [[5], [1, 4]]


def test_empty_input_produces_no_batches() -> None:
    assert pack_batches([], 10) == []

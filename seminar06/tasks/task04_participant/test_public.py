import pytest

from seminar06.tasks.task04_participant.participant import Participant


def test_equality_depends_on_id_and_not_name_or_identity() -> None:
    anna = Participant(17, "Анна")
    same = Participant(17, "Аня")
    other = Participant(18, "Анна")
    assert anna is not same
    assert anna == same
    assert same == anna
    assert anna != other
    assert anna == anna


def test_equal_participants_have_equal_hashes_and_merge_in_set() -> None:
    anna = Participant(17, "Анна")
    same = Participant(17, "Аня")
    other = Participant(18, "Анна")
    assert hash(anna) == hash(same)
    assert len({anna, same, other}) == 2


def test_lookup_and_update_through_equal_key() -> None:
    anna = Participant(17, "Анна")
    same = Participant(17, "Аня")
    results = {anna: 8}
    assert results[same] == 8
    results[same] = 9
    assert len(results) == 1
    assert results[anna] == 9


def test_renaming_keeps_hash_equality_and_dictionary_lookup() -> None:
    anna = Participant(17, "Анна")
    same = Participant(17, "Аня")
    results = {anna: 8}
    original_hash = hash(anna)
    anna.name = "Анна Петрова"
    assert anna.name == "Анна Петрова"
    assert same.name == "Аня"
    assert anna == same
    assert hash(anna) == original_hash
    assert results[anna] == results[same] == 8


def test_id_is_read_only_and_failed_write_keeps_key_usable() -> None:
    participant = Participant(17, "Анна")
    results = {participant: 8}
    with pytest.raises(AttributeError):
        participant.student_id = 99
    assert participant.student_id == 17
    assert results[Participant(17, "Аня")] == 8


@pytest.mark.parametrize("other", [17, "17", None, object()])
def test_unrelated_types_are_not_supported(other: object) -> None:
    participant = Participant(17, "Анна")
    assert participant.__eq__(other) is NotImplemented
    assert (participant == other) is False
    assert (other == participant) is False


def test_zero_id_and_empty_name_are_valid() -> None:
    participant = Participant(0, "")
    assert participant.student_id == 0
    assert participant.name == ""
    assert {participant: "found"}[Participant(0, "новое имя")] == "found"

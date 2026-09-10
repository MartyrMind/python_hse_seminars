from seminar01.tasks.task04_packet_header.packet_header import pack_header, unpack_header


def test_pack_zero_header() -> None:
    assert pack_header(0, 0, 0) == 0


def test_pack_known_header() -> None:
    assert pack_header(5, 17, 200) == 0xB1C8


def test_pack_maximum_values() -> None:
    assert pack_header(7, 31, 255) == 0xFFFF


def test_unpack_known_header() -> None:
    assert unpack_header(0xB1C8) == (5, 17, 200)


def test_unpack_maximum_values() -> None:
    assert unpack_header(0xFFFF) == (7, 31, 255)


def test_pack_and_unpack_round_trip() -> None:
    assert unpack_header(pack_header(3, 9, 127)) == (3, 9, 127)

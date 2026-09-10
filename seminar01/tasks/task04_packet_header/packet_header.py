def pack_header(version: int, kind: int, payload_size: int) -> int:
    raise NotImplementedError("Implement me")


def unpack_header(header: int) -> tuple[int, int, int]:
    raise NotImplementedError("Implement me")

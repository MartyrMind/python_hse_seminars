from types import NotImplementedType


class Affine:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def __call__(self, x: int) -> int:
        raise NotImplementedError("Implement me")

    def __mul__(self, other: object) -> Affine | NotImplementedType:
        raise NotImplementedError("Implement me")

    def __rmul__(self, other: object) -> Affine | NotImplementedType:
        raise NotImplementedError("Implement me")

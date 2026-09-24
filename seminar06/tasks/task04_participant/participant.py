class Participant:
    name: str

    def __init__(self, student_id: int, name: str) -> None:
        raise NotImplementedError("Implement me")

    def get_student_id(self) -> int:
        raise NotImplementedError("Implement me")

    student_id = property(get_student_id)

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError("Implement me")

    def __hash__(self) -> int:
        raise NotImplementedError("Implement me")

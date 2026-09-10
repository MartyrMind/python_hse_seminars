from seminar02.tasks.task04_walk_robot.walk_robot import walk_robot


def test_moves_robot_in_four_directions() -> None:
    commands = ["right 3", "up 2", "left 1", "down 5"]
    assert walk_robot(commands) == (2, -3, 4)


def test_pause_and_unknown_commands_are_ignored() -> None:
    commands = ["pause", "jump 100", "up 2", "wait"]
    assert walk_robot(commands) == (0, 2, 1)


def test_stop_ignores_remaining_commands() -> None:
    commands = ["right 4", "stop", "up 100"]
    assert walk_robot(commands) == (4, 0, 1)


def test_extra_whitespace_is_ignored() -> None:
    commands = ["  right   3  ", "\tup  4"]
    assert walk_robot(commands) == (3, 4, 2)

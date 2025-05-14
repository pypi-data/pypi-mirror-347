from random import random


def try_with(failure_chance: float) -> bool:
    assert 0 <= failure_chance <= 1, "Failure chance must be between 0 and 1."

    return random() > failure_chance

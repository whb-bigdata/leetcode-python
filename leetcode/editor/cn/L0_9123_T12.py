"""COMP9123 Tutorial 12 - Randomization programming solutions.

The functions implement the sampling algorithms from Problems 1-5, a skip-list
RangeSearch for Problem 6, and the blacklist remapping picker from Problem 7.
"""

from __future__ import annotations

import math
import random
from typing import Callable, Generic, Iterable, List, Optional, TypeVar


K = TypeVar("K")
V = TypeVar("V")


# Problem 1
def expected_geometric_trials(success_probability: float) -> float:
    """Return E[number of trials until first success] = 1 / p."""
    if not 0 < success_probability <= 1:
        raise ValueError("success_probability must be in (0, 1]")
    return 1 / success_probability


# Problem 2
def fair_coin_from_biased(biased_flip: Callable[[], bool]) -> bool:
    """Return a fair coin result from an unknown non-degenerate biased coin.

    Von Neumann's method rejects HH and TT. The remaining outcomes HT and TH
    have equal probability p(1-p), so returning True for HT and False for TH
    is fair without knowing p.
    """
    while True:
        first = biased_flip()
        second = biased_flip()
        if first != second:
            return first  # HT -> True; TH -> False


def expected_biased_flips_for_fair_coin(head_probability: float) -> float:
    """Return 1 / (p * (1-p)), the expected flips used by Von Neumann's method."""
    if not 0 < head_probability < 1:
        raise ValueError("head_probability must be in (0, 1)")
    return 1 / (head_probability * (1 - head_probability))


# Problem 3
def uniform_integer_from_fair_coin(n: int, fair_flip: Callable[[], bool]) -> int:
    """Uniformly sample an integer in {1, ..., n} using rejection sampling.

    Generate k = ceil(log2(n)) bits. Values at least n are rejected and retried.
    Every accepted value in [0, n) has equal probability.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    bit_count = (n - 1).bit_length()
    while True:
        value = 0
        for _ in range(bit_count):
            value = (value << 1) | int(fair_flip())
        if value < n:
            return value + 1


def expected_fair_flips_for_uniform_integer(n: int) -> float:
    """Return k * 2**k / n, where k = ceil(log2(n))."""
    if n <= 0:
        raise ValueError("n must be positive")
    bit_count = (n - 1).bit_length()
    return bit_count * (2**bit_count) / n


# Problems 4 and 5
def sample_unit_square(random_real: Callable[[], float] = random.random) -> tuple[float, float]:
    """Uniformly sample (x, y) from [-1, 1]^2 using exactly two random reals."""
    return 2 * random_real() - 1, 2 * random_real() - 1


def sample_unit_disk(random_real: Callable[[], float] = random.random) -> tuple[float, float]:
    """Uniformly sample the unit disk by rejecting square samples outside it.

    A proposal succeeds with probability pi/4, so this uses 4/pi proposals,
    or 8/pi calls to ``random_real``, in expectation.
    """
    while True:
        x, y = sample_unit_square(random_real)
        if x * x + y * y <= 1:
            return x, y


def expected_random_reals_for_unit_disk() -> float:
    """Return 8/pi random-real samples expected by disk rejection sampling."""
    return 8 / math.pi


# Problem 6
class _SkipNode(Generic[K, V]):
    def __init__(self, key: Optional[K], value: Optional[V], level: int) -> None:
        self.key = key
        self.value = value
        self.forward: List[Optional[_SkipNode[K, V]]] = [None] * (level + 1)


class SkipList(Generic[K, V]):
    """A simple randomized skip list with expected O(log n) operations."""

    def __init__(self, max_level: int = 16, probability: float = 0.5, rng: Optional[random.Random] = None) -> None:
        if max_level < 1 or not 0 < probability < 1:
            raise ValueError("max_level must be positive and probability must be in (0, 1)")
        self._max_level = max_level
        self._probability = probability
        self._rng = rng or random.Random()
        self._head: _SkipNode[K, V] = _SkipNode(None, None, max_level)
        self._level = 0
        self._size = 0

    def insert(self, key: K, value: V) -> None:
        """Insert or update an item in expected O(log n) time."""
        update: List[_SkipNode[K, V]] = [self._head] * (self._max_level + 1)
        current = self._head
        for level in range(self._level, -1, -1):
            while current.forward[level] is not None and current.forward[level].key < key:
                current = current.forward[level]
            update[level] = current

        current = current.forward[0]
        if current is not None and current.key == key:
            current.value = value
            return

        level = self._random_level()
        if level > self._level:
            for index in range(self._level + 1, level + 1):
                update[index] = self._head
            self._level = level
        node = _SkipNode(key, value, level)
        for index in range(level + 1):
            node.forward[index] = update[index].forward[index]
            update[index].forward[index] = node
        self._size += 1

    def range_search(self, lower: K, upper: K) -> List[tuple[K, V]]:
        """Return all s entries with lower <= key <= upper in expected O(log n + s)."""
        if lower > upper:
            return []
        current = self._head
        # Find the predecessor of the first key that is at least lower.
        for level in range(self._level, -1, -1):
            while current.forward[level] is not None and current.forward[level].key < lower:
                current = current.forward[level]

        current = current.forward[0]
        result: List[tuple[K, V]] = []
        while current is not None and current.key <= upper:
            assert current.key is not None and current.value is not None
            result.append((current.key, current.value))
            current = current.forward[0]
        return result

    def _random_level(self) -> int:
        level = 0
        while level < self._max_level and self._rng.random() < self._probability:
            level += 1
        return level


# Problem 7
class ActiveServerPicker:
    """Uniformly choose active server IDs in O(1) expected time per pick.

    Blacklisted IDs below ``bound`` are remapped to active IDs above ``bound``.
    Thus sampling uniformly from [0, bound) becomes a uniform sample over every
    non-blacklisted server without repeatedly retrying blacklisted IDs.
    """

    def __init__(self, server_count: int, blacklist: Iterable[int], rng: Optional[random.Random] = None) -> None:
        if server_count <= 0:
            raise ValueError("server_count must be positive")
        blocked = set(blacklist)
        if any(server < 0 or server >= server_count for server in blocked):
            raise ValueError("blacklisted server ID is outside the valid range")
        if len(blocked) == server_count:
            raise ValueError("at least one server must be active")

        self._rng = rng or random.Random()
        self._bound = server_count - len(blocked)
        lower_blacklisted = [server for server in blocked if server < self._bound]
        replacement_ids = [server for server in range(self._bound, server_count) if server not in blocked]
        self._remap = dict(zip(lower_blacklisted, replacement_ids))

    def pick(self) -> int:
        """Return one active server, uniformly, in O(1) expected time."""
        chosen = self._rng.randrange(self._bound)
        return self._remap.get(chosen, chosen)


if __name__ == "__main__":
    assert expected_geometric_trials(0.25) == 4

    biased_sequence = iter([True, True, False, True])  # HH rejected, then TH -> False
    assert fair_coin_from_biased(lambda: next(biased_sequence)) is False

    fair_sequence = iter([True, True, True, False, True, False])  # 7 rejected, then 2 accepted
    assert uniform_integer_from_fair_coin(5, lambda: next(fair_sequence)) == 3
    assert expected_fair_flips_for_uniform_integer(5) == 24 / 5

    square_values = iter([0.0, 0.75])
    assert sample_unit_square(lambda: next(square_values)) == (-1.0, 0.5)
    disk_values = iter([0.99, 0.99, 0.5, 0.5])
    assert sample_unit_disk(lambda: next(disk_values)) == (0.0, 0.0)

    skip_list = SkipList[int, str](rng=random.Random(7))
    for key, value in [(10, "ten"), (3, "three"), (7, "seven"), (15, "fifteen")]:
        skip_list.insert(key, value)
    assert skip_list.range_search(5, 12) == [(7, "seven"), (10, "ten")]

    picker = ActiveServerPicker(7, {2, 3, 5}, rng=random.Random(7))
    assert all(picker.pick() in {0, 1, 4, 6} for _ in range(100))
    print("Tutorial 12 randomization checks passed.")

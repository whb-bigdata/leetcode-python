"""COMP9123 Tutorial 7 - Hashing programming solutions (Problems 3-10).

Problems 1 and 2 are analysis-only questions. This file implements the
algorithmic questions and includes small executable checks at the bottom.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Generic, Hashable, Iterable, Iterator, List, Optional, Tuple, TypeVar


K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
T = TypeVar("T", bound=Hashable)


# Problem 3
def set_intersection(first: Iterable[T], second: Iterable[T]) -> set[T]:
    """Return the distinct intersection in expected O(n + m) time.

    The smaller input is stored in a set, so the additional space is
    O(min(n, m)) after materialising the two input iterables.
    """
    first_values = list(first)
    second_values = list(second)
    smaller, larger = (
        (first_values, second_values)
        if len(first_values) <= len(second_values)
        else (second_values, first_values)
    )
    candidates = set(smaller)
    return {value for value in larger if value in candidates}


# Problems 4 and 5
@dataclass
class _CuckooEntry(Generic[K, V]):
    key: K
    value: V


class _CuckooHashBase(Generic[K, V]):
    """Shared two-table cuckoo hash map operations.

    A key has exactly two possible locations. Subclasses differ only in how
    they detect that an insertion is following a cycle.
    """

    def __init__(self, capacity: int = 11) -> None:
        if capacity < 2:
            raise ValueError("capacity must be at least 2")
        self._capacity = capacity
        self._first: List[Optional[_CuckooEntry[K, V]]] = [None] * capacity
        self._second: List[Optional[_CuckooEntry[K, V]]] = [None] * capacity
        self._size = 0

    def _first_index(self, key: K) -> int:
        return hash(key) % self._capacity

    def _second_index(self, key: K) -> int:
        # The tagged tuple provides a second, independent-looking hash route.
        return hash(("cuckoo-second", key)) % self._capacity

    def get(self, key: K) -> Optional[V]:
        """Return the value for key, or None when it is absent, in O(1)."""
        first = self._first[self._first_index(key)]
        if first is not None and first.key == key:
            return first.value
        second = self._second[self._second_index(key)]
        return second.value if second is not None and second.key == key else None

    def delete(self, key: K) -> bool:
        """Delete key in O(1), returning whether a key was removed."""
        index = self._first_index(key)
        entry = self._first[index]
        if entry is not None and entry.key == key:
            self._first[index] = None
            self._size -= 1
            return True

        index = self._second_index(key)
        entry = self._second[index]
        if entry is not None and entry.key == key:
            self._second[index] = None
            self._size -= 1
            return True
        return False

    def size(self) -> int:
        return self._size

    def _update_if_present(self, entry: _CuckooEntry[K, V]) -> bool:
        first = self._first[self._first_index(entry.key)]
        if first is not None and first.key == entry.key:
            first.value = entry.value
            return True
        second = self._second[self._second_index(entry.key)]
        if second is not None and second.key == entry.key:
            second.value = entry.value
            return True
        return False

    def _slot(self, table: int, key: K) -> Tuple[List[Optional[_CuckooEntry[K, V]]], int]:
        if table == 0:
            return self._first, self._first_index(key)
        return self._second, self._second_index(key)


class CuckooHashByEvictionCount(_CuckooHashBase[K, V]):
    """Problem 4: detect a cuckoo cycle by limiting evictions.

    ``put`` returns False on a cycle. A production table would then rehash into
    larger tables; this exercise exposes the detection result directly.
    """

    def put(self, key: K, value: V) -> bool:
        if self._update_if_present(_CuckooEntry(key, value)):
            return True

        entry = _CuckooEntry(key, value)
        table = 0
        max_evictions = 2 * self._capacity
        changes: List[Tuple[int, int, Optional[_CuckooEntry[K, V]]]] = []

        for _ in range(max_evictions):
            slots, index = self._slot(table, entry.key)
            displaced = slots[index]
            changes.append((table, index, displaced))
            slots[index] = entry
            if displaced is None:
                self._size += 1
                return True
            entry = displaced
            table = 1 - table

        # Restore every overwritten slot, so a failed insertion loses no data.
        for table, index, previous in reversed(changes):
            (self._first if table == 0 else self._second)[index] = previous
        return False


class CuckooHashByVisitedFlags(_CuckooHashBase[K, V]):
    """Problem 5: detect a cycle by marking each visited table entry.

    Timestamps act as resettable flags: a slot is visited in this insertion if
    its stamp equals the current insertion stamp. This avoids clearing O(m)
    flags before every insertion.
    """

    def __init__(self, capacity: int = 11) -> None:
        super().__init__(capacity)
        self._first_flags = [0] * capacity
        self._second_flags = [0] * capacity
        self._stamp = 0

    def put(self, key: K, value: V) -> bool:
        if self._update_if_present(_CuckooEntry(key, value)):
            return True

        self._stamp += 1
        entry = _CuckooEntry(key, value)
        table = 0
        changes: List[Tuple[int, int, Optional[_CuckooEntry[K, V]]]] = []

        while True:
            slots, index = self._slot(table, entry.key)
            flags = self._first_flags if table == 0 else self._second_flags
            if flags[index] == self._stamp:
                for changed_table, changed_index, previous in reversed(changes):
                    (self._first if changed_table == 0 else self._second)[changed_index] = previous
                return False

            flags[index] = self._stamp
            displaced = slots[index]
            changes.append((table, index, displaced))
            slots[index] = entry
            if displaced is None:
                self._size += 1
                return True
            entry = displaced
            table = 1 - table


# Problem 6
@dataclass
class _OrderNode(Generic[K, V]):
    key: K
    value: V
    previous: Optional["_OrderNode[K, V]"] = None
    next: Optional["_OrderNode[K, V]"] = None


class InsertionOrderedHashTable(Generic[K, V]):
    """Hash table with O(1) expected put/get/delete and O(n) iteration.

    The dictionary gives expected O(1) key access. Each dictionary entry points
    to a node in a doubly linked list, which preserves insertion order with only
    O(1) extra pointer overhead per item.
    """

    def __init__(self) -> None:
        self._nodes: Dict[K, _OrderNode[K, V]] = {}
        self._head: Optional[_OrderNode[K, V]] = None
        self._tail: Optional[_OrderNode[K, V]] = None

    def put(self, key: K, value: V) -> None:
        node = self._nodes.get(key)
        if node is not None:
            node.value = value
            return

        node = _OrderNode(key, value, previous=self._tail)
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._nodes[key] = node

    def get(self, key: K) -> Optional[V]:
        node = self._nodes.get(key)
        return node.value if node is not None else None

    def delete(self, key: K) -> bool:
        node = self._nodes.pop(key, None)
        if node is None:
            return False
        if node.previous is None:
            self._head = node.next
        else:
            node.previous.next = node.next
        if node.next is None:
            self._tail = node.previous
        else:
            node.next.previous = node.previous
        return True

    def items(self) -> Iterator[Tuple[K, V]]:
        current = self._head
        while current is not None:
            yield current.key, current.value
            current = current.next


# Problem 7
def most_frequent_value(values: Iterable[T]) -> Optional[T]:
    """Return a most frequent value in expected O(n) time, or None if empty."""
    counts: Dict[T, int] = {}
    best_value: Optional[T] = None
    best_count = 0
    for value in values:
        counts[value] = counts.get(value, 0) + 1
        if counts[value] > best_count:
            best_value = value
            best_count = counts[value]
    return best_value


# Problem 8
class MultiMap(Generic[K, V]):
    """Map each key to all associated values using a hash table of lists."""

    def __init__(self) -> None:
        self._values: Dict[K, List[V]] = {}

    def put(self, key: K, value: V) -> None:
        """Associate value with key in expected O(1) amortised time."""
        self._values.setdefault(key, []).append(value)

    def get(self, key: K) -> List[V]:
        """Return all s values in expected O(1 + s) time."""
        return list(self._values.get(key, []))


# Problem 9
def shared_birthday(people: Iterable[Tuple[str, T]]) -> Optional[Tuple[str, str, T]]:
    """Return a pair of people with the same birthday in expected O(n) time.

    Reading n input birthdays already takes Omega(n) time. If birthdays are
    restricted to 366 calendar days, the fixed universe can be treated as a
    constant in the usual birthday-problem interpretation.
    """
    first_person_by_birthday: Dict[T, str] = {}
    for person, birthday in people:
        previous = first_person_by_birthday.get(birthday)
        if previous is not None:
            return previous, person, birthday
        first_person_by_birthday[birthday] = person
    return None


# Problem 10
def k_gram_frequencies(words: List[str], k: int) -> Dict[Tuple[str, ...], int]:
    """Count all k-grams in expected O(n) time for a fixed positive k."""
    if k <= 0:
        raise ValueError("k must be positive")
    frequencies: Dict[Tuple[str, ...], int] = {}
    for start in range(len(words) - k + 1):
        gram = tuple(words[start : start + k])
        frequencies[gram] = frequencies.get(gram, 0) + 1
    return frequencies


if __name__ == "__main__":
    assert set_intersection([1, 2, 2, 3], [2, 2, 4]) == {2}

    count_table = CuckooHashByEvictionCount[int, str]()
    flag_table = CuckooHashByVisitedFlags[int, str]()
    for table in (count_table, flag_table):
        assert table.put(1, "one") and table.put(2, "two")
        assert table.get(1) == "one" and table.delete(2) and table.get(2) is None

    ordered = InsertionOrderedHashTable[str, int]()
    ordered.put("first", 1)
    ordered.put("second", 2)
    ordered.put("first", 10)
    assert list(ordered.items()) == [("first", 10), ("second", 2)]

    assert most_frequent_value([4, 1, 4, 2, 4, 2]) == 4
    multimap = MultiMap[str, int]()
    multimap.put("course", 9123)
    multimap.put("course", 9024)
    assert multimap.get("course") == [9123, 9024]
    assert shared_birthday([("Ada", "01-01"), ("Lin", "02-02"), ("Sam", "01-01")]) == (
        "Ada",
        "Sam",
        "01-01",
    )
    assert k_gram_frequencies("to be or not to be".split(), 2) == {
        ("to", "be"): 2,
        ("be", "or"): 1,
        ("or", "not"): 1,
        ("not", "to"): 1,
    }
    print("Tutorial 7 hashing checks passed.")

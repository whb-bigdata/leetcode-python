"""COMP9123 Tutorial 11 - Divide and Conquer programming solutions.

Problem 5 consists only of recurrence solving, so it has no code solution here.
All other algorithmic questions are implemented with executable examples.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple, TypeVar


T = TypeVar("T")
Matrix = List[List[float]]


# Problem 1
def merge_sort(values: Sequence[T]) -> List[T]:
    """Sort values using divide-and-conquer merge sort in O(n log n) time."""
    if len(values) <= 1:
        return list(values)
    middle = len(values) // 2
    return _merge(merge_sort(values[:middle]), merge_sort(values[middle:]))


def _merge(left: Sequence[T], right: Sequence[T]) -> List[T]:
    result: List[T] = []
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1
    return result + list(left[left_index:]) + list(right[right_index:])


# Problem 2
def matrix_multiply_divide_conquer(first: Matrix, second: Matrix) -> Matrix:
    """Multiply two same-size square matrices by recursive block multiplication.

    For an even n, the recurrence is T(n) = 8T(n/2) + O(n^2). Odd sizes use
    direct multiplication as a base case so the public function remains usable
    for every square matrix size.
    """
    _validate_square_pair(first, second)
    size = len(first)
    if size == 0:
        return []
    if size == 1:
        return [[first[0][0] * second[0][0]]]
    if size % 2:
        return _naive_matrix_multiply(first, second)

    top_left_a, top_right_a, bottom_left_a, bottom_right_a = _split_matrix(first)
    top_left_b, top_right_b, bottom_left_b, bottom_right_b = _split_matrix(second)

    top_left = _matrix_add(
        matrix_multiply_divide_conquer(top_left_a, top_left_b),
        matrix_multiply_divide_conquer(top_right_a, bottom_left_b),
    )
    top_right = _matrix_add(
        matrix_multiply_divide_conquer(top_left_a, top_right_b),
        matrix_multiply_divide_conquer(top_right_a, bottom_right_b),
    )
    bottom_left = _matrix_add(
        matrix_multiply_divide_conquer(bottom_left_a, top_left_b),
        matrix_multiply_divide_conquer(bottom_right_a, bottom_left_b),
    )
    bottom_right = _matrix_add(
        matrix_multiply_divide_conquer(bottom_left_a, top_right_b),
        matrix_multiply_divide_conquer(bottom_right_a, bottom_right_b),
    )
    return [top_left[row] + top_right[row] for row in range(len(top_left))] + [
        bottom_left[row] + bottom_right[row] for row in range(len(bottom_left))
    ]


def _validate_square_pair(first: Matrix, second: Matrix) -> None:
    size = len(first)
    if len(second) != size or any(len(row) != size for row in first + second):
        raise ValueError("both matrices must be square and have the same size")


def _split_matrix(matrix: Matrix) -> Tuple[Matrix, Matrix, Matrix, Matrix]:
    middle = len(matrix) // 2
    return (
        [row[:middle] for row in matrix[:middle]],
        [row[middle:] for row in matrix[:middle]],
        [row[:middle] for row in matrix[middle:]],
        [row[middle:] for row in matrix[middle:]],
    )


def _matrix_add(first: Matrix, second: Matrix) -> Matrix:
    return [[first[row][column] + second[row][column] for column in range(len(first))] for row in range(len(first))]


def _naive_matrix_multiply(first: Matrix, second: Matrix) -> Matrix:
    size = len(first)
    return [
        [sum(first[row][middle] * second[middle][column] for middle in range(size)) for column in range(size)]
        for row in range(size)
    ]


# Problem 3
def recursive_reverse(values: Sequence[T]) -> List[T]:
    """Reverse a sequence by recursively reversing its halves."""
    if len(values) <= 1:
        return list(values)
    middle = len(values) // 2
    return recursive_reverse(values[middle:]) + recursive_reverse(values[:middle])


# Problem 4
def smallest_missing_non_negative(values: Sequence[int]) -> int:
    """Find the smallest missing non-negative integer in sorted distinct values.

    If values[mid] equals mid, all smaller positions are present; otherwise a
    missing value exists at or before mid. This binary search takes O(log n).
    """
    low, high = 0, len(values)
    while low < high:
        middle = (low + high) // 2
        if values[middle] == middle:
            low = middle + 1
        else:
            high = middle
    return low


# Problem 6
def majority_element(values: Sequence[T]) -> T | None:
    """Return a value occurring more than n/2 times, or None, in O(n log n).

    Each recursive half returns only its possible majority. The combine phase
    counts the two candidates over the current interval in linear time.
    """
    def solve(start: int, end: int) -> T | None:
        if start >= end:
            return None
        if end - start == 1:
            return values[start]
        middle = (start + end) // 2
        left_candidate = solve(start, middle)
        right_candidate = solve(middle, end)
        if left_candidate == right_candidate:
            return left_candidate
        for candidate in (left_candidate, right_candidate):
            if candidate is not None:
                occurrences = sum(value == candidate for value in values[start:end])
                if occurrences > (end - start) // 2:
                    return candidate
        return None

    return solve(0, len(values))


# Problem 7
def count_inversions(values: Sequence[T]) -> int:
    """Count inversions by merge sort in O(n log n) time."""
    def sort_and_count(items: Sequence[T]) -> Tuple[List[T], int]:
        if len(items) <= 1:
            return list(items), 0
        middle = len(items) // 2
        left, left_count = sort_and_count(items[:middle])
        right, right_count = sort_and_count(items[middle:])
        merged: List[T] = []
        index_left = index_right = 0
        split_count = 0
        while index_left < len(left) and index_right < len(right):
            if left[index_left] <= right[index_right]:
                merged.append(left[index_left])
                index_left += 1
            else:
                merged.append(right[index_right])
                split_count += len(left) - index_left
                index_right += 1
        merged.extend(left[index_left:])
        merged.extend(right[index_right:])
        return merged, left_count + right_count + split_count

    return sort_and_count(values)[1]


# Problem 8 (Challenge)
def consistent_triplet_count(first_ranking: Sequence[T], second_ranking: Sequence[T]) -> int:
    """Count consistent ranking triplets in O(n log n) time.

    Convert A into B-ranks: ``positions[i]`` is the B position of contestant
    ``A[i]``. A consistent triplet is then an increasing triple in positions.
    Divide-and-conquer merge counting calculates, for each middle contestant,
    how many smaller values occur on its left and how many greater values occur
    on its right; the product is its contribution.
    """
    if len(first_ranking) != len(second_ranking) or set(first_ranking) != set(second_ranking):
        raise ValueError("both rankings must contain the same contestants exactly once")

    position_in_second = {contestant: index for index, contestant in enumerate(second_ranking)}
    positions = [position_in_second[contestant] for contestant in first_ranking]
    smaller_left = _smaller_values_on_left(positions)
    reversed_negated = [-value for value in reversed(positions)]
    greater_right = list(reversed(_smaller_values_on_left(reversed_negated)))
    return sum(left * right for left, right in zip(smaller_left, greater_right))


def _smaller_values_on_left(values: Sequence[int]) -> List[int]:
    """Use merge-sort recursion to count earlier values strictly smaller than each value."""
    counts = [0] * len(values)
    indexed = [(value, index) for index, value in enumerate(values)]

    def sort_and_count(items: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        if len(items) <= 1:
            return items
        middle = len(items) // 2
        left = sort_and_count(items[:middle])
        right = sort_and_count(items[middle:])
        result: List[Tuple[int, int]] = []
        left_index = right_index = smaller_count = 0
        while right_index < len(right):
            while left_index < len(left) and left[left_index][0] < right[right_index][0]:
                result.append(left[left_index])
                left_index += 1
                smaller_count += 1
            value, original_index = right[right_index]
            counts[original_index] += smaller_count
            result.append((value, original_index))
            right_index += 1
        result.extend(left[left_index:])
        return result

    sort_and_count(indexed)
    return counts


if __name__ == "__main__":
    assert merge_sort([5, 8, 2, 0, 23, 786, -2, 65]) == [-2, 0, 2, 5, 8, 23, 65, 786]
    assert matrix_multiply_divide_conquer([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]
    assert recursive_reverse([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]
    assert smallest_missing_non_negative([0, 1, 3, 5, 7]) == 2
    assert majority_element(["a", "b", "a", "a", "c", "a"]) == "a"
    assert majority_element([1, 2, 3, 4]) is None
    assert count_inversions([2, 4, 1, 3, 5]) == 3
    assert consistent_triplet_count(["a", "b", "c", "d"], ["b", "a", "c", "d"]) == 2
    print("Tutorial 11 divide-and-conquer checks passed.")

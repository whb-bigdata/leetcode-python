"""
COMP9123 - 2026S2 - Assignment 3
Q1. Freight Optimisation

Problem:
Given an array of crate weights and an array of truck payload capacities, determine the minimum total weight of crates that cannot dispatched.

"""


def min_outsourced_weight(crates: list[int], trucks: list[int]) -> int:
    """
    Calculates the minimum total weight of crates that must be outsourced.

    :param crates: A list of integers representing crate weights.
    :param trucks: A list of integers representing truck payload capacities.
    :return: An integer representing the total weight left undispatched.
    """
    # TODO: Implement your greedy algorithm here
    crates = sorted(crates, reverse=True)
    trucks = sorted(trucks, reverse=True)
    trucks_index = 0
    crates_index = 0
    sum_weight = 0

    while trucks_index < len(trucks) and crates_index < len(crates):
        if trucks[trucks_index] >= crates[crates_index]:
            trucks_index += 1
            crates_index += 1
        else:
            sum_weight += crates[crates_index]
            crates_index += 1
    sum_weight += sum(crates[crates_index:])
    return sum_weight
# ------------------
# MAIN PROGRAM
# ------------------

# You can use the block below to test your code
# Hit the "Run" button to execute this file and see the output of your own test cases. When you are ready to submit, hit the "Mark" button to run the official test cases and submit your solution.

if __name__ == "__main__":
    print("Running custom test cases...")

    # Feel free to modify the test cases in for your own debugging purposes.
    test_cases = [
        {
            "name": "Standard Example",
            "crates": [350, 750, 450, 850],
            "trucks": [550, 250, 850, 450],
            "expected": 750
        },
        {
            "name": "All Crates Dispatched",
            "crates": [250, 150, 400],
            "trucks": [400, 150, 250],
            "expected": 0
        },
        {
            "name": "No Trucks Available",
            "crates": [300, 700, 200],
            "trucks": [],
            "expected": 1200
        },
        {
            "name": "Trucks Too Small",
            "crates": [800, 1200],
            "trucks": [750, 600, 790, 799],
            "expected": 2000
        },
        {
            "name": "More Trucks Than Crates",
            "crates": [650],
            "trucks": [200, 700, 900, 50],
            "expected": 0
        }
    ]

    for i, test in enumerate(test_cases):
        crates_copy = test["crates"][:]
        trucks_copy = test["trucks"][:]

        result = min_outsourced_weight(crates_copy, trucks_copy)

        if result == test["expected"]:
            print(f"Test {i + 1} Passed: {test['name']}")
        else:
            print(f"Test {i + 1} Failed: {test['name']}")
            print(f"   Input Crates: {test['crates']}")
            print(f"   Input Trucks: {test['trucks']}")
            print(f"   Expected Output: {test['expected']}")
            print(f"   Your Output:     {result}")
        print("-" * 40)

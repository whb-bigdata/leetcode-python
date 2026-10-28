# This file contains the scaffold code for Q2. Do not modify this file.

class EncryptedPacket:
    def __init__(self, source_id: str, size: int):
        self._source_id = source_id
        self.size = size

    __hash__ = None  # type: ignore

    def __lt__(self, other):
        raise TypeError("EncryptedPackets cannot be sorted.")
# a = EncryptedPacket('A', 0)
# print(a._source_id)

def is_same_source(packet_A: EncryptedPacket, packet_B: EncryptedPacket) -> bool:
    """Returns True if both packets come from the same source."""
    return packet_A._source_id == packet_B._source_id


"""
COMP9123 - 2026S2 - Assignment 3
Q2. Bandwidth Hog

Problem:
Given a traffic log of encrypted packets, identify the source that takes up more than 50% of the total bandwidth usage. If no such source exists, return None.

"""



def find_bandwidth_hog(traffic_log: list[EncryptedPacket]) -> EncryptedPacket | None:
    """
    Finds the bandwidth hog source using Divide and Conquer.

    :param traffic_log: A list of EncryptedPacket objects.
    :return: An EncryptedPacket from the hog source, or None.
    """
    # TODO: Implement your divide-and-conquer solution here.

    # The comments below are hints to help you develop your solution if you're stuck. You don't have to follow them exactly, and you can remove them if you don't find them useful.

    # 1. What is the base case?

    # 2. Where do you divide? You will need to assign the sub-arrays to variables so that you can pass them into the recursive calls.

    # 3. Recursion: You will need variables to store the results of the recursive calls.

    # 4. How do you combine the results? What do you need to check? Look for hints in the test cases below in the MAIN PROGRAM section.

    if len(traffic_log) == 0:
        return None

    if len(traffic_log) == 1:
        return traffic_log[0]

    mid = len(traffic_log) // 2

    left_result = find_bandwidth_hog(traffic_log[:mid])
    right_result = find_bandwidth_hog(traffic_log[mid:])

    if left_result is not None and right_result is not None:
        if is_same_source(left_result, right_result):
            return left_result
    weight_left = 0
    weight_right = 0
    total_weight = 0

    for packet in traffic_log:
        total_weight += packet.size
        if left_result is not None and is_same_source(packet, left_result):
            weight_left += packet.size
        if right_result is not None and is_same_source(packet, right_result):
            weight_right += packet.size

    if left_result is not None and weight_left * 2 > total_weight:
        return left_result
    if right_result is not None and weight_right * 2 > total_weight:
        return right_result

    return None






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
            "name": "Standard Hog",
            "log": [EncryptedPacket('A', 15), EncryptedPacket('B', 70), EncryptedPacket('C', 20),
                    EncryptedPacket('B', 35), EncryptedPacket('A', 5)],
            "expected_source": 'B'
        },
        {
            "name": "Frequency vs Weight Trap",
            "log": [EncryptedPacket('B', 80), EncryptedPacket('A', 3), EncryptedPacket('A', 3), EncryptedPacket('A', 3),
                    EncryptedPacket('A', 3), EncryptedPacket('A', 3)],
            "expected_source": 'B'
        },
        {
            "name": "Exactly 50 Percent (No Hog)",
            "log": [EncryptedPacket('A', 30), EncryptedPacket('B', 20), EncryptedPacket('C', 10)],
            "expected_source": None
        },
        {
            "name": "Cross-Boundary Split",
            "log": [EncryptedPacket('A', 40), EncryptedPacket('B', 30), EncryptedPacket('C', 10),
                    EncryptedPacket('D', 20), EncryptedPacket('A', 40)],
            "expected_source": 'A'
        },
        {
            "name": "No Hog (All distinct)",
            "log": [EncryptedPacket('A', 25), EncryptedPacket('B', 30), EncryptedPacket('C', 20),
                    EncryptedPacket('D', 15), EncryptedPacket('E', 10)],
            "expected_source": None
        },
        {
            "name": "Single Element Base Case",
            "log": [EncryptedPacket('K', 42)],
            "expected_source": 'K'
        }
    ]

    for i, test in enumerate(test_cases):
        log_copy = test["log"][:]

        result = find_bandwidth_hog(log_copy)

        is_correct = False
        if test["expected_source"] is None:
            is_correct = (result is None)
        else:
            expected_dummy = EncryptedPacket(test["expected_source"], 0)
            is_correct = (result is not None) and is_same_source(result, expected_dummy)

        if is_correct:
            print(f"Test {i + 1} Passed: {test['name']}")
        else:
            print(f"Test {i + 1} Failed: {test['name']}")
            print(f"   Expected: {test['expected_source']}")
            returned_val = getattr(result, 'source', 'Unknown Packet') if result else None
            print(f"   Your Result:     {returned_val}")
        print("-" * 50)
"""
COMP9123 Data Structures and Algorithms
Assignment 2 -- Question 3: Priority Task Scheduler via a Binary Min-Heap

Scaffold file. The ONLY file you need to edit is this one.

You must implement the three methods marked with TODO:
    _sift_up, _sift_down, build_heap

You are allowed to add extra helper methods if you wish, but please do
not modify any of the other provided methods, as this may break the
autograder.

A task is represented as a tuple (priority, name), where a SMALLER
priority number means a MORE URGENT task. The heap is stored as a
plain Python list self.data, satisfying the array representation of a
binary min-heap covered in lectures:

    - the children of the task at index i are at indices 2*i + 1 and
      2*i + 2 (if they exist)
    - the parent of the task at index i (for i > 0) is at index
      (i - 1) // 2
    - every task's priority is <= the priorities of both its children
"""


class MinHeap:

    def __init__(self):
        self.data = []

    # ------------------------------------------------------------------
    # Provided helper methods -- please do not modify
    # ------------------------------------------------------------------

    def size(self):
        """Return the number of tasks currently in the heap."""
        return len(self.data)

    def is_empty(self):
        """Return True iff the heap contains no tasks."""
        return len(self.data) == 0

    def peek_min(self):
        """Return (without removing) the most urgent task, i.e. the
        task with the smallest priority. O(1) time."""
        if self.is_empty():
            raise IndexError("peek_min() called on an empty heap")
        return self.data[0]

    def insert(self, priority, name):
        """Add a new task (priority, name) to the heap."""
        self.data.append((priority, name))
        self._sift_up(len(self.data) - 1)

    def extract_min(self):
        """Remove and return the most urgent task (smallest priority)."""
        if self.is_empty():
            raise IndexError("extract_min() called on an empty heap")
        min_task = self.data[0]
        last_task = self.data.pop()          # remove last element
        if not self.is_empty():
            self.data[0] = last_task
            self._sift_down(0)
        return min_task

    @staticmethod
    def _parent(i):
        return (i - 1) // 2

    @staticmethod
    def _left(i):
        return 2 * i + 1

    @staticmethod
    def _right(i):
        return 2 * i + 2

    # ------------------------------------------------------------------
    # Methods you need to implement
    # ------------------------------------------------------------------

    def _sift_up(self, i):
        """
        The task at index i may have a smaller priority than its
        parent, violating the min-heap property. Repeatedly swap it
        with its parent until the min-heap property is restored (or
        it reaches the root, index 0).

        This is called once, from insert(), on the index of the
        newly-appended task.
        """
        # TODO: implement this method
        while i >0 :
            parent_index = self._parent(i)
            if self.data[parent_index][0] <= self.data[i][0]:
                break
            self.data[parent_index],self.data[i]  = (self.data[i]
            , self.data[parent_index])
            i = parent_index


    def _sift_down(self, i):
        """
        The task at index i may have a LARGER priority than one (or
        both) of its children, violating the min-heap property.
        Repeatedly swap it with the smaller of its two children until
        the min-heap property is restored (or it reaches a position
        with no children).

        This is called once, from extract_min(), on index 0 (the
        root), after the last task has been moved there.

        It is also required by build_heap() below -- make sure your
        implementation works correctly when called on an arbitrary
        index i (only assume the subtrees rooted at i's children are
        already valid heaps).
        """
        # TODO: implement this method
        n = self.size()
        while True:
            left_index = self._left(i)
            right_index = self._right(i)
            smallest = i

            if left_index < n and self.data[left_index][0] < self.data[smallest][0]:
                smallest = left_index

            if right_index < n and self.data[right_index][0] < self.data[smallest][0]:
                smallest = right_index

            if smallest == i:
                    break
            self.data[i],self.data[smallest] = (self.data[smallest]
             ,self.data[i])

            i = smallest

    def build_heap(self, tasks):
        """
        Replace the contents of this heap with the given list of
        (priority, name) tasks, rearranged into a valid min-heap.

        `tasks` is a plain, unordered list -- it is NOT assumed to
        already satisfy the heap property.

        Your implementation MUST run in O(n) time overall, where
        n = len(tasks). In particular, calling insert() once per task
        (which would take O(n log n) time overall) will NOT receive
        full marks -- use the standard bottom-up heap-construction
        algorithm instead, which relies on _sift_down().
        """
        # TODO: implement this method
        self.data = list(tasks)

        for i in range(self.size() // 2 - 1, -1 , -1):
            self._sift_down(i)

# ----------------------------------------------------------------------
# Example usage / manual testing (this main method is not marked)
# ----------------------------------------------------------------------

def main():
    heap = MinHeap()
    for priority, name in [(5, "Backup"), (1, "SecurityAlert"),
                            (3, "EmailDigest"), (2, "PatchUpdate")]:
        heap.insert(priority, name)

    print("Most urgent task:", heap.peek_min())
    print("Tasks in priority order:")
    while not heap.is_empty():
        print(" ", heap.extract_min())

    print()
    print("Building a heap directly from an unordered list:")
    heap2 = MinHeap()
    heap2.build_heap([(9, "Cleanup"), (4, "ReportGen"), (7, "Sync"),
                       (1, "FireAlarm"), (6, "Archive"), (2, "Deploy")])
    print("Most urgent task after build_heap:", heap2.peek_min())
    while not heap2.is_empty():
        print(" ", heap2.extract_min())


if __name__ == "__main__":
    main()

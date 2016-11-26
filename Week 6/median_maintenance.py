import heapq
import math


class MedianMaintainer:
    def __init__(self):
        self.__lo_heap = LoHeap()
        self.__hi_heap = HiHeap()
        self.__median = 0
        self.__difference = 0

    def add(self, number):
        if number < self.__lo_heap.max:  # goes to the lower half
            self.__lo_heap.push(number)
            self.__difference += 1
        elif number > self.__hi_heap.min:  # goes to the upper half
            self.__hi_heap.push(number)
            self.__difference -= 1
        else:  # wedged in between, by default to the lower
            self.__lo_heap.push(number)
            self.__difference += 1
        if self.__difference > 1:  # we've pushed into lo heap twice
            self.__hi_heap.push(self.__lo_heap.pop())
            self.__difference = 0
        elif self.__difference < -1:  # we've pushed into hi heap twice
            self.__lo_heap.push(self.__hi_heap.pop())
            self.__difference = 0
        candidate = self.__lo_heap.max if self.__difference >= 0 else self.__hi_heap.min
        self.__median = (self.__median + candidate) % 10000

    @property
    def median_sum(self):
        return self.__median


class LoHeap:
    """
    a max-heap to store the lower half of the numbers
    push and pop in O(log(n)) time
    if the 2 heaps are balanced, max property returns the median
    """
    def __init__(self):
        self.__heap = []

    def push(self, number):
        heapq.heappush(self.__heap, - number)

    def pop(self):
        return - heapq.heappop(self.__heap)

    @property
    def max(self):
        """
        if the 2 heaps are balanced, max property returns the median
        :return: int
        """
        if self.__heap:
            return - self.__heap[0]
        else:
            return math.inf


class HiHeap:
    """
    a min-heap to store the upper half of the numbers
    push and pop in O(log(n)) time
    """
    def __init__(self):
        self.__heap = []

    def push(self, number):
        heapq.heappush(self.__heap, number)

    def pop(self):
        return heapq.heappop(self.__heap)

    @property
    def min(self):
        if self.__heap:
            return self.__heap[0]
        else:
            return 0


if __name__ == '__main__':
    maintainer = MedianMaintainer()
    # load data
    with open('median.txt') as data:
        for line in data:
            raw = line.strip()
            if raw:
                maintainer.add(int(raw))
    print('Sum of medians is {0}'.format(maintainer.median_sum))


class IndexMinPQ:
    """
    A minimum-oriented indexed priority queue, implemented using a binary heap array.

    Note that operations are only guaranteed to work with indices less than the maximum size
    that is specified in the constructor. The maximum size can be changed using resize(k),
    which can expand or shrink (truncate) the queue.

    Constructor uses worst case time complexity of O(N), then most operations are O(logN)
    Uses extra space proportional to N
    """

    def __init__(self, max_n):
        """ Constructor
        Worst case time complexity of O(N)

        :param max_n: array length of priority queue (maximum index + 1)
        """
        self._max_n = max_n
        self.__pq = [0] * (max_n + 1)
        self.__qp = [-1] * (max_n + 1)
        self.__keys = [None] * (max_n + 1)
        self.__n = 0

    def empty(self):
        """ Test if queue is empty
        Worst case time complexity of O(1)

        :return: true if empty, false otherwise
        """
        return self.__n == 0

    def contains(self, i):
        """ Test if queue contains element at index i
        Worst case time complexity of O(1)

        :param i: index
        :return: true if index has element, false if empty
        """
        return self.__qp[i] != -1

    def insert(self, i, key):
        """ Insert key in queue at index i
        Worst case time complexity of O(logN)

        :param i: index
        :param key: item to insert
        :return:
        """
        if self.contains(i):
            raise IndexError("index is already in pq")
        self.__n += 1
        self.__pq[self.__n] = i
        self.__qp[i] = self.__n
        self.__keys[i] = key
        self.__swim(self.__n)

    def min_key(self):
        """ Get item with minimum priority
        Worst case time complexity of O(1)

        :return: smallest item in queue
        """
        return self.__keys[self.__pq[1]]

    def min_index(self):
        """ Get index of item with minimum priority
        Worst case time complexity of O(1)

        :return: index of smallest item in queue
        """
        return self.__pq[1]

    def del_min(self):
        """ Remove item with minimum priority and return its index
        Worst case time complexity of O(logN)

        :return: smallest item in queue
        """
        min_idx = self.__pq[1]
        self.__swap(1, self.__n)
        self.__n -= 1
        self.__sink(1)
        self.__keys[self.__pq[self.__n + 1]] = None
        self.__qp[self.__pq[self.__n + 1]] = -1
        return min_idx

    def delete(self, i):
        """ Remove item at index i
        Worst case time complexity of O(logN)

        :param i: index of item to delete
        :return:
        """
        pq_idx = self.__qp[i]
        self.__swap(pq_idx, self.__n)
        self.__n -= 1
        self.__swim(pq_idx)
        self.__sink(pq_idx)
        self.__keys[i] = None
        self.__qp[i] = -1

    def change_key(self, i, key):
        """ Change value of item at index i
        Worst case time complexity of O(logN)

        :param i: index
        :param key: item/value to change
        :return:
        """
        self.__keys[i] = key
        self.__swim(self.__qp[i])
        self.__sink(self.__qp[i])

    def get_key(self, i):
        return self.keys[i]

    def resize(self, cap):
        """ Change the maximum index of the priority queue
            Note that decreasing the size will truncate the queue and delete elements
        Worst case time complexity of O(N)

        :param cap: new size (maximum index + 1)
        :return:
        """
        temp_pq = [0] * (cap + 1)
        temp_qp = [-1] * (cap + 1)
        temp_keys = [None] * (cap + 1)
        for i in range(cap + 1):
            temp_pq[i] = self.__pq[i]
            temp_qp[i] = self.__qp[i]
            temp_keys[i] = self.__keys[i]
        self.__pq = temp_pq
        self.__qp = temp_qp
        self.__keys = temp_keys
        self._max_n = cap
        if self.__n > self._max_n:
            self.__n = self._max_n

    def __greater(self, i, j):
        return self.__keys[self.__pq[i]] > self.__keys[self.__pq[j]]

    def __swap(self, i, j):
        temp = self.__pq[i]
        self.__pq[i] = self.__pq[j]
        self.__pq[j] = temp
        self.__qp[self.__pq[i]] = i
        self.__qp[self.__pq[j]] = j

    def __swim(self, k):
        while k > 1 and self.__greater(k // 2, k):
            self.__swap(k // 2, k)
            k = k//2

    def __sink(self, k):
        while 2*k <= self.__n:
            j = 2*k
            if j < self.__n and self.__greater(j, j + 1):
                j += 1
            if not self.__greater(k, j):
                break
            self.__swap(k, j)
            k = j

    def __len__(self):
        return self.__n

    def __str__(self):
        return str([self.__pq[i] for i in range(1, self.__n+1)])

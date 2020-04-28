from LinkedListST import LinkedListST


class HashDict:
    """
    Dictionary implemented using hash table with separate chaining.
    Separate chains are implemented as linked lists nested in a Python list
    Array resizing is performed automatically to maintain constant-time performance in core functions

    Constructor runs with worst case time complexity of O(m), then most operations are O(1)
    Uses extra space proportional to N + m
    """

    def __init__(self, m=997):
        """Initialize hash table dictionary with m bins
        Worst case time complexity of O(m)

        :param m: the number of bins
        """
        self._m = m
        self.__table = [LinkedListST() for i in range(m)]
        self.__len = 0

    def get(self, key):
        """Return item associated with key, or None if key not found
        Worst case time complexity is O(N/m), which is effectively O(1)

        :param key: key that uniquely identifies item
        :return: item
        """
        return self.__table[self.__hash_bin(key)].get(key)

    def put(self, key, value):
        """Add key-value pair to dictionary, or replace value if key is already in dictionary
        Worst case time complexity is O(N/m), which is effectively O(1)

        :param key: key
        :param value: value
        :return:
        """
        self.__len += 1
        if len(self) >= 8 * self._m:
            self.__resize(2 * self._m)
        self.__table[self.__hash_bin(key)].put(key, value)

    def delete(self, key):
        """Remove and return item associated with key from dict
        Worst case time complexity is O(N/m), which is effectively O(1)

        :param key: key
        :return: deleted item
        """
        self.__len -= 1
        if 0 < len(self) <= 2 * self._m:
            self.__resize(self._m // 2)
        return self.__table[self.__hash_bin(key)].delete(key)

    def keys(self):
        """Return list of all keys in dictionary
        Worst case time complexity is O(N)

        :return: list of keys
        """
        return [key for lst in self.__table for key, val in lst]

    def values(self):
        """Return list of all values in dictionary
        Worst case time complexity is O(N)

        :return: list of values
        """
        return [val for lst in self.__table for key, val in lst]

    def __hash_bin(self, key):
        """Convert hash function to hash table bin

        :param key: key
        :return:
        """
        return hash(key) % self._m

    def __resize(self, cap):
        """ resize hash table with more bins

        :param cap: new number of bins, m
        :return:
        """
        temp = HashDict(cap)
        for key in self.keys():
            temp.put(key, self.get(key))
        self.__table = temp.__table
        self._m = cap

    def __len__(self):
        return self.__len

    def __iter__(self):
        return zip(self.keys(), self.values())


class LinkedListST:
    """
    Symbol table implemented as unordered linked list

    Most operations have worst case time complexity of O(N)
    Uses extra space proportional to N
    """

    def __init__(self):
        """ Constructor
        Worst case time complexity of O(1)

        """
        self.__head = None
        self.__len = 0

    def get(self, key):
        """Return item associated with key, or None if key not found
        Worst case time complexity is O(N)

        :param key: key that uniquely identifies item
        :return: item
        """
        current = self.__head
        while current is not None:
            if current.key == key:
                return current.val
            current = current.next
        return None

    def put(self, key, value):
        """Add key-value pair to list, or replace value if key is already in list
        Worst case time complexity is O(N)

        :param key: key
        :param value: value
        :return:
        """
        current = self.__head
        while current is not None:
            if current.key == key:
                current.val = value
                return
            current = current.next
        self.__head = self.Node(key, value, self.__head)
        self.__len += 1

    def delete(self, key):
        """Remove and return item associated with key from list
        Worst case time complexity is O(N)

        :param key: key
        :return: deleted item
        """
        item = None
        # check if head is item
        if self.__head.key == key:
            item = self.__head.val
            self.__head = self.__head.next
        # iterate through list
        else:
            current = self.__head
            while current.next is not None:
                if current.next.key == key:
                    item = current.next.val
                    current.next = current.next.next
                current = current.next
        self.__len -= 1
        return item

    def __len__(self):
        return self.__len

    def __iter__(self):
        return self.LinkedListIterator(self.__head)

    class Node:
        def __init__(self, key=None, val=None, next=None):
            self.key = key
            self.val = val
            self.next = next

    class LinkedListIterator:

        def __init__(self, first):
            self.current = first

        def __iter__(self):
            return self

        def __next__(self):
            if self.current is None:
                raise StopIteration
            else:
                key = self.current.key
                val = self.current.val
                self.current = self.current.next
                return key, val

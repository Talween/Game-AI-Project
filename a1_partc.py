class Stack:
    def __init__(self, cap=10):
        """
        Initialize a stack with a given capacity.
        :param cap: The initial capacity of the stack.
        """
        self._data = [None] * cap
        self._capacity = cap
        self._size = 0

    def capacity(self):
        """
        Get the current capacity of the stack.
        :return: The capacity of the stack.
        """
        return self._capacity

    def push(self, data):
        """
        Push a new element onto the stack.
        :param data: The data to push onto the stack.
        """
        if self._size == self._capacity:
            self._resize()
        self._data[self._size] = data
        self._size += 1

    def pop(self):
        """
        Pop the top element from the stack.
        :return: The data from the top element.
        :raises IndexError: If the stack is empty.
        """
        if self._size == 0:
            raise IndexError('pop() used on empty stack')
        value = self._data[self._size - 1]
        self._size -= 1
        return value

    def get_top(self):
        """
        Get the top element of the stack without removing it.
        :return: The top element of the stack, or None if the stack is empty.
        """
        if self._size == 0:
            return None
        return self._data[self._size - 1]

    def is_empty(self):
        """
        Check if the stack is empty.
        :return: True if the stack is empty, False otherwise.
        """
        return self._size == 0

    def __len__(self):
        """
        Get the number of elements in the stack.
        :return: The number of elements in the stack.
        """
        return self._size

    def _resize(self):
        """
        Resize the stack to double its current capacity.
        """
        new_capacity = self._capacity * 2
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity


class Queue:
    def __init__(self, cap=10):
        """
        Initialize a queue with a given capacity.
        :param cap: The initial capacity of the queue.
        """
        self._data = [None] * cap
        self._capacity = cap
        self._size = 0
        self._front = 0
        self._back = -1

    def capacity(self):
        """
        Get the current capacity of the queue.
        :return: The capacity of the queue.
        """
        return self._capacity

    def enqueue(self, data):
        """
        Add an element to the back of the queue.
        :param data: The data to add to the queue.
        """
        if self._size == self._capacity:
            self._resize()
        self._back = (self._back + 1) % self._capacity
        self._data[self._back] = data
        self._size += 1

    def dequeue(self):
        """
        Remove and return the front element of the queue.
        :return: The data from the front element.
        :raises IndexError: If the queue is empty.
        """
        if self._size == 0:
            raise IndexError('dequeue() used on empty queue')
        value = self._data[self._front]
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return value

    def get_front(self):
        """
        Get the front element of the queue without removing it.
        :return: The front element of the queue, or None if the queue is empty.
        """
        if self._size == 0:
            return None
        return self._data[self._front]

    def is_empty(self):
        """
        Check if the queue is empty.
        :return: True if the queue is empty, False otherwise.
        """
        return self._size == 0

    def __len__(self):
        """
        Get the number of elements in the queue.
        :return: The number of elements in the queue.
        """
        return self._size

    def _resize(self):
        """
        Resize the queue to double its current capacity.
        """
        new_capacity = self._capacity * 2
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._front + i) % self._capacity]
        self._data = new_data
        self._front = 0
        self._back = self._size - 1
        self._capacity = new_capacity


class Deque:
    def __init__(self, cap=10):
        """
        Initialize a deque with a given capacity.
        :param cap: The initial capacity of the deque.
        """
        self._data = [None] * cap
        self._capacity = cap
        self._size = 0
        self._front = 0
        self._back = -1

    def capacity(self):
        """
        Get the current capacity of the deque.
        :return: The capacity of the deque.
        """
        return self._capacity

    def push_front(self, data):
        """
        Add an element to the front of the deque.
        :param data: The data to add to the front of the deque.
        """
        if self._size == self._capacity:
            self._resize()
        self._front = (self._front - 1 + self._capacity) % self._capacity
        self._data[self._front] = data
        self._size += 1

    def pop_front(self):
        """
        Remove and return the front element of the deque.
        :return: The data from the front element.
        :raises IndexError: If the deque is empty.
        """
        if self._size == 0:
            raise IndexError('pop_front() used on empty deque')
        value = self._data[self._front]
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return value

    def push_back(self, data):
        """
        Add an element to the back of the deque.
        :param data: The data to add to the back of the deque.
        """
        if self._size == self._capacity:
            self._resize()
        self._back = (self._back + 1) % self._capacity
        self._data[self._back] = data
        self._size += 1

    def pop_back(self):
        """
        Remove and return the back element of the deque.
        :return: The data from the back element.
        :raises IndexError: If the deque is empty.
        """
        if self._size == 0:
            raise IndexError('pop_back() used on empty deque')
        value = self._data[self._back]
        self._back = (self._back - 1 + self._capacity) % self._capacity
        self._size -= 1
        return value

    def get_front(self):
        """
        Get the front element of the deque without removing it.
        :return: The front element of the deque, or None if the deque is empty.
        """
        if self._size == 0:
            return None
        return self._data[self._front]

    def get_back(self):
        """
        Get the back element of the deque without removing it.
        :return: The back element of the deque, or None if the deque is empty.
        """
        if self._size == 0:
            return None
        return self._data[self._back]

    def is_empty(self):
        """
        Check if the deque is empty.
        :return: True if the deque is empty, False otherwise.
        """
        return self._size == 0

    def __len__(self):
        """
        Get the number of elements in the deque.
        :return: The number of elements in the deque.
        """
        return self._size

    def __getitem__(self, k):
        """
        Get the element at the k-th position in the deque.
        :param k: The index of the element to retrieve.
        :return: The element at the k-th position.
        :raises IndexError: If the index is out of range.
        """
        if k < 0 or k >= self._size:
            raise IndexError('Index out of range')
        return self._data[(self._front + k) % self._capacity]

    def _resize(self):
        """
        Resize the deque to double its current capacity.
        """
        new_capacity = self._capacity * 2
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._front + i) % self._capacity]
        self._data = new_data
        self._front = 0
        self._back = self._size - 1
        self._capacity = new_capacity

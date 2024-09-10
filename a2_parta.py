class HashTable:
	def __init__(self, initial_capacity=32):  # Initialize the HashTable with a default capacity of 32
		self.cap = initial_capacity  # Set the capacity of the HashTable
		self.my_list = [None] * self.cap  # Create an empty list of size equal to the capacity

	def insert(self, key, value):
		# Check if the key already exists in the HashTable
		for i in range(self.cap):
			if self.my_list[i] is not None and self.my_list[i][0] == key:
				return False  # Key already exists, return False
		
		# Insert the key-value pair into the HashTable
		self.just_insert(key, value)
		
		# Check the load factor and rehash if necessary
		if len([slot for slot in self.my_list if slot is not None]) / self.cap > 0.7:
			self.rehash_and_insert()  # Rehash the HashTable and insert the key-value pair
		
		return True  # Return True after successful insertion

	def rehash_and_insert(self):
		# Create a copy of the current list and capacity
		copy_list = self.my_list

		# Double the capacity of the HashTable
		self.cap *= 2
		self.my_list = [None] * self.cap

		# Reinsert all elements from the copy list
		for item in copy_list:
			if item is not None:
				key, value = item
				self.just_insert(key, value)

	def just_insert(self, key, value):
		hash_value = hash(key)  # Compute the hash value of the key
		hash_index = hash_value % self.cap  # Compute the hash index using modulo operator

		# Linear probing to find an empty slot in the HashTable
		for i in range(self.cap):
			index = (hash_index + i) % self.cap
			if self.my_list[index] is None:
				self.my_list[index] = [key, value]  # Insert the key-value pair into the empty slot
				break

	def modify(self, key, value):
		for i in range(self.cap):
			slot = self.my_list[i]
			if slot is not None and slot[0] == key:
				self.my_list[i][1] = value  # Modify the value associated with the key
				return True  # Return True after successful modification
		return False  # Key not found, return False

	def remove(self, key):
		for i in range(self.cap):
			slot = self.my_list[i]
			if slot is not None and slot[0] == key:
				self.my_list[i] = None  # Remove the key-value pair from the HashTable
				return True  # Return True after successful removal
		return False  # Key not found, return False

	def search(self, key):
		for i in range(self.cap):
			slot = self.my_list[i]
			if slot is not None and slot[0] == key:
				return slot[1]  # Return the value associated with the key
		return None  # Key not found, return None

	def count_occupied_slots(self):
		return len([slot for slot in self.my_list if slot is not None])  # Count the number of occupied slots in the HashTable

	def capacity(self):
		return self.cap  # Return the total capacity of the HashTable

	def __len__(self):
		return self.count_occupied_slots()  # Return the number of occupied slots in the HashTable
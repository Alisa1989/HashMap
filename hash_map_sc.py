# Name: Alexandre Steinhauslin
# OSU Email: steinhal@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: HashMap Implementation
# Due Date: 8/15/2023
# Description: using a dynamic array to store the hash table and implementing
# chaining for collision resolution using a singly linked list.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Receives Key and Value
        Updates existing value if the key already exists
        Creates a new key/value pair if the key doesn't exist
        """
        if self. table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        mapped_index = self._hash_function(key) % self._capacity

        for i in self._buckets[mapped_index]:           # if the key exists substitute the value
            if i.key == key:
                i.value = value
                return

        self._buckets[mapped_index].insert(key, value)
        # print("in put k=", key, "v=", value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        counter = 0
        for index in range(self._capacity):
            if self._buckets[index].length() == 0:
                counter += 1
        return counter

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears content of Hash Table
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:          # PASSES local tests
        """
        Receives new_capacity
        Changes the capacity of the internal hash table
        """
        if new_capacity < 1:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # OPTION 1
        # make a hash map out of the new_array
        # new_array = DynamicArray()
        # new_size = 0
        # for _ in range(new_capacity):
        #     new_array.append(LinkedList())
        #
        # for index in range(self._capacity):
        #     if self._buckets[index].length() != 0:
        #         for j in self._buckets[index]:
        #             # print(" j = ", j, " k = ", j.key, " v= ", j.value)
        #             # new_array.append((j.key, j.value))
        #             mapped_index = self._hash_function(j.key) % new_capacity
        #             new_array[mapped_index].insert(j.key, j.value)
        #             new_size += 1
        #
        # self._buckets = new_array
        # self._capacity = new_capacity
        # self._size = new_size

        # # OPTION 2
        # transfer over key/values and rehash
        # copy
        existing_pairs = self.get_keys_and_values()              # too expensive
        # change size
        self._capacity = new_capacity
        self._size = 0
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        for i in range(existing_pairs.length()):
            # print("in resize table, key:", existing_pairs[i][0], "value:", existing_pairs[i][1])
            self.put(existing_pairs[i][0], existing_pairs[i][1])

    def get(self, key: str):    # PASSES LOCAL TESTS
        """
        Receives key
        Returns value associated with the given key or None
        """
        if self._size == 0:
            return None

        mapped_index = self._hash_function(key) % self._capacity
        for j in self._buckets[mapped_index]:
            if j.key == key:
                return j.value
        return None

    def contains_key(self, key: str) -> bool:   # PASSES LOCAL TESTS
        """
        Receives a key
        Returns True if the given key is in the hash map, otherwise it returns False
        """
        if self._size == 0:
            return False

        mapped_index = self._hash_function(key) % self._capacity

        if self._buckets[mapped_index].contains(key):
            return True
        return False

    def remove(self, key: str) -> None:     # PASSES LOCAL TESTS
        """
        Receives a key
        Removes the key and associated value from the hash map
        """
        mapped_index = self._hash_function(key) % self._capacity
        for j in self._buckets[mapped_index]:
            if key == j.key:
                self._buckets[mapped_index].remove(key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:      # PASSES LOCAL TESTS
        """
        Returns a dynamic array where each index contains a tuple of a
        key/value pair stored in the hash map
        """
        new_array = DynamicArray()

        for index in range(self._capacity):
            if self._buckets[index].length() != 0:
                for j in self._buckets[index]:
                    # print(" j = ", j, " k = ", j.key, " v= ", j.value)
                    new_array.append((j.key, j.value))
        return new_array


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives a Dynamic array
    Returns a tuple containing the modes ina dynamic array,
     and its/their frequency
    """
    map = HashMap()
    for i in range(da.length()):
        if map.contains_key(da[i]):     # if key exists increment value
            value = map.get(da[i])
            map.put(da[i], value + 1)   # if key doesn't add node and value 1
        else:
            map.put(da[i], 1)

    modes = DynamicArray()
    frequency = 0
    pairs = map.get_keys_and_values()

    for i in range(pairs.length()):
        if pairs[i][1] > frequency:     # if it has a higher frequency
            frequency = pairs[i][1]
            modes = DynamicArray()
            modes.append(pairs[i][0])
        elif pairs[i][1] == frequency:  # if it has the same frequency
            modes.append(pairs[i][0])

    return modes, frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())#

    # print("\nPDF - put customized example")
    # print("-------------------")
    # values = [("key164", 35), ("key742", 456), ("key706", -919), ("key88", 976), ("key447", 830), ("key285", 492),
    #           ("key637", 91), ("key782", -391), ("key378", 35), ("key839", 546), ("key304", 481),
    #           ("key134", 598), ("key839", -260)]
    #
    # m = HashMap(23, hash_function_2)
    # for i in range(len(values)):
    #     m.put(values[i][0], values[i][1])
    # print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    # for index in range(m._capacity):
    #     print(index, " contains: ", m._buckets[index])

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # # m = HashMap(11, hash_function_2)
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")

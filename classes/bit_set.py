class BitSet:
    def __init__(self, size):
        self.size = size
        self.bits = [0] * ((size + 63) >> 6)

    def __validate_index(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range.")
        chunk = index >> 6
        position = index & 63
        mask = 1 << position
        return chunk, mask

    def is_set(self, index):
        chunk, mask = self.__validate_index(index)
        return (self.bits[chunk] & mask) == 1

    def set(self, index):
        chunk, mask = self.__validate_index(index)
        self.bits[chunk] |= mask

    def clear(self, index):
        chunk, mask = self.__validate_index(index)
        self.bits[chunk] &= ~mask

    def toggle(self, index):
        chunk, mask = self.__validate_index(index)
        self.bits[chunk] ^= mask

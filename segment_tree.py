class SegmentTree:
    def __init__(self, data):
        self.__n = len(data)
        self.__tree = [0] * (2 * self.__n)
        for i in range(self.__n):
            self.__tree[self.__n + i] = data[i]
        for i in range(self.__n - 1, 0, -1):
            self.__tree[i] = self.__tree[i << 1] + self.__tree[i << 1 | 1]

    def __len__(self):
        return self.__n

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__tree[self.__n:]})"

    def __getitem__(self, i):
        return self.__tree[i + self.__n]

    def __setitem__(self, i, value):
        i += self.__n
        self.__tree[i] = value
        while i > 1:
            i >>= 1
            self.__tree[i] = self.__tree[i << 1] + self.__tree[i << 1 | 1]

    def range_sum(self, left, right):
        left += self.__n
        right += self.__n
        res = 0
        while left < right:
            if left & 1:
                res += self.__tree[left]
                left += 1
            if right & 1:
                right -= 1
                res += self.__tree[right]
            left >>= 1
            right >>= 1
        return res

    def sum(self):
        return 0 if self.__n == 0 else self.__tree[1]

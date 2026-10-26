
class MyHashMap:
    MAX_LOAD_FACTOR = 0.75

    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _index(self, key):
        return hash(key) % self.capacity

    def load_factor(self):
        return self.size / self.capacity

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]

        for bucket in old_buckets:
            for key, value in bucket:
                index = self._index(key)
                self.buckets[index].append((key, value))

    def put(self, key, value):
        index = self._index(key)
        bucket = self.buckets[index]

        for i, (old_key, old_value) in enumerate(bucket):
            if old_key == key:
                bucket[i] = (key, value)
                return

        if (self.size + 1) / self.capacity > self.MAX_LOAD_FACTOR:
            self._resize()
            index = self._index(key)
            bucket = self.buckets[index]

        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        index = self._index(key)

        for old_key, value in self.buckets[index]:
            if old_key == key:
                return value

        return None

    def contains(self, key):
        return self.get(key) is not None

    def remove(self, key):
        index = self._index(key)
        bucket = self.buckets[index]

        for i, (old_key, value) in enumerate(bucket):
            if old_key == key:
                bucket.pop(i)
                self.size -= 1
                return True

        return False

    def stats(self):
        empty_buckets = sum(1 for bucket in self.buckets if not bucket)
        longest_bucket = max(
            (len(bucket) for bucket in self.buckets),
            default=0
        )

        return {
            "size": self.size,
            "capacity": self.capacity,
            "load_factor": self.load_factor(),
            "empty_buckets": empty_buckets,
            "longest_bucket": longest_bucket
        }

    def __len__(self):
        return self.size


def build_hash_index(values):
    index = MyHashMap()

    for row_id, key in enumerate(values):
        index.put(key, row_id)

    return index

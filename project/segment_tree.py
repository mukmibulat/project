
class SegmentTree:
    def __init__(self, a):
        self.n = len(a)
        self.a = a
        self.tree = [0] * (4 * self.n)

        if self.n > 0:
            self._build(1, 0, self.n - 1)

    def _build(self, v, tl, tr):
        if tl == tr:
            self.tree[v] = self.a[tl]
            return

        tm = (tl + tr) // 2

        self._build(2 * v, tl, tm)
        self._build(2 * v + 1, tm + 1, tr)

        self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]

    def query(self, l, r):
        return self._query(1, 0, self.n - 1, l, r)

    def _query(self, v, tl, tr, l, r):
        if tl > r or tr < l:
            return 0
        elif tl >= l and tr <= r:
            return self.tree[v]
        else:
            return (
                self._query(2 * v, tl, (tl + tr) // 2, l, r)
                + self._query(
                    2 * v + 1,
                    (tl + tr) // 2 + 1,
                    tr,
                    l,
                    r
                )
            )

    def update(self, pos, value):
        self._update(1, 0, self.n - 1, pos, value)
        self.a[pos] = value

    def _update(self, v, tl, tr, pos, value):
        if tl == tr:
            self.tree[v] = value
            return

        tm = (tl + tr) // 2

        if pos <= tm:
            self._update(2 * v, tl, tm, pos, value)
        else:
            self._update(2 * v + 1, tm + 1, tr, pos, value)

        self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]


class SegmentTreeIndex:
    def __init__(self, df):
        self.df = df
        self.values = df['Quantity'].tolist()
        self.st = SegmentTree(self.values)

    def update(self, i, x):
        self.values[i] = x
        self.st.update(i, x)

    def range_query(self, left, right):
        return self.st.query(left, right)

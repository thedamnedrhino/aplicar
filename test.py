from array_merge import *
import numpy
from copy import copy

rand = numpy.random.randint

class ArrayCase:
    def __init__(self, a1, a2, getcases, setcases):
        self.a = Array(a1, a2)
        self.getcases = getcases
        self.setcases = setcases

    def test(self):
        for i, expected in self.getcases:
            assert self.a.get(i) == expected, "get failed, i = {}, v = {}, expected = {}".format(i, self.a.get(i), expected)

        for i, v in self.setcases:
            self.a.set(i, v)
            assert self.a.get(i) == v, "set failed, i = {}, v = {}, set_value = {}".format(i, self.a.get(i), v)

class PivotCase:
    def __init__(self, a1, a2, pivot_i, start1, length1, length2, expected_a, stp1, stp2):
        self.a1 = a1
        self.a2 = a2
        self.pivot_i = pivot_i
        self.start1 = start1
        self.length1 = length1
        self.length2 = length2
        self.expected_a = expected_a
        self.expected_stp1 = stp1
        self.expected_stp2 = stp2
        self.a = Array(a1, a2, len(a1), len(a2))
        self.pivot_v = self.a.get(pivot_i)

    def assert_pivot_equals_expected(self):
        stp1, stp2 = self.a.pivot(self.pivot_i, self.start1, self.length1, self.length2)
        a = self.a
        expected_a = self.expected_a
        for i in range(len(expected_a)):
            assert a.get(i) == expected_a[i], "array != expected, index: {}, val: {}, expected: {}, stp1: {}, stp2: {}".format(i, a.get(i), expected_a[i], stp1, stp2)
    def test(self):
        self.assert_pivot_equals_expected()

class Test:
    def test(self):
        self.test_wrapped_array()
        self.test_array()
        self.test_pivot()
        self.test_merge()
        raise Exception('SUCCESS')
    def test_wrapped_array(self):
        array = Array([-1, -2, -3], [-4, -5, -6, -7])
        wrapped = WrappedArray(array, 2, 4, 0)
        getcases = [(0, -3), (3, -6), (4, -3)]
        for i, v in getcases:
            assert wrapped.get(i) == (v, i%wrapped.length), 'get failed!, index = {}, value = {}, expected = {}'.format(i, wrapped.get(i), (v, i%wrapped.length))
        getsetcases = [(0, -3, 3000), (0, 3000, 4000), (4, 4000, 5000), (0, 5000, -3), (3, -6, 6000), (7, 6000, 7000), (3, 7000, -6)]
        for index, getval, setval in getsetcases:
            val, i = wrapped.getset(index, setval)
            assert (val, i) == (getval, index%wrapped.length), 'getset failed!, index = {}, value = {}, expected = {}'.format(index, (val, i), (getval, index%wrapped.length))
        array.assert_equivalent_to([-1, -2, -3, -4, -5, -6, -7])
        """
        let's shift
        """

    def test_array(self):

        CASES = [ArrayCase([1, 2], [3, 4, 5], [(0, 1), (2, 3), (4, 5)], [(0, 2), (0, 3), (4, 4), (4, 100)])]
        for case in CASES:
            case.test()

    def test_pivot(self):
        case = PivotCase([1, 3, 4], [6, 8, 10], 1, 0, 3, 3, [1, 3, 4, 6, 8, 10], 1, 0)
        case.test()
        case = PivotCase([1, 3, 5], [2, 3, 4], 1, 0, 3, 3, [1, 2, 3, 5, 3, 4], 1, 1)
        case.test()
    def rand_array(self):
        a = rand(20, size=200)
        a.sort()
        return a

    def test_merge(self):
        cases = [(self.rand_array(), self.rand_array()) for i in range(100)]
        cases.extend( [
            ([2, 3, 4], []),
            ([], [4, 5, 6])
            ] )
        sol = Solution()
        for arr1, arr2 in cases:
            sol.merge(copy(arr1), copy(arr2), len(arr1), len(arr2))
            arr = numpy.append(arr1, arr2)
            arr.sort()
            sol.a.assert_equivalent_to(arr)




Test().test()

import math

class Array:
	def __init__(self, arr1, arr2, n=None, m=None):
		self.arr1 = arr1
		self.arr2 = arr2
		self.m = m if m != None else len(arr2)
		self.n = n if n != None else len(arr1)
		self.total_length = self.m + self.n

	def get(self, i):
		assert i < self.n + self.m
		if i < self.n:
			return self.arr1[i]
		return self.arr2[i - self.n]

	def set(self, i, val):
		assert i < self.n + self.m
		if i < self.n:
			self.arr1[i] = val
		else:
			self.arr2[i - self.n] = val
	def bin_search(self, element, start, length):
		if length == 0:
			return start
		if length == 1:
			return 1 + start if self.get(start) < element else start
		length2 = length // 2
		e = self.get(start + length2 - 1)
		if element == e:
			return start + length2 - 1
		if element < e:
			return self.bin_search(element, start, length2)
		else:
			return self.bin_search(element, start + length2, length - length2)


	def pivot(self, i, start1, length1, length2):
		"""
		We need to do:
		- How many elements of arr2 is smaller than pivot
		- Place them before pivot
			- Must shift elements of arr1 forward by that many places
		"""
		assert i >= start1
		assert i < start1 + length1
		pivot = self.get(i)
		count1 = i - start1
		count2 = 0
		end = start1 + length1 + length2
		"""
		for j in range(start1 + length1, end):
			if pivot <= self.get(j):
				break
			count2 += 1
		"""
		count2 = self.bin_search(pivot, start1 + length1, length2) - (start1 + length1)
		smaller_than_pivot = count1 + count2
		pivot_index = start1 + smaller_than_pivot
		smaller_than_pivot = count1 + count2
		pivot_index = start1 + smaller_than_pivot
		"""
		we need to shift the > pivot from arr1 with the < pivot from arr2
		These lie by in nature consecutively in our array
		So we will shift the > pivot from arr1 length(< pivot from arr2) circularly in a wrapped array containing only these two partitions
		"""
		wrapped = WrappedArray(self, start1+count1, length1 - count1, count2)
		wrapped.circular_shift(count2)
		return count1, count2
	def assert_equivalent_to(self, l):
		assert (self.total_length == len(l))
		for i in range(len(l)):
			assert (l[i] == self.get(i)), 'not equal, val: {}, expected: {}, arrays: [{}, {}]'.format(self.get(i), l[i], self.arr1, self.arr2)
	def to_array(self):
		return [self.get(i) for i in range(self.m + self.n)]



class WrappedArray:
	def __init__(self, array, start1, length1, length2):
		self.array = array
		self.start = start1
		self.length = length1 + length2

	def project_index(self, index):
		return self.start + index


	def get(self, i):
		index = i%self.length
		return self.array.get(self.project_index(index)), index

	def getset(self, i, val):
		pval, index = self.get(i)
		self.array.set(self.project_index(index), val)
		return pval, index

	def circular_shift(self, x):
		length = self.length
		gcd = math.gcd(length, x)
		for i in range(gcd):
			t = i
			e, _ = self.get(i)
			while True:
				e, t = self.getset(t + x, e)
				if t == i:
					break


class Solution:
	def merge(self, arr1, arr2, n, m):
		a = Array(arr1, arr2, n, m)
		self.a = a
		self.merge_array(0, n, m, '0')

	def merge_array(self, arr1_start, arr1_length, arr2_length, execution):
		#print("call {}: start1={}, length1={}, length2={}".format(execution, arr1_start, arr1_length, arr2_length), flush=True)
		# the base case has two parts
		# the second part is further down
		if arr1_length == 0 or arr2_length == 0:
			return
		a = self.a
		pivot_i = arr1_start + arr1_length//2
		pivot = a.get(pivot_i)
		stp1, stp2 = a.pivot(pivot_i, arr1_start, arr1_length, arr2_length)
		# second part of the base case
		# if the length of the first array is 1 we are done after pivoting
		if arr1_length == 1:
			return
		ltp1, ltp2 = arr1_length - stp1, arr2_length - stp2
		start_part_1 = arr1_start
		start_part_2 = arr1_start + stp1 + stp2
		# print("pivot_i={}, pivot={}\nstart1={}, length1.1={}, length1.2={}\nstart2={}, length2.1={}, length2.2={}".format(pivot_i, pivot, start_part_1, stp1, stp2, start_part_2, ltp1, ltp2))
		# print("{}\n\n".format(self.a.to_array()))
		self.merge_array(start_part_1, stp1, stp2, execution+'0')
		self.merge_array(start_part_2, ltp1, ltp2, execution+'1')








#{
#  Driver Code Starts
#Initial Template for Python 3

if __name__ == "__main__":
	tc=int(input())
	while tc > 0:
		n, m=map(int, (input().strip().split()))
		arr1=list(map(int , input().strip().split()))
		arr2=list(map(int , input().strip().split()))
		ob = Solution()
		ans=ob.merge(arr1, arr2, n, m)
		for x in arr1:
			print(x, end=" ")
		for x in arr2:
			print(x, end=" ")
		print()
		tc=tc-1
# } Driver Code Ends

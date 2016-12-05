'''
Question: Dictionary order
	
	When giving two integers, n and m, please sort all of the integers between [1-n]
following dictionary order, and then hand out the m-th number of the sorted sequence.
	For instance, when given n is 11 and m is 4, the sorted sequence is [1, 10, 11, 
2, 3, 4, 5, 6, 7, 8, 9], so the 4-th number is 2.

Input:
	Input is a one-line string contains two numbers, n and m.

Output:
	Output is the result number.

Sample:
	input:
	11 4
	output:
	2

AC: 100%

URL: http://exercise.acmcoder.com/online/online_judge_list?konwledgeId=158

Keyword: 
	Trie tree, or dictionary tree, always used to store giant data and efficient 
retrieve.
'''


class Solution:

	def process(self, n, m):

		depth = len(str(n))
		tail_leaf = n - (10**(depth-1)-1)
		self.tree = (depth, tail_leaf)

		no = 0
		self.result = []
		for i in range(1, 10):
			no += 1
			node = (1, i)
			if no == m:
				self.result.append(i)
				break
			leaves = self.countLeaves(node)
			if m <= no + leaves:
				self.result.append(i)
				self.searchResult(node, no)
				break
			no += leaves

		self.result = [str(item) for item in self.result]
		self.result = ''.join(self.result)

		return self.result


	def searchResult(self, node, no):

		left_bro = (node[1]-1)*10
		depth = node[0]+1
		for i in range(1, 11):
			no += 1
			node = (depth, left_bro+i)
			if no == m:
				self.result.append(i-1)
				break
			leaves = self.countLeaves(node)
			if m <= no + leaves:
				self.result.append(i-1)
				self.searchResult(node, no)
				break
			no += leaves


	def countLeaves(self, node):

		depth = node[0]
		left_bro = node[1] - 1
		tree_depth = self.tree[0]
		tree_tail_leaf = self.tree[1]
		depth_diff = tree_depth - depth
		
		min_tail_leaf = left_bro * (10**depth_diff) + 1
		max_tail_leaf = (left_bro+1) * (10**depth_diff)

		if tree_tail_leaf < min_tail_leaf:
			return (10**depth_diff-10)/9
		elif tree_tail_leaf <= max_tail_leaf:
			return (10**depth_diff-10)/9 + \
			(tree_tail_leaf-min_tail_leaf+1)
		else:
			return (10**depth_diff-10)/9 + \
			(max_tail_leaf-min_tail_leaf+1)


# Memory use exceeded.
# class Solution_1:
# 
#     def process(self, n, m):
# 
#         dictionary = [str(item) for item in range(1, n+1)]
#         dictionary.sort()
# 
#         return dictionary[m-1]

# Time exceeded.
# class Solution_2:
# 
#     def process(self, n, m):
# 
#         number = '1'
# 
#         for _ in xrange(1, m):
# 
#             number = self.getNext(number, n)
# 
#         return number
# 
#     def getNext(self, number, max):
# 
#         last = int(number[-1])
# 
#         # when end with 0-8
#         if last in range(9):
# 
#             # move into deep
#             number_tmp = number + '0'
#             if int(number_tmp) <= n:
#                 return number_tmp
# 
#             # move right
#             number_tmp = number[:-1] + str(last+1)
#             if int(number_tmp) <= n:
#                 return number_tmp
# 
#             # move back to up level
#             return self.backTrack(number)
# 
#         # when end with 9
#         else:
# 
#             # move into deep
#             number_tmp = number + '0'
#             if int(number_tmp) <= n:
#                 # return number_tmp
# 
#             # move back to up level
#             return self.backTrack(number)
# 
#     def backTrack(self, number):
# 
#         number = number[:-1]
#         last = int(number[-1])
# 
#         if last in range(9):
# 
#             # move right
#             number_tmp = number[:-1] + str(last+1)
#             return number_tmp
# 
#         else:
# 
#             return self.backTrack(number)


if __name__ == "__main__":

	solution = Solution()

	data = raw_input()
	n = int(data.split(' ')[0])
	m = int(data.split(' ')[1])

	result = solution.process(n, m)

	print result
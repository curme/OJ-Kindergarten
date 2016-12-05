class Solution:

	def process(self, m, A):

		self.trie = []
		self.depth = 0

		for number in A:
			binary = self.convertIntBinary(number)
			self.addNode(binary)

		print self.trie

		m = self.convertIntBinary(m)

		self.count = 0
		for depth in range(1, self.depth+1)[::-1]:
			base_nodes = 2**depth-2
			for index in range(1, depth**2+1):
				node_index = base_nodes+index-1
				if self.trie[node_index] == 0: continue
				else:
					count = self.trie[node_index]
					count *= self.trie[0]+self.trie[1]-sum(self.trie[base_nodes+((index+1)%2):2**(depth+1)-2:2])
					self.count += count
					self.removeNode(depth, index)
					print count
					print self.trie

		return self.count


	def convertIntBinary(self, int):

		return '{0:b}'.format(int)

	def addNode(self, new_bin):

		bin_length = len(new_bin)
		while bin_length > self.depth:
			new_nodes = 2**(self.depth+1)
			self.trie += [0] * new_nodes
			self.depth += 1

		left_bro = 0
		for depth in range(bin_length):
			digit = int(new_bin[depth])
			left_bro = 2*left_bro+digit
			leaf_index = 2**(depth+1)-2+left_bro
			self.trie[leaf_index] += 1

	def removeNode(self, depth, index):

		for depth in range(1, depth+1)[::-1]:
			base_nodes = 2**depth-2
			self.trie[base_nodes+index-1] -= 1
			index = (index+1)//2




if __name__ == "__main__":

	solution = Solution()

	data = raw_input()
	n = int(data.split(' ')[0])
	m = int(data.split(' ')[1])
	data = raw_input()
	A = [int(item) for item in data.split(' ')]

	m = 10

	A = [6, 5, 10]


	result = solution.process(m, A)

	print result
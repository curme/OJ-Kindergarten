'''
	Author: 
		
		Whip


	Brief: 
		
		This sample code is used to compare the time cost of several primes 
		search methods.


	Conclusion: 
		
		Sieve of Fratosthenes is the more efficient solution to search primes,
		compared with the methods suggested by prime definition.


	Intro:
		
		Prime number search is a common question in programming.
		In this sample code I implement three ways to find all prime numbers 
		under a giving number n:
		A1. Definition, Naive: loop [2-n]: stash number cannot be divided by 
			all number in [2-n].
		A2. Definition, Advance: loop [2-n]: stash number cannot be divided by 
			all number in [2-sqrt(n)]
		B. Sieve of Eratosthenes
			1. Create a list of consecutive integers from 2 through n: 
				(2, 3, 4, ..., n).
			2. Initially, let p equal 2, the smallest prime number.
			3. Enumerate the multiples of p by counting to n from 2p in 
				increments of p, and mark them in the list (these will be 2p, 
				3p, 4p, ... ; the p itself should not be marked).
			4. Find the first number greater than p in the list that is not 
				marked. If there was no such number, stop. Otherwise, let p now 
				equal this new number (which is the next prime), and repeat from 
				step 3.
		After implemention, I would compare the speed of them.
'''

from datetime import datetime

# A1 Definition: Naive
def definition_naive(n):
	
	prime_numbers = []

	for cand in range(2, n+1):

		is_prime = True
		
		for factor in range(2, cand):
			if cand % factor == 0:
				is_prime = False
				break
		
		if is_prime: 
			prime_numbers.append(cand)

	return prime_numbers


# A2 Definition: Advance
def definition_advance(n):

	prime_numbers = []

	for cand in range(2, n+1):

		is_prime = True
		
		for factor in range(2, int(cand**0.5 + 1)):
			if cand % factor == 0:
				is_prime = False
				break
		
		if is_prime: 
			prime_numbers.append(cand)

	return prime_numbers


# B Sieve of Eratosthenes
def sieve_of_eratosthenes(n):
	prime_numbers = []
	dustbin = set()

	for cand in range(2, n+1):

		if cand in dustbin: continue
			
		for dust in range(cand*2, n+1, cand):
			dustbin.add(dust)

		prime_numbers.append(cand)

	return prime_numbers


if __name__ == "__main__":

	n = 960960

	start = datetime.now()
	a1 = definition_naive(n)
	end = datetime.now()
	print 'Definition naive time cost:\t\t%s.' % \
		(end - start)

	start = datetime.now()
	a2 = definition_advance(n)
	end = datetime.now()
	print 'Definition advance time cost:\t\t%s.' % \
		(end - start)

	start = datetime.now()
	b = sieve_of_eratosthenes(n)
	end = datetime.now()
	print 'Sieve of Eratosthenes time cost:\t%s.' % \
		(end - start)


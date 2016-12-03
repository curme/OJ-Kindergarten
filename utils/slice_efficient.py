'''
	Author: 

		Whip


	Brief:

		This sample code is used to explore when segmenting long string data, 
		how the slice length influent the effect of Python Slice process.


	Conclusion:

		In my computer: 
			OSX 10.12.1
			2.6 GHz Intel Core i5
			8 GB 1600 MHz DDR3
		When process a 10^6 long string, the time cost would increase dramatical
		if the slice length longer than 400,000 (approximate value). And under 
		400,000 the time cost varies slightly.
		It suggests we'd better use Slice to cut no longer than 400,000 string.
		(that is segment length, but not the whole string length. Exactly, when 
		process 10^7 or 10^8 long string, the elbows are also around 400,000)

'''

import numpy
from datetime import datetime
import matplotlib.pyplot as plt

# used to slice a string into segments
# and finally return the time cost 
#	rather than the slice results
def slice_time_cost(string, interval):

	# segmenting
	start = datetime.now()
	length = len(string)
	segments = range(0, length, interval)
	for segment in segments:
		string[segment:segment+interval]
	end = datetime.now()

	# cost time
	time_cost = (end-start).total_seconds()
	return time_cost


# plot: limit the datapoint within a giving number
def plot_line_chart(intervals, time_costs, datapoints):

	# refine data points
	if len(intervals) > datapoints:
		intervals_tmp = []
		time_costs_tmp = []
		batch_size = 1+(len(intervals)/datapoints)
		batchs=range(0,len(intervals),batch_size)
		for batch in batchs:
			interval_ave = numpy.mean(\
			intervals[batch:batch+batch_size])
			time_cost_ave = numpy.mean(\
			time_costs[batch:batch+batch_size])
			intervals_tmp.append(interval_ave)
			time_costs_tmp.append(time_cost_ave)
		intervals = intervals_tmp
		time_costs = time_costs_tmp

	plt.figure('Slice Time Cost v.s. Slice Length')
	plt.plot(intervals, time_costs)
	plt.grid()
	plt.show()


if __name__ == "__main__":

	string = 'A'*(10**6)
	time_costs = []
	intervals = range(100, 1000001, 100)
	for interval in intervals:
		time_cost = slice_time_cost(string, interval)
		time_costs.append(time_cost)

	plot_line_chart(intervals, time_costs, 50)

	
import csv
import glob
import matplotlib.pyplot as plt
import math
import matplotlib
from scipy.stats.mstats import rankdata
import numpy as np

def get_results(directory, statistic_name):
	"""
	read from files in directory about results for statistic_name for every available boosting round.
	return results as a dictionary
	"""

	statistics_names = ['test_error', 'train_error']

	#for modified rankboost
		
	#statistics_names = statistics_names + earlyStop_names
	#for modified rankboost

	for index in range(len(statistics_names)):
		if statistics_names[index] == statistic_name:
			statistic_index = index

	results = {}
	csv_file_names = glob.glob(directory+'/*.csv')
	
	for csv_file_name in  csv_file_names:
		with open(csv_file_name) as csvfile:
			csvreader = csv.reader(csvfile)
			method_name = csv_file_name.split('.')[0]
			method_name = method_name.split('/')[-1]
			for row in csvreader:
				try:
					boosting_round = int(row[0])
					
					if dataset_name not in results:
						results[dataset_name]={}
					
					if method_name not in results[dataset_name]:
						results[dataset_name][method_name]  = []

					results[dataset_name][method_name].append(row[statistic_index + 1])

				except:
					dataset_name = row[0]
	#import pdb;pdb.set_trace()
	return results

def draw_plot_no_use(results, statistic_name,  outputfile_name):
	#colors=['r', 'b', 'k','c', 'y', 'm']
	colors={'rankboost':'r', 'miboosting_xu':'b','adaboost':'k', 'martiboost':'c', 'rankboost_m3':'m','martiboost_max':'y'}
	dataset_names =  results.keys()
	num_dataset = len(dataset_names)
	plt.figure(figsize=(6*num_dataset, 6*num_dataset))

	index_dataset = -1
	for dataset_name in dataset_names:
		index_dataset += 1

		plt.subplot(math.ceil( len(dataset_names )/2 + 1), 3, index_dataset)

		plt.xlabel('Boosting Iterations')
		plt.ylabel(statistic_name)
		color_index = -1
		plt.axis([0, 500, 0.49, 1.1])

		method_names = results[dataset_name].keys()
		
		for method_name in method_names:
			color_index +=1
			plt.plot(results[dataset_name][method_name], colors[method_name]+'.-')

		plt.legend(method_names)
	     	plt.title(dataset_name)
	plt.savefig(outputfile_name)


def generateAppendixLikeTable(directory, outputfile_name):
	"""
	generate the table used in appendix of latex files
	"""

	boosting_round = 150
	statistics_name = ['test_error']
			
	stat_caption_map = {'test_error': 'Test Ranking Error'}

	datasetname_map = {"cardboardbox~candlewithholder": "CB vs. CH", "wd40can~largespoon": "WC vs. LS", "smileyfacedoll~feltflowerrug": "SFD vs. FFR", "checkeredscarf~dataminingbook": "CS vs. DMB", "dirtyworkgloves~dirtyrunningshoe": "DWG vs. DRS", "bluescrunge~ajaxorange": "BS vs. AO", "apple~cokecan": "A vs. CC", "stripednotebook~greenteabox": "SN vs. GTB", "juliespot~rapbook": "JP vs. RB", "banana~goldmedal":"B vs. GM"}
	
	results = {}
	dataset_names = []
	method_names = []

	ranks = {}
	ranks_average = {}
	for statistic in statistics_name:
		results[statistic] = get_results(directory, statistic)
		dataset_names += results[statistic].keys()
		ranks[statistic] = {}
		for dataset_name in results[statistic].keys():
			method_names+=results[statistic][dataset_name].keys()
			
	dataset_names = set(dataset_names)
	method_names = set(method_names)
	
	method_names_prechosen = set(["rankboost","adaboost","martiboost","miboosting_xu", "rankboost_modiII", "rankboost_modiIII", 'rboost', 'auerboost'])
	method_names = method_names.intersection(method_names_prechosen)

	methodname_map = {"adaboost": "\\AB{}", "martiboost": "\\MB{}", "miboosting_xu":"\\MIB{}", "rboost":"\\rB{}", "auerboost":"\\AuerB{}", "rankboost_modiII": "\\RB{}+", "rankboost":"\\RB{}","rankboost_modiIII":"\\CRB{}" }

	#import pdb;pdb.set_trace()

	for statistic in statistics_name:

		line  = "\\begin{table}[ht]\\footnotesize\n"
		with open(outputfile_name, 'a+') as f:
			f.write(line)
		
		line = "\centering\n"
		with open(outputfile_name, 'a+') as f:
			f.write(line)

		line = "\caption{%s}\n" % stat_caption_map[ statistic]
		with open(outputfile_name, 'a+') as f:
			f.write(line)		

		line = "\label{Table:mil_%s}\n" % statistic
		with open(outputfile_name, 'a+') as f:
			f.write(line)	

		line = "\\begin{tabular}{|"  
		line += "c|"*(len(method_names)+1)
		line += "}\n"
		with open(outputfile_name, 'a+') as f:
			f.write(line)
		
		line = "  \hline\n"
		with open(outputfile_name, 'a+') as f:
			f.write(line)


		if statistic not in ranks:
			ranks[statistic] = {}
		if statistic not in ranks_average:
			ranks_average[statistic] = {}

		#write the all method names 
		line = "          &"
		line += ("  &  ".join([methodname_map[x] for x in method_names]))
		line += "\\\\ \n"
		with open(outputfile_name, 'a+') as f:
			f.write(line)

		line = "  \hline\n"
		with open(outputfile_name, 'a+') as f:
			f.write(line)
		dataset_count = 1
		for dataset_name in results[statistic].keys():
			 
			raw_data_per_stat_dataset = []
			for method_name in method_names:
				
				if boosting_round < len(results[statistic][dataset_name][method_name]):
					raw_data_per_stat_dataset.append(results[statistic][dataset_name][method_name][boosting_round])
				else:
					raw_data_per_stat_dataset.append(results[statistic][dataset_name][method_name][-1])

			#write the statistic values for all methods

			#write raw datasetnames or after mapping using datasetname_map 
			#line = datasetname_map[dataset_name] if dataset_name in datasetname_map else  dataset_name
			#directly use count as datasetname
			line = str(dataset_count)

			for value in raw_data_per_stat_dataset:
				line += ("  &  %.4f " % float(value) )
			line += "\\\\ \n"
				
			with open(outputfile_name, 'a+') as f:
				f.write(line)
			
			dataset_count += 1
		line = "\hline\n \end{tabular}\n  \end{table}\n"
		with open(outputfile_name, 'a+') as f:
			f.write(line)		

		line = "\n"
		with open(outputfile_name, 'a+') as f:
			f.write(line)

		line = "\n"
		with open(outputfile_name, 'a+') as f:
			f.write(line)

def generateRank(directory, outputfile_name):
	"""
	generate the rankfiles with name 'ranking/'+statistic+"_"+outputfile_name. The rank is based on the boosting round being 'boosting_round'. Its format is like
	
	RankBoost, 2.4
	RankBoost_modiII,1.9
	RankBoost_modiIII,1.3

	Input: a directory name which contains several csv files ( generated using ranking/statistics_boosting_multiple_ranking ), each csv file corresponding to 
	one method/algorithm. The file name of each csv file should be the method name, and it must be included in the variable 'method_names_prechosen'
	
	"""	


	boosting_round = 150
	#boosting_round = 40

	statistics_name = ['test_error', 'train_error']

	results = {}
	dataset_names = []
	method_names = []

	ranks = {}
	ranks_average = {}
	for statistic in statistics_name:
		results[statistic] = get_results(directory, statistic)
		dataset_names += results[statistic].keys()
		ranks[statistic] = {}
		for dataset_name in results[statistic].keys():
			method_names+=results[statistic][dataset_name].keys()
			
	dataset_names = set(dataset_names)
	method_names = set(method_names)
	
	method_names_prechosen = set(["rankboost","adaboost","martiboost","miboosting_xu", "rankboost_modiII", "rankboost_modiOp", "rankboost_modiIII"])
	method_names = method_names.intersection(method_names_prechosen)
	
	for statistic in statistics_name:
		if statistic not in ranks:
			ranks[statistic] = {}
		if statistic not in ranks_average:
			ranks_average[statistic] = {}
		for dataset_name in results[statistic].keys():
			if not 	method_names.issubset(set(results[statistic][dataset_name].keys())):
				continue		

			raw_data_per_stat_dataset = []
			for method_name in method_names:
				
				if boosting_round < len(results[statistic][dataset_name][method_name]):
					raw_data_per_stat_dataset.append(results[statistic][dataset_name][method_name][boosting_round])
				else:
					raw_data_per_stat_dataset.append(results[statistic][dataset_name][method_name][-1])

			raw_rank = rankdata(map(lambda x: float(x), raw_data_per_stat_dataset)) #smallest value of error leads to rank score of value 1 
			index = 0
			for method_name in method_names:
				if method_name not in ranks[statistic]:
					ranks[statistic][method_name] = []
				ranks[statistic][method_name].append(raw_rank[index])
				
				index += 1

		for method_name in method_names:
			if method_name not in ranks_average[statistic]:
				ranks_average[statistic][method_name] ={}
			ranks_average[statistic][method_name]["rank"] = np.average(ranks[statistic][method_name])
			ranks_average[statistic][method_name]["num_dataset"] = len(ranks[statistic][method_name])

		import pdb;pdb.set_trace()
		output_file_name_extended = 'ranking/'+statistic+"_"+outputfile_name
		
		for method_name in method_names:
			line = method_name
			line += ","
			line += str(ranks_average[statistic][method_name]["num_dataset"])
			line += ","
			line += str(ranks_average[statistic][method_name]["rank"])
			line += "\n"
			#import pdb;pdb.set_trace()

			with open(output_file_name_extended, 'a+') as f:
				f.write(line)
			
def draw_plot(directory, outputfile_name):
	"""
	plot the error vs boosting round figures. Each figure corresponds to all methods on one dataset. Each method is one input file. 
	(The input is the same with the above generateRank())
	"""

	colors={'rankboost':'b', 'rankboost_modiIII':'r','rankboost_modiII':'k' }
	#linestyles: rankboost_modiIII solid line, rankboost dotted line, rankboost_modiII dashed line
	linestyles = {'rankboost_modiIII':'-', 'rankboost':(0,[10,10]),'rankboost_modiII':(0,[40,10]) }

	statistics_name = ['test_error', 'train_error']
	
	# for modified rankboost
	#earlyStop_name = ['test_instance_AUC', 'test_bag_AUC', 'train_instance_AUC', 'train_bag_AUC', 'ranking_error', 'ranking_error_bound']	
	#statistics_name = earlyStop_name
	# for modified rankboost


	results = {}
	dataset_names = []
	for statistic in statistics_name:
		results[statistic] = get_results(directory, statistic)
		dataset_names += results[statistic].keys()
	dataset_names = set(dataset_names)

	index_dataset = -1
	#matplotlib.rc('legend', fontsize=0.5, linewidth=2)
	#plt.tick_params(labelsize=50)
	for dataset_name in dataset_names:
	#for dataset_name in ['user_181']:
	#for dataset_name in ['user_wine']:
	#for dataset_name in ['user_Horse_colic']:

		output_name = 'ranking/'+dataset_name + outputfile_name
		plt.figure(figsize=(14*len(statistics_name), 10*len(statistics_name)))
		#plt.figure(figsize=(17*2, 20*2))
		index_dataset += 1
		subplot_handle = {}
		for stat_index in range(len(statistics_name)):
			stat_name = statistics_name[stat_index]
			#plt.subplot(4, math.ceil( len(statistics_name)/3), stat_index+1)
			#plt.subplot(2, 2, stat_index+1)
			plt.subplot(2, 1, stat_index+1)
			plt.yticks(fontsize = 50)
			plt.xticks(fontsize = 50)
			plt.xlabel('Boosting Round', fontsize = 60)
			if stat_name == 'test_instance_best_balanced_accuracy':
				plt.ylabel('test_best_\nbalanced_accuracy', fontsize = 60)
			elif stat_name == 'test_instance_AUC':
				plt.ylabel('test AUC', fontsize = 60)
			elif stat_name == 'train_instance_AUC':
				plt.ylabel('train AUC', fontsize = 60)
			elif stat_name == 'train_error':
				plt.ylabel('Train Error', fontsize = 60)	
			elif stat_name == 'test_error':
				plt.ylabel('Test Error', fontsize = 60)		
			else:
				plt.ylabel(stat_name, fontsize = 60)
			color_index = -1
			if stat_name != "ranking_error" and stat_name != "ranking_error_bound" and stat_name != "train_error" and stat_name != "test_error":
				plt.axis([0, 150, 0.49, 1.1], fontsize = 50)
			else:
				#plt.axis([0, 150, 0, 0.4], fontsize = 50)
				plt.axis([0, 20, 0, 0.3], fontsize = 50)


			method_names = results[stat_name][dataset_name].keys()
		
			for method_name in method_names:
				color_index +=1
				#subplot_handle[method_name], = plt.plot(results[stat_name][dataset_name][method_name], colors[method_name]+'.-')
				#subplot_handle[method_name], = plt.plot(results[stat_name][dataset_name][method_name], colors[method_name]+linestyles[method_name])
				subplot_handle[method_name], = plt.plot(results[stat_name][dataset_name][method_name], colors[method_name], ls = linestyles[method_name], linewidth = 10)


			#plt.legend(method_names, fontsize = 35)
	     		#plt.title(dataset_name, fontsize = 30)
		#plt.suptitle(dataset_name, fontsize = 50)
		#plt.legend(method_names, fontsize = 35)
		#plt.figlegend([subplot_handle[x] for x in method_names], convertMethodNames(method_names), loc = 'upper right',  fontsize = 50)
		plt.savefig(output_name, orientation = 'landscape')

		#break

def draw_plot_test_error(directory, outputfile_name):
	"""
	only plot test error
	"""

	#colors={'rankboost':'r', 'rankboost_modiOp':'b','adaboost':'k', 'martiboost':'c', 'rankboost_modiIII':'y','rankboost_m3':'m', 'rankboost_modiII':'g' }
	colors={'rankboost':'b', 'rankboost_modiIII':'r','rankboost_modiII':'k' }
	#linestyles = {'rankboost':'--', 'rankboost_modiIII':'-','rankboost_modiII':':' },
	# 'auerboost': (0,[40,10,10,10]), 'rboost':  (0,[40,10,10,10,10,10])
	linestyles = {'rankboost_modiIII':'-', 'rankboost':(0,[10,10]),'rankboost_modiII':(0,[40,10]) }

	#statistics_name = ['test_error', 'train_error']
	statistics_name = ['test_error']

	# for modified rankboost
	#earlyStop_name = ['test_instance_AUC', 'test_bag_AUC', 'train_instance_AUC', 'train_bag_AUC', 'ranking_error', 'ranking_error_bound']	
	#statistics_name = earlyStop_name
	# for modified rankboost


	results = {}
	dataset_names = []
	for statistic in statistics_name:
		results[statistic] = get_results(directory, statistic)
		dataset_names += results[statistic].keys()
	dataset_names = set(dataset_names)

	index_dataset = -1
	#matplotlib.rc('legend', fontsize=0.5, linewidth=2)
	#plt.tick_params(labelsize=50)
	#for dataset_name in dataset_names:
	#for dataset_name in ['user_181']:
	for dataset_name in ['user_wine']:
	#for dataset_name in ['user_Horse_colic']:

		output_name = 'ranking/'+dataset_name + outputfile_name
		#plt.figure(figsize=(14*len(statistics_name), 10*len(statistics_name)))
		plt.figure(figsize=(17*2, 13*2))
		index_dataset += 1
		subplot_handle = {}
		for stat_index in range(len(statistics_name)):
			stat_name = statistics_name[stat_index]
			#plt.subplot(4, math.ceil( len(statistics_name)/3), stat_index+1)
			#plt.subplot(2, 2, stat_index+1)
			#plt.subplot(2, 1, stat_index+1)
			plt.yticks(fontsize = 60)
			plt.xticks(fontsize = 60)
			plt.xlabel('Boosting Round', fontsize = 80)
			if stat_name == 'test_instance_best_balanced_accuracy':
				plt.ylabel('test_best_\nbalanced_accuracy', fontsize = 60)
			elif stat_name == 'test_instance_AUC':
				plt.ylabel('test AUC', fontsize = 60)
			elif stat_name == 'train_instance_AUC':
				plt.ylabel('train AUC', fontsize = 60)
			elif stat_name == 'train_error':
				plt.ylabel('Train Error', fontsize = 60)	
			elif stat_name == 'test_error':
				plt.ylabel('Test Error', fontsize = 80)		
			else:
				plt.ylabel(stat_name, fontsize = 60)
			color_index = -1
			if stat_name != "ranking_error" and stat_name != "ranking_error_bound" and stat_name != "train_error" and stat_name != "test_error":
				plt.axis([0, 150, 0.49, 1.1], fontsize = 50)
			else:
				#plt.axis([0, 150, 0, 0.4], fontsize = 50)
				#plt.axis([0, 20, 0, 0.3], fontsize = 50)
				plt.axis([0, 10, 0, 0.1], fontsize = 70)


			method_names = results[stat_name][dataset_name].keys()
			method_names = ['rankboost']
			for method_name in method_names:
				color_index +=1
				#subplot_handle[method_name], = plt.plot(results[stat_name][dataset_name][method_name], colors[method_name]+'.-')
				#subplot_handle[method_name], = plt.plot(results[stat_name][dataset_name][method_name], colors[method_name]+linestyles[method_name])
				#subplot_handle[method_name], = plt.plot(results[stat_name][dataset_name][method_name], colors[method_name], ls = linestyles[method_name], linewidth = 10)
				subplot_handle[method_name], = plt.plot(results[stat_name][dataset_name][method_name], colors[method_name], ls = '-', linewidth = 10)



			#plt.legend(method_names, fontsize = 35)
	     		#plt.title(dataset_name, fontsize = 30)
		#plt.suptitle(dataset_name, fontsize = 50)
		#plt.legend(method_names, fontsize = 35)
		#plt.figlegend([subplot_handle[x] for x in method_names], convertMethodNames(method_names), loc = 'upper right',  fontsize = 50)
		plt.savefig(output_name, orientation = 'landscape')



def convertMethodNames(names):
	result = []
	for name in names:
		if name == 'rankboost_modiII':
			result.append('Rankboost+')
		elif name == 'rankboost_modiIII':
			result.append('Crankboost')
		elif name == 'rankboost':
			result.append('Rankboost')
		else:
			result.append(name)
	return result
if __name__ == '__main__':
	from optparse import OptionParser, OptionGroup
    	parser = OptionParser(usage="Usage: %resultsdir  statistic outputfile")
    	options, args = parser.parse_args()
    	options = dict(options.__dict__)
    	if len(args) != 3:
        	parser.print_help()
        	exit()		

	directory = args[0]
	outputfile_name = args[1]
	func_invoked = args[2]

	if func_invoked == 'plot':
	
		draw_plot(directory, outputfile_name)
	elif func_invoked == 'plotTest':

		draw_plot_test_error(directory, outputfile_name)
	elif func_invoked == 'rank':
		generateRank(directory, outputfile_name)
	elif func_invoked == 'table':
		generateAppendixLikeTable(directory, outputfile_name)
	else:
		raise error('Do NOT support %s functionality' % func_invoked)
	#results = get_results(directory, statistic_name)
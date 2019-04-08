from graphviz import Digraph
import csv
import pandas as pd
from criticalpath import Node

#Class representing an activity
class activity:

	def __init__(self, rows, activity_index):
		
		self.activity_name = rows[activity_index][0]
		self.predecessors_string = rows[activity_index][1]
		self.duration = int(rows[activity_index][2])
		self.start_event = (rows[activity_index][3])
		self.end_event = (rows[activity_index][4])
		self.predecessors = list()
		for i in range(len(self.predecessors_string)):
			self.predecessors.append(self.predecessors_string[i])
		self.no_of_predecessors = len(self.predecessors)
		self.ES = 0
		self.EF = 0
		self.LS = 0
		self.LF = 0
		self.TF = 0
		self.FF = 0
		self.IDF = 0
		self.ITF = 0

class Event:
	def __init__(self, index):
		self.node_num = index
		self.successors = []
		self.EST = 0
		self.LFT = 0
		self.slack_time = 0

	def get_successor_node(self, duration, successor):
		self.successors.append([duration, successor])

	

#Getting the activities
def get_activities():
	rows = []
	with open('my_csv.csv','r') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			rows.append(row)

	return rows[1:]



#Function to get all attribs in the graph
def get_graph_attribs(activities):
	nodes = set()
	edges = []
	for activity in activities:
		label = activity.activity_name + " , " + str(activity.duration)
		edges.append((activity.start_event,activity.end_event,label))
		nodes.add(int(activity.start_event))
		nodes.add(int(activity.end_event))
	return sorted(nodes), edges

#Function to plot the graph
def plot_graph(nodes, _edges):
	dot = Digraph()
	graph_edges = []
	for _edge in _edges:
		dot.edge(_edge[0], _edge[1], _edge[2])

	dot.render('Activity graph', view=True)


#Function to return the maximum previous Early Finish
def getMaxPrevEF(activities, predecessors):
	max_val = 0
	for pred in predecessors:
		for act in activities:
			if act.activity_name == pred:
				if max_val < act.EF:
					max_val = act.EF
					break
	return max_val


def display_table(activities):
	print("------------------------------------------------------------------------\n")
	df = pd.read_csv('my_csv.csv')
	df.insert(5,'ES', 0)
	df.insert(6,'EF', 0)
	df.insert(7,'LS', 0)
	df.insert(8,'LF', 0)
	df.insert(9, 'TF', 0)
	df.insert(10, 'FF', 0)
	df.insert(11, 'IDF', 0)
	df.insert(12, 'ITF', 0)
	for i in range(len(activities)):
		df.loc[df.index[i], 'Activity'] = activities[i].activity_name
		df.loc[df.index[i], 'Predecessors'] = activities[i].predecessors_string
		df.loc[df.index[i], 'Duration'] = activities[i].duration
		df.loc[df.index[i], 'ES'] = activities[i].ES
		df.loc[df.index[i], 'EF'] = activities[i].EF
		df.loc[df.index[i], 'LS'] = activities[i].LS
		df.loc[df.index[i], 'LF'] = activities[i].LF
		activities[i].TF = activities[i].LF - activities[i].EF
		df.loc[df.index[i], 'TF'] = activities[i].TF
		df.loc[df.index[i], 'FF'] = activities[i].FF
		df.loc[df.index[i], 'IDF'] = activities[i].IDF
		activities[i].ITF = activities[i].TF - activities[i].FF
		df.loc[df.index[i], 'ITF'] = activities[i].ITF
		
	print(df)
	df.to_csv('result.csv')


def get_critical_path(activities, nodes, edges):
	p = Node('Activity')
	links = []
	p.add(Node(activities[0].activity_name, duration=activities[0].duration))
	
	for i in range(1, len(activities)):
		p.add(Node(activities[i].activity_name, duration=activities[i].duration, lag=0))


	for act in activities:
		if act.no_of_predecessors != 0:
			if len(act.predecessors_string) > 1:
				for pred in act.predecessors:
					links.append((pred, act.activity_name))
			else:
				links.append((act.predecessors_string,act.activity_name))
	
	for lk in links:
		if lk[0] != ' ':
			p.link(lk[0], lk[1])
			

	p.update_all()
	print("Critical Path = ", p.get_critical_path())
	print("Critical Path Duration = ", p.duration)
	return p.get_critical_path(), p.duration


if __name__ == '__main__':
	
	data = get_activities()
	n = len(data)
	activities = []

	for i in range(n):
		activities.append(activity(data, i))

	'''	
	STEP 1:
	CALCULATION OF EST AT EACH NODE STARTING FROM FIRST NODE
	'''

	for i in range(n):
		if activities[i].no_of_predecessors == 0:
			activities[i].ES = 0
			activities[i].EF = activities[i].duration
		else:
			activities[i].ES = getMaxPrevEF(activities, activities[i].predecessors)
			activities[i].EF = activities[i].ES + activities[i].duration

	last_value = activities[n-1].EF
	nodes, edges = get_graph_attribs(activities)
	
	nodes_list = [[nodes[0], 0, 0, -1]]


	for i in range(1, len(nodes)):
	 	max = 0
	 	for act in activities:
	 		if (int(act.end_event) == int(nodes[i])):
				
	 			if(act.ES + act.duration > max):
	 				max = act.ES + act.duration
	 	nodes_list.append([nodes[i], max, 0, -1])


	no_of_nodes = len(nodes)


	_nodes = []
	for i in range(no_of_nodes):
		_nodes.append(Event(i+1))

	for node in _nodes:
		for act in activities:
			if str(act.start_event) == str(node.node_num):
				node.get_successor_node(act.duration, act.end_event)

	for i in range(len(nodes)):
	 	_nodes[i].EST = nodes_list[i][1]

	'''	
	STEP 2:
	IDENTIFICATION OF THE CRITICAL PATH
	'''

	CP, CP_duration = get_critical_path(activities, nodes, edges)
	CP = [str(cp) for cp in CP]
	

	'''
	STEP 3:
	CALCULATION OF LFT AT EACH NODE STARTING FROM THE LAST NODE
	'''
	for act in activities:
	 	if str(act.activity_name) in CP:
	 		for node in nodes_list:
	 			if str(act.start_event) == str(node[0]):
	 				node[2] = node[1]
	 				node[3] = 1
	 			if str(act.end_event) == str(node[0]):
	 				node[2] = node[1]
	 				node[3] = 1


	node_num = 1
	for act in activities:
	 	for node in nodes_list:
	 		if str(act.end_event) == str(node[0]):
	 			act.LF = node[2]
	 			act.LS = act.LF - act.duration
	 			break

	for i in range(len(activities)-1, -1, -1):
	 	for j in range(len(nodes_list)-1, 0, -1):
	 		if (nodes_list[j][3] == -1) and (str(nodes_list[j][0]) == str(activities[i].end_event)):
	 			
	 			for act in activities:
	 				if str(nodes_list[j][1]) == str(act.ES):
	 					if str(activities[i].activity_name) in act.predecessors:
	 						
	 						activities[i].LF = act.LS
	 						break

	_nodes[-1].LFT = _nodes[-1].EST

	for i in range(len(nodes)-2, -1, -1):
		min_val = 100000000
		succ_nodes = []
		duration_vals = []
		for succ in _nodes[i].successors:
			succ_nodes.append(int(succ[1]))
			duration_vals.append(int(succ[0]))
		for j in range(len(nodes)-1, -1, -1):
			for k in range(len(succ_nodes)-1, -1, -1):
				if _nodes[j].node_num == succ_nodes[k]:
					val = _nodes[j].LFT - duration_vals[k]
					if val < min_val:
						min_val = val
		_nodes[i].LFT = min_val
	
	for node in _nodes:
		node.slack_time = abs(node.EST - node.LFT)	


	for act in activities:
		for node in _nodes:
			if str(node.node_num) == str(act.start_event):
				act.ES = node.EST
			if str(node.node_num) == str(act.end_event):
				act.LF = node.LFT
		act.EF = act.ES + act.duration
		act.LS = act.LF - act.duration


	for act in activities:
		for node in _nodes:
			if str(node.node_num) == str(act.start_event):
				x = act.FF - node.slack_time
				if x < 0:
					act.IDF = 0
				else:
					act.IDF = x

			if str(node.node_num) == str(act.end_event):
				x = act.TF - node.slack_time
				if x < 0:
					act.FF = 0
				else:
					act.FF = x
	
	for act in activities:
		act.ITF = act.TF - act.FF


	nodes, edges = get_graph_attribs(activities)
	
	display_table(activities)
	plot_graph(nodes, edges)
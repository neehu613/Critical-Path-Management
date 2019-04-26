from graphviz import Digraph
import csv
import pandas as pd
from criticalpath import Node
from tkinter import *
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
		label = activity.activity_name + " [ " + str(activity.ES) + "," + str(activity.LF) + " ] "
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



def get_freefloat_time(activity, nodes_list):

	for node in nodes_list:
		if str(node[0]) == str(activity.end_event):
			head_slack = abs(node[1]-node[2])
		elif str(node[0]) == str(activity.start_event):
			tail_slack = abs(node[1]-node[2])
	return int(head_slack), int(tail_slack)


def display_table(activities, nodes_list):
	print("------------------------------------------------------------------------\n")
	df = pd.read_csv('my_csv.csv')
	df.insert(5,'ES', 0)
	df.insert(6,'EF', 0)
	df.insert(7,'LS', 0)
	df.insert(8,'LF', 0)
	df.insert(9, 'TF', 0)
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

def solution(CP,CP_duration):
	root = Tk()
	T = Text(root, height=2, width=30)
	T.pack()
	CP.append("Total Duration:")
	CP.append(CP_duration)
	T.insert(END, CP)
	mainloop()	
	



if __name__ == '__main__':
	
	data = get_activities()
	n = len(data)
	activities = []

	for i in range(n):
		activities.append(activity(data, i))

	for i in range(n):
		if activities[i].no_of_predecessors == 0:
			activities[i].ES = 0
			activities[i].EF = activities[i].duration
		else:
			activities[i].ES = getMaxPrevEF(activities, activities[i].predecessors)
			activities[i].EF = activities[i].ES + activities[i].duration

	last_value = activities[n-1].EF
	nodes, edges = get_graph_attribs(activities)


	#Calculate the ES from the first node and put them in the left box
	nodes_list = [[nodes[0], 0, 0]]
	for i in range(1, len(nodes)):
		max = 0
		for act in activities:
			if (int(act.end_event) == int(nodes[i])):
				
				if(act.ES + act.duration > max):
					max = act.ES + act.duration
		nodes_list.append([nodes[i], max, max])


	'''
	for i in range(n-1, -1, -1):
		if int(activities[i].end_event) == len(nodes):
			activities[i].LF = last_value
			
		else:
			min_value = 100000000
			for j in range(i+1, n):
				if activities[j].start_event == activities[i].end_event:
					if activities[j].ES < min_value:
						min_value = activities[j].ES
			activities[i].LF = min_value

		activities[i].LS = activities[i].LF - activities[i].duration
	'''
	CP, CP_duration = get_critical_path(activities, nodes, edges)
	CP = [str(cp) for cp in CP]
	print(CP)
	
	node_num = 1
	for act in activities:
		for node in nodes_list:
			if str(act.end_event) == str(node[0]):
				act.LF = node[2]
				act.LS = act.LF - act.duration
				break
	
	nodes, edges = get_graph_attribs(activities)
	display_table(activities, nodes_list)
	plot_graph(nodes, edges)
	solution(CP,CP_duration)

	

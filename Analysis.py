# ************************************************
#
# Student 1	: 150120059 - Cemal Fatih Kuyucu
# Student 2	: 150120014 - Meriç Turan
# Student 3	: 150110006 - Alperen Babagil
# 
# Course	: BLG 440E
# Term		: 2015-2016 Spring
# File		: Analysis.py
# 
# *********************************************** #


#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import json
from collections import OrderedDict
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime
import networkx as nx

Min_Time = "2020-01-01"
Max_Time = "1000-01-01"

Developers = defaultdict(lambda:0)
Files = defaultdict(lambda:0)

TopDevelopers = OrderedDict()
Top10Developers = OrderedDict()
Top50Developers = OrderedDict()
Top10DevelopersFrequency = OrderedDict()

TopFiles = OrderedDict()
Top10Files = OrderedDict()
Top10FilesFrequency = OrderedDict()

Top10FilesList = []
Top10DevelopersList = []
DeveloperFileRelationValues = []
Developer_File_Relation_Table = defaultdict(lambda:0)

CommitCount = 0
MenuChoose = "Z"



# Open JSON File
commit_files = json.loads(open('DATA.json').read())

# Find Min & Max Dates
for commit_file in commit_files:
	commit_detail = commit_files[commit_file]
	for commit in commit_detail:
		if commit["Time_Stamp"] < Min_Time:
			Min_Time = commit["Time_Stamp"].split(" ")[0]
		if commit["Time_Stamp"] > Max_Time:
			Max_Time = commit["Time_Stamp"].split(" ")[0]

print("Readed data dates are between " + Min_Time + " and " + Max_Time + "\n")
Start_Date = input("Please Enter Start Date (Between: " + Min_Time + " , " + Max_Time + "):")
End_Date = input("Please Enter End Date (Between: " + Min_Time + " , " + Max_Time + "):")
			

# Count User Commit Times 
for commit_file in commit_files:
	commit_detail = commit_files[commit_file]
	for commit in commit_detail:
		if commit["Time_Stamp"].split(" ")[0] >= Start_Date and commit["Time_Stamp"].split(" ")[0] <= End_Date:
			Developers[commit["Author"].split(" ")[0]] += 1
			CommitCount += 1
			Files[commit_file] += 1
			Developer_File_Relation_Table[commit["Author"].split(" ")[0], commit_file] = 1
			#print(Developer_File_Relation_Table[commit["Author"].split(" ")[0]][commit_file])
			


Day_Count = (datetime.strptime(End_Date, "%Y-%m-%d") - datetime.strptime(Start_Date, "%Y-%m-%d")).days 


while (MenuChoose != "Q" and MenuChoose != "q"):

	#if MenuChoose != "Z":
	os.system('cls')
		
	print("Readed data dates are between " + Min_Time + " and " + Max_Time + "\n")
	print("There are " + str(Day_Count) + " days between choosen dates.(" + Start_Date + " | " + End_Date + ")")
	print("There are " + str(CommitCount) + " file changes between choosen dates.(" + Start_Date + " | " + End_Date + ")\n")

	print("\nPlease choose an analysis:")
	print("A: All Developers Commits Count Graphic")
	print("B: Top Developers Commits Count Graphic(According to sum of %80 commits)")
	print("C: Top 10 Developers Commit Count Graphic")
	print("D: Top 10 Developers Commit Frequency Graphic")
	print("E: Top Files Changes Count Graphic(According to sum of %80 commits)")
	print("F: Top 10 Files Changes Count Graphic")
	print("G: Top 10 Files Changes Frequency Graphic")
	print("H: Top 10 Developers and Top 10 Files Relation Table")
	print("I: Top 10 Developers Relation Visualization ")
	print("J: Top 50 Developers Relation Visualization ")
	print("K: All Developers Relation Visualization ")
	print("Q: EXIT ")

	MenuChoose = input("\nPlease Enter Your Choose:")

	# Order Develepors According To Commit Count
	OrderedDevelopers = OrderedDict(sorted(Developers.items(), key=lambda t: t[1], reverse=True))

	# Order Files According To Commit Count
	OrderedFiles = OrderedDict(sorted(Files.items(), key=lambda t: t[1], reverse=True))

	if MenuChoose == "A" or MenuChoose == "a":

		plt.title('All Developers Commits Count', fontsize=20)
		plt.xlabel('Developer Names')
		plt.ylabel('Commit Count')
		plt.bar(range(len(OrderedDevelopers)), OrderedDevelopers.values(), align='center')
		plt.xticks(range(len(OrderedDevelopers)), OrderedDevelopers.keys())
		plt.show()

	elif MenuChoose == "B" or MenuChoose == "b":

		# Find Top Developers
		Count = 0
		for Developer in OrderedDevelopers:
			if Count >= CommitCount*0.8:
				break
			TopDevelopers.update({Developer:OrderedDevelopers[Developer]})
			Count += OrderedDevelopers[Developer]

		plt.title('Top Developers', fontsize=20)
		plt.xlabel('Developer Names')
		plt.ylabel('Commit Count')
		plt.bar(range(len(TopDevelopers)), TopDevelopers.values(), align='center')
		plt.xticks(range(len(TopDevelopers)), TopDevelopers.keys())
		plt.show()

	elif MenuChoose == "C" or MenuChoose == "c":

		# Find Top 10 Developers
		Count = 0
		for Developer in OrderedDevelopers:
			if Count > 9:
				break
			Top10Developers.update({Developer:OrderedDevelopers[Developer]})
			Count += 1
		
		plt.title('Top 10 Developers', fontsize=20)
		plt.xlabel('Developer Names')
		plt.ylabel('Commit Count')
		plt.bar(range(len(Top10Developers)), Top10Developers.values(), align='center')
		plt.xticks(range(len(Top10Developers)), Top10Developers.keys())
		plt.show()
		

	elif MenuChoose == "D" or MenuChoose == "d":

		# Find Top 10 Developer Commit Frequency Changes per Day
		Count = 0
		for Developer in OrderedDevelopers:
			if Count > 9:
				break
			Top10Developers.update({Developer:OrderedDevelopers[Developer]/Day_Count})
			Count += 1
		
		plt.title('Top 10 Developers Commit Frequency', fontsize=20)
		plt.xlabel('Developer Names')
		plt.ylabel('Change per Day')
		plt.bar(range(len(Top10Developers)), Top10Developers.values(), align='center')
		plt.xticks(range(len(Top10Developers)), Top10Developers.keys())
		plt.show()


	elif MenuChoose == "E" or MenuChoose == "e":

		# Find Top Files
		Count = 0
		for File in OrderedFiles:
			if Count >= CommitCount*0.80:
				break
			TopFiles.update({File:OrderedFiles[File]})
			Count += OrderedFiles[File]
		
		plt.title('Top Files Commits Count', fontsize=20)
		plt.xlabel('File Names')
		plt.ylabel('Commit Count')
		plt.bar(range(len(TopFiles)), TopFiles.values(), align='center')
		plt.xticks(range(len(TopFiles)), TopFiles.keys())
		plt.show()
		

	elif MenuChoose == "F" or MenuChoose == "f":

		# Find Top 10 Files
		Count = 0
		for File in OrderedFiles:
			if Count > 9:
				break
			Top10Files.update({File:OrderedFiles[File]})
			Count += 1
		
		plt.title('Top 10 Files', fontsize=20)
		plt.xlabel('File Names')
		plt.ylabel('Commit Count')
		plt.bar(range(len(Top10Files)), Top10Files.values(), align='center')
		plt.xticks(range(len(Top10Files)), Top10Files.keys())
		plt.show()
		

	elif MenuChoose == "G" or MenuChoose == "g":

		# Find Top 10 Files Frequency Changes per Day
		Count = 0
		for File in OrderedFiles:
			if Count > 9:
				break
			Top10Files.update({File:OrderedFiles[File]/Day_Count})
			Count += 1
		
		plt.title('Top 10 Files Change Frequency', fontsize=20)
		plt.xlabel('File Names')
		plt.ylabel('Change per Day')
		plt.bar(range(len(Top10Files)), Top10Files.values(), align='center')
		plt.xticks(range(len(Top10Files)), Top10Files.keys())
		plt.show()

	elif MenuChoose == "H" or MenuChoose == "h":

		# Find Top 10 Developers
		Count = 0
		for Developer in OrderedDevelopers:
			if Count > 9:
				break
			Top10Developers.update({Developer:OrderedDevelopers[Developer]})
			Count += 1
			
		# Find Top 10 Files
		Count = 0
		for File in OrderedFiles:
			if Count > 9:
				break
			Top10Files.update({File:OrderedFiles[File]})
			Count += 1


		# File-Developer Relation Matrix	
		DeveloperFileRelationValues = [[Developer_File_Relation_Table[UserName, FileName] for FileName in Top10Files] for UserName in Top10Developers] 

		for DeveloperName in Top10Developers.keys():
			Top10DevelopersList.append(DeveloperName)

		for FileName in Top10Files.keys():
			Top10FilesList.append(FileName)

			
		fig=plt.figure()
		ax = fig.add_subplot(111)  
		table_vals = [[11, 12, 13], [21, 22, 23], [31, 32, 33]]

		the_table = ax.table(cellText=DeveloperFileRelationValues,
							colWidths=[0.1] * 10,
							rowLabels=Top10DevelopersList,
							colLabels=Top10FilesList,
							loc='center right')

		ax.xaxis.set_visible(False)
		ax.yaxis.set_visible(False)
		plt.show()


	elif MenuChoose == "I" or MenuChoose == "ı" or MenuChoose == "i":
		
		# Find Top 10 Developers
		Count = 0
		for Developer in OrderedDevelopers:
			if Count > 9:
				break
			Top10Developers.update({Developer:OrderedDevelopers[Developer]})
			Count += 1
		
		
		# Visualization of Relation
		G=nx.Graph()
		
		
		# Add nodes
		for DeveloperName in Top10Developers.keys():
			G.add_node(DeveloperName)
		
		# Add edges	
		for DeveloperName in Top10Developers.keys():
			for FileName in OrderedFiles.keys():
				if Developer_File_Relation_Table[DeveloperName, FileName] == 1:
					for PeerDeveloperName in Top10Developers.keys():
						if Developer_File_Relation_Table[PeerDeveloperName, FileName] == 1 and DeveloperName != PeerDeveloperName:
							G.add_edge(DeveloperName, PeerDeveloperName)
		
		
		# draw graph
		pos = nx.shell_layout(G)
		nx.draw(G,pos,with_labels=True,node_size=1800, node_color='blue', node_alpha=0.3,node_text_size=12,)

		# show graph
		plt.show()


	elif MenuChoose == "J" or MenuChoose == "j":

		# Find Top 50 Developers
		Count = 0
		for Developer in OrderedDevelopers:
			if Count > 49:
				break
			Top50Developers.update({Developer:OrderedDevelopers[Developer]})
			Count += 1
		
		
		# Visualization of Relation
		G=nx.Graph()
		
		
		# Add nodes
		for DeveloperName in Top50Developers.keys():
			G.add_node(DeveloperName)
		
		# Add edges	
		for DeveloperName in Top50Developers.keys():
			for FileName in OrderedFiles.keys():
				if Developer_File_Relation_Table[DeveloperName, FileName] == 1:
					for PeerDeveloperName in Top50Developers.keys():
						if Developer_File_Relation_Table[PeerDeveloperName, FileName] == 1 and DeveloperName != PeerDeveloperName:
							G.add_edge(DeveloperName, PeerDeveloperName)
		
		
		# draw graph
		pos = nx.shell_layout(G)
		nx.draw(G,pos,with_labels=True,node_size=1800, node_color='blue', node_alpha=0.3,node_text_size=12,)

		# show graph
		plt.show()

	elif MenuChoose == "K" or MenuChoose == "k":
		
		# Visualization of Relation
		G=nx.Graph()
		
		
		# Add nodes
		for DeveloperName in OrderedDevelopers.keys():
			G.add_node(DeveloperName)
		
		# Add edges	
		for DeveloperName in OrderedDevelopers.keys():
			for FileName in OrderedFiles.keys():
				if Developer_File_Relation_Table[DeveloperName, FileName] == 1:
					for PeerDeveloperName in OrderedDevelopers.keys():
						if Developer_File_Relation_Table[PeerDeveloperName, FileName] == 1 and DeveloperName != PeerDeveloperName:
							G.add_edge(DeveloperName, PeerDeveloperName)
		
		
		# draw graph
		pos = nx.shell_layout(G)
		nx.draw(G,pos,with_labels=True,node_size=1800, node_color='blue', node_alpha=0.3,node_text_size=12,)

		# show graph
		plt.show()

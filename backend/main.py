import time
from datetime import datetime
import pandas as pd
import mapping
from collections import Counter
import mysql.connector

class main:
	start_time = time.time()
	mydb = mysql.connector.connect(
	    host="localhost",
	    user="root",
	    passwd="koustubh28",
	    database="db_affirmation"
	)
	mycursor = mydb.cursor()
	query='select MID,Activity_Name,User,date_format(filled_date,"%d-%m-%Y"),Filled_Xp,Status from tb_affirmation_data Order by Filled_Date ASC'
	mycursor.execute(query)
	myresult=mycursor.fetchall()
	# MID=[]
	# Activity_Name=[]
	# User=[]
	# Filled_Date=[]
	# Filled_Xp=[]
	# Status=[]
	# for x in myresult:
	# 	MID.append(x[0])
	# 	Activity_Name.append(x[1])
	# 	User.append(x[2])
	# 	Filled_Date.append(x[3])
	# 	Filled_Xp.append(x[4])
	# 	Status.append(x[5])
	# DATA = {"MID": MID, "Activity Name": Activity_Name, "User": User, "Date": Filled_Date, "Filled XP": Filled_Xp,"Status":Status}
	# data = pd.DataFrame(DATA)
	# ob=mapping.map(data)
	# ob.mapping()
	# ob.calculations()
	# print(ob.getGrades())
	# # print(data)
	board="SBAP"
	subject="MAT"
	grade="10"
	element="Assessments"
	# ob.gradeswise_progress()
	# ob.element_grades_progress()
	# ob.grade_element_action_progress()
	# ob.action_prog_2()
	query="select * from tb_data where board= %s and subject=%s and grade=%s and element=%s"
	mycursor.execute(query,[board,subject,grade,element])
	weeks={}
	myresult=mycursor.fetchall()
	for row in myresult:
		mid=row[0]
		action=row[5]
		element=row[4]
		if mid not in weeks:
			weeks[mid]={}
		if action+" In Progress" not in weeks[mid]:
			weeks[mid][action+" In Progress"]=0
		if action+" Closed" not in weeks[mid]:
			weeks[mid][action+" Closed"]=0
		if row[7]=="Closed":
			weeks[mid][action+" Closed"]+=1
		if row[7] =="In Progress":
			weeks[mid][action+" In Progress"]+=1
	print(weeks)

	print("--- %s seconds ---" % (time.time() - start_time))

import mysql.connector
import csv
from sqlalchemy import create_engine
import pymysql
import pandas as pd
from datetime import datetime

class db:
	def db_connection(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="koustubh28"
		)
		print(mydb)
		mycursor = mydb.cursor()

	def db_creation_schema(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="koustubh28"
		)
		mycursor = mydb.cursor()
		mycursor.execute("CREATE DATABASE db_affirmation")
		mydb.commit()
		mycursor.close()

	def display_data(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="koustubh28",
		  database="db_affirmation"
		)
		query='select MID,Activity_Name,User,date_format(filled_date,"%d-%m-%Y"),Filled_Xp,Status from TB_affirmation_data Order by Filled_Date ASC'
		mycursor = mydb.cursor()
		mycursor.execute(query)
		myresult=mycursor.fetchall()
		MID=[]
		Activity_Name=[]
		User=[]
		Filled_Date=[]
		Filled_Xp=[]
		for x in myresult:
			MID.append(x[0])
			Activity_Name.append(x[1])
			User.append(x[2])
			Filled_Date.append(x[3])
			Filled_Xp.append(x[4])		
		DATA = {"MID": MID, "Activity Name": Activity_Name, "User": User, "Date": Filled_Date, "Filled XP": Filled_Xp}
		df = pd.DataFrame(DATA)
		print(df)

	def db_creation_table_afiirmation(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="koustubh28",
		  database="db_affirmation"
		)
		mycursor = mydb.cursor()
		mycursor.execute("CREATE TABLE if not EXISTS TB_affirmation_data (MID VARCHAR(255), Activity_Name VARCHAR(255), User VARCHAR(255), Filled_Date DATE, Filled_Xp VARCHAR(255), Status VARCHAR(255))")
		mydb.commit()
		mycursor.close()


	def db_creation_temp(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="koustubh28",
		  database="db_affirmation"
		)
		mycursor = mydb.cursor()
		mycursor.execute("CREATE TABLE if not EXISTS TB_temp (MID VARCHAR(255), Activity_Name VARCHAR(255), User VARCHAR(255), Filled_Date DATE, Filled_Xp VARCHAR(255), Status VARCHAR(255))")
		mydb.commit()
		mycursor.close()

	def db_insert_main_data(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="koustubh28",
		  database="db_affirmation"
		)
		mycursor = mydb.cursor()
		loc="sample_data.csv"
		csv_data=pd.read_csv(loc)
		for i,j in csv_data.iterrows():
			mycursor.execute('INSERT INTO TB_affirmation_data(MID, Activity_Name, User, Filled_Date,Filled_Xp, Status)' \
			          'VALUES(%s,%s,%s,%s,%s,%s)', 
			          [j[0],j[1],j[2],datetime.strptime(j[3], "%d-%m-%Y"),j[4],j[5]])
		mydb.commit()
		mycursor.close()
		print ("Done")

	def db_insert_temp_data(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="koustubh28",
		  database="db_affirmation"
		)
		mycursor = mydb.cursor()
		loc="new_sample_data.csv"
		csv_data=pd.read_csv(loc)
		for i,j in csv_data.iterrows():
			mycursor.execute('INSERT INTO TB_temp(MID, Activity_Name, User, Filled_Date,Filled_Xp, Status)' \
			          'VALUES(%s,%s,%s,%s,%s,%s)', 
			          [j[0],j[1],j[2],datetime.strptime(j[3], "%d-%m-%Y"),j[4],j[5]])
		mydb.commit()
		mycursor.close()
		print ("Done")

	def delete_duplicate_data(self):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="root",
		  passwd="koustubh28",
		  database="db_affirmation"
		)
		mycursor = mydb.cursor()

		mycursor.execute("SELECT TB_temp.MID,TB_temp.Activity_Name,TB_temp.User,TB_temp.Filled_Date,TB_temp.Filled_Xp  FROM TB_affirmation_data INNER JOIN TB_temp on TB_affirmation_data.MID=TB_temp.MID and TB_affirmation_data.Activity_Name=TB_temp.Activity_Name and TB_affirmation_data.User=TB_temp.User and TB_affirmation_data.Filled_Date=TB_temp.Filled_Date and TB_affirmation_data.Filled_Xp=TB_temp.Filled_Xp")
		myresult = mycursor.fetchall()
		for x in myresult:
		  sql_query="DELETE FROM TB_temp WHERE MID=%s and Activity_Name=%s and User=%s and Filled_Date=%s and Filled_Xp=%s "
		  delete_data=[x[0],x[1],x[2],x[3],x[4]]
		  mycursor.execute(sql_query,delete_data)
		mydb.commit()
		print(mycursor.rowcount, "record(s) deleted")

		joining_data="INSERT INTO TB_affirmation_data SELECT * FROM TB_temp"
		mycursor.execute(joining_data)
		mycursor.execute("DELETE from TB_temp")
		mydb.commit()		

	
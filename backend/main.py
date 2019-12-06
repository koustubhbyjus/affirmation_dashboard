import time
from datetime import datetime
import pandas as pd
import mapping
from collections import Counter
import pymysql


class main:
    start_time = time.time()
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="koustubh28",
    #     database="db_affirmation"
    # )
    # mycursor = mydb.cursor()
    # query = 'select MID,Activity_Name,User,date_format(filled_date,"%d-%m-%Y"),Filled_Xp,Status from tb_affirmation_data Order by Filled_Date ASC'
    # mycursor.execute(query)
    # myresult = mycursor.fetchall()
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
    # ob.gradeswise_progress()
    # ob.element_grades_progress()
    # ob.action_grades_progress()
    # ob.grade_element_action_progress()
    # ob.action_progress()
    board=['SBAP']
    subject=['MAT']
    grade=['10']
    element=['Assessments']
    mid=['19SBAP10MAT01']
    header = []
    table_data = {}
    headers = []
    data_pushed = []
    board=tuple(board)
    subject=tuple(subject)
    grade=tuple(grade)
    element=tuple(element)
    mid=tuple(mid)
    if (board != "null" and subject != "null" and grade != "null" and element != "null" and mid != "null"):
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            passwd="koustubh28",
            database="db_affirmation"
        )
        mycursor = mydb.cursor()
        query = "select mid,action,week,status from tb_data where board in %s and subject in %s and grade in %s and element in %s"
        mycursor.execute(query, (board, subject, grade, element))
        myresult = mycursor.fetchall()
        pd_mid = []
        pd_action = []
        pd_week = []
        pd_status = []
        for row in myresult:
            pd_mid.append(row[0])
            pd_action.append(row[1])
            pd_week.append(row[2])
            pd_status.append(row[3])
        pd_data = {"MID": pd_mid, "Action": pd_action, "Week": pd_week, "Status": pd_status}
        data = pd.DataFrame(pd_data)
        headers.append("Actions")
        weeks = Counter(data["Week"])
        weeks = list(weeks.keys())
        for i in weeks:
            headers.append(i)

        for i, j in data.iterrows():
            if j[0] == mid:
                if j[1] not in table_data:
                    table_data[j[1]] = {}
                if j[2] not in table_data[j[1]]:
                    table_data[j[1]][j[2]] = j[3]

        val_2 = {}
        val = list(table_data.keys())
        data_pushed.append(val)
        for i in table_data:
            for j in table_data[i]:
                if j not in val_2:
                    val_2[j] = []
                val_2[j].append(table_data[i][j])
        for i in val_2:
            data_pushed.append(val_2[i])
    # layout = go.Layout(title='MID progress weekwise')
    print(header)
    print(data_pushed)
    print("ended particular_mid")

    print("--- %s seconds ---" % (time.time() - start_time))

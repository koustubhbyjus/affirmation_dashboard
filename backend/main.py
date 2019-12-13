import time
from datetime import datetime
import pandas as pd
import mapping
from collections import Counter
import pymysql


class main:
    start_time = time.time()
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="koustubh28",
        database="db_affirmation"
    )
    mycursor = mydb.cursor()
    query = 'select MID,Activity_Name,User,date_format(filled_date,"%d-%m-%Y"),Filled_Xp,Status from TB_affirmation_data Order by Filled_Date ASC'
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    MID=[]
    Activity_Name=[]
    User=[]
    Filled_Date=[]
    Filled_Xp=[]
    Status=[]
    for x in myresult:
    	MID.append(x[0])
    	Activity_Name.append(x[1])
    	User.append(x[2])
    	Filled_Date.append(x[3])
    	Filled_Xp.append(x[4])
    	Status.append(x[5])
    DATA = {"MID": MID, "Activity Name": Activity_Name, "User": User, "Date": Filled_Date, "Filled XP": Filled_Xp,"Status":Status}
    data = pd.DataFrame(DATA)
    ob=mapping.map(data)
    ob.mapping()
    ob.calculations()
    ob.getActions()
    ob.getBoards()

    print("--- %s seconds ---" % (time.time() - start_time))

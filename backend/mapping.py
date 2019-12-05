import numpy as np
import pandas as pd
from datetime import datetime
from collections import Counter
from statistics import stdev
from statistics import mean
from pandas import ExcelWriter
from collections import OrderedDict
import mysql.connector

class map:
    modified_data = {}
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="koustubh28",
        database="db_affirmation"
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        "CREATE TABLE if not EXISTS TB_gradewise_progress (board VARCHAR(255), subject VARCHAR(255), grade VARCHAR(255), closed VARCHAR(255), open VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE if not EXISTS TB_element_grades_progress (board VARCHAR(255), subject VARCHAR(255), grade VARCHAR(255),element VARCHAR(255), closed VARCHAR(255), open VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE if not EXISTS TB_action_grades_progress (board VARCHAR(255), subject VARCHAR(255), grade VARCHAR(255),action VARCHAR(255), closed VARCHAR(255), open VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE if not EXISTS TB_action_progress (board VARCHAR(255), subject VARCHAR(255), grade VARCHAR(255),element VARCHAR(255), action VARCHAR(255), closed VARCHAR(255), open VARCHAR(255))")
    mycursor.execute(
        "CREATE TABLE if not EXISTS TB_action_progress_chapter (board VARCHAR(255), subject VARCHAR(255), grade VARCHAR(255),element VARCHAR(255), action VARCHAR(255),chapter VARCHAR(255), status VARCHAR(255))")

    mycursor.execute("CREATE TABLE if not EXISTS TB_data(board VARCHAR(255), subject VARCHAR(255), grade VARCHAR(255), element VARCHAR(255), mid VARCHAR(255),action VARCHAR(255),week VARCHAR(255), status VARCHAR(255))")

    def __init__(self, data):
        self.data = data

    getsubject=[]
    getboard=[]
    getgrade=[]

    def mapping(self):
        activity_split = []
        activity = {}
        year = []
        state_board = []
        board = []
        grade = []
        subject = []
        chapter = []
        MID_Map = []
        weekNumber = []
        for i, j in self.data.iterrows():
            year = j[0][0:2]
            state_board = j[0][2:4]
            if j[0][2:6] not in self.getboard and j[0][2:6]!="":
            	if type(j[0][2:6])!=list:
            		self.getboard.append(j[0][2:6])

            if subject not in self.getsubject and subject!="":
            	if type(subject)!=list:
            		self.getsubject.append(subject)

            if grade not in self.getgrade and grade!="":
            	if type(grade)!=list:
            		self.getgrade.append(grade)

            board = j[0][4:6]
            grade = j[0][6:8]
            subject = j[0][8:11]
            chapter = j[0][11:13]
            week = j[3]
            week = datetime.strptime(week, "%d-%m-%Y")
            weekNumber.append(week.isocalendar()[1])
            activity = j[1].split("_")
            MID_Map.append([year, state_board, board, grade, subject, chapter, activity])
        self.data["Mid_Map"] = MID_Map
        self.data["Week"] = weekNumber
        # print(self.data)

    def calculations(self):
        calculated_data = {}
        for i, j in self.data.iterrows():
            if j[0] not in calculated_data:
                calculated_data[j[0]] = {}
            element=j[6][6][2]
            if element not in calculated_data[j[0]]:
                calculated_data[j[0]][element] = {}
            action = j[6][6][3]
            if action not in calculated_data[j[0]][element]:
                calculated_data[j[0]][element][action] = {}
                calculated_data[j[0]][element][action]["Date"] = []
                calculated_data[j[0]][element][action]["XP"] = 0
                calculated_data[j[0]][element][action]["Status"] = "Closed"
            if j[5]=="In Progress":
            	calculated_data[j[0]][element][action]["Status"] = "In Progress"
            if j[5]=="Closed":
            	calculated_data[j[0]][element][action]["Status"] = "Closed"

            if j[3] not in calculated_data[j[0]][element][action]["Date"]:
                calculated_data[j[0]][element][action]["Date"].append(j[3])
            calculated_data[j[0]][element][action]["XP"] += float(j[4])
        pd_MID = []
        pd_TRADE = []
        pd_ELEMENT = []
        pd_ACTION = []
        pd_DATE = []
        pd_STATUS = []
        pd_XP = []
        for mid in calculated_data:
            for element in calculated_data[mid]:
                for action in calculated_data[mid][element]:
                    pd_MID.append(mid)
                    pd_ELEMENT.append(element)
                    pd_ACTION.append(action)
                    pd_TRADE.append(element + " " + action)
                    pd_DATE.append(calculated_data[mid][element][action]["Date"])
                    pd_XP.append(calculated_data[mid][element][action]["XP"])
                    pd_STATUS.append(calculated_data[mid][element][action]["Status"])
        DATA = {"MID": pd_MID, "Trade": pd_TRADE, "Element": pd_ELEMENT, "Action": pd_ACTION, "XP": pd_XP,
                "Date": pd_DATE, "Status": pd_STATUS}
        self.modified_data = pd.DataFrame(DATA)

    def gradeswise_progress(self):
        self.mycursor.execute("DELETE from TB_gradewise_progress")
        mid_status = {}
        for i, j in self.modified_data.iterrows():
            if len(j[0]) == 23:
                mid = j[0][0:13]
            else:
                mid = j[0]
            if mid not in mid_status:
                mid_status[mid] = "Closed"
            if j[6] == "In Progress":
                mid_status[mid] = "In Progress"
        grades_status = {}
        for mid in mid_status:
            if len(mid) == 13:
                key = mid[2:6] + "" + mid[8:11] + "" + mid[6:8]
                if key not in grades_status:
                    grades_status[key] = {}
                    grades_status[key]["Closed"] = 0
                    grades_status[key]["In Progress"] = 0
                if mid_status[mid] == "In Progress":
                    grades_status[key]["In Progress"] += 1
                elif mid_status[mid] == "Closed":
                    grades_status[key]["Closed"] += 1
        for key in grades_status:
            self.mycursor.execute(
                "INSERT into TB_gradewise_progress(board,subject,grade,closed,open) VALUES (%s,%s,%s,%s,%s)",
                [key[0:4], key[4:7], key[7:], grades_status[key]["Closed"], grades_status[key]["In Progress"]])
        self.mydb.commit()
        # self.mycursor.close()
        print("Done")

    def element_grades_progress(self):
        self.mycursor.execute("DELETE from TB_element_grades_progress")
        element_status = {}
        element_status2 = {}
        for i, j in self.modified_data.iterrows():
            if len(j[0]) == 23:
                mid = j[0][0:13]
            else:
                mid = j[0]
            if len(mid) == 13:
                key = mid[2:6] + "" + mid[8:11] + "" + mid[6:8]
                chapter = mid[11:]
                if key not in element_status:
                    element_status[key] = {}
                    element_status2[key] = {}
                if j[2] not in element_status[key]:
                    element_status[key][j[2]] = {}
                    element_status2[key][j[2]] = {}
                    element_status2[key][j[2]]["Closed"] = 0
                    element_status2[key][j[2]]["In Progress"] = 0
                if chapter not in element_status[key][j[2]]:
                    element_status[key][j[2]][chapter] = {}
                    element_status[key][j[2]][chapter] = "Closed"
                if j[6] == "In Progress":
                    element_status[key][j[2]][chapter] = "In Progress"
        for key in element_status:
            for element in element_status[key]:
                for chapter in element_status[key][element]:
                    if element_status[key][element][chapter] == "Closed":
                        element_status2[key][element]["Closed"] += 1
                    elif element_status[key][element][chapter] == "In Progress":
                        element_status2[key][element]["In Progress"] += 1
        for key in element_status2:
            for element in element_status2[key]:
                self.mycursor.execute(
                    'INSERT INTO TB_element_grades_progress(board, subject, grade ,element, closed,open )VALUES(%s,%s,%s,%s,%s,%s)',
                    [key[0:4], key[4:7], key[7:], element, element_status2[key][element]["Closed"],
                     element_status2[key][element]["In Progress"]])
        self.mydb.commit()
        # self.mycursor.close()
        print("Done")
    def action_grades_progress(self):
        self.mycursor.execute("DELETE from TB_action_grades_progress")
        action_status = {}
        action_status2 = {}
        for i, j in self.modified_data.iterrows():
            if len(j[0]) == 23:
                mid = j[0][0:13]
            else:
                mid = j[0]
            if len(mid) == 13:
                key = mid[2:6] + "" + mid[8:11] + "" + mid[6:8]
                chapter = mid[11:]
                action=j[3]
                if key not in action_status:
                    action_status[key] = {}
                    action_status2[key] = {}
                if action not in action_status[key]:
                    action_status[key][action] = {}
                    action_status2[key][action] = {}
                    action_status2[key][action]["Closed"] = 0
                    action_status2[key][action]["In Progress"] = 0
                if chapter not in action_status[key][action]:
                    action_status[key][action][chapter] = {}
                    action_status[key][action][chapter] = "Closed"
                if j[6] == "In Progress":
                    action_status[key][action][chapter] = "In Progress"
        for key in action_status:
            for action in action_status[key]:
                for chapter in action_status[key][action]:
                    if action_status[key][action][chapter] == "Closed":
                        action_status2[key][action]["Closed"] += 1
                    elif action_status[key][action][chapter] == "In Progress":
                        action_status2[key][action]["In Progress"] += 1
        for key in action_status2:
            for action in action_status2[key]:
                self.mycursor.execute(
                    'INSERT INTO TB_action_grades_progress(board, subject, grade ,action, closed,open )VALUES(%s,%s,%s,%s,%s,%s)',
                    [key[0:4], key[4:7], key[7:], action, action_status2[key][action]["Closed"],
                     action_status2[key][action]["In Progress"]])
        self.mydb.commit()
        # self.mycursor.close()
        print("Done")

    def grade_element_action_progress(self):
        self.mycursor.execute("DELETE from TB_action_progress")
        self.mycursor.execute("DELETE from TB_action_progress_chapter")
        action_status = {}
        action_status2 = {}
        for i, j in self.modified_data.iterrows():
            if len(j[0]) == 13:
                key = j[0][2:6] + "" + j[0][8:11] + "" + j[0][6:8]
                element = j[2]
                chapter = j[0][11:]
                action = j[3]
                if key not in action_status:
                    action_status[key] = {}
                    action_status2[key] = {}

                if element not in action_status[key]:
                    action_status[key][element] = {}
                    action_status2[key][element] = {}
                if action not in action_status[key][element]:
                    action_status[key][element][action] = {}
                    action_status2[key][element][action] = {}
                    action_status2[key][element][action]["In Progress"] = 0
                    action_status2[key][element][action]["Closed"] = 0
                if chapter not in action_status[key][element][action]:
                    action_status[key][element][action][chapter] = {}
                    action_status[key][element][action][chapter] = "Closed"
                if j[6] == "In Progress":
                    action_status[key][element][action][chapter] = "In Progress"
                if j[6] == "In Progress":
                    action_status2[key][element][action]["In Progress"] += 1
                elif j[6] == "Closed":
                    action_status2[key][element][action]["Closed"] += 1
        for key in action_status2:
            for element in action_status2[key]:
                for action in action_status2[key][element]:
                    self.mycursor.execute(
                        "INSERT into TB_action_progress (board,subject,grade,element,action,closed,open) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        [key[0:4], key[4:7], key[7:], element, action, action_status2[key][element][action]["Closed"],
                         action_status2[key][element][action]["In Progress"]])
        for key in action_status:
            for element in action_status[key]:
                for action in action_status[key][element]:
                    for chapter in action_status[key][element][action]:
                        self.mycursor.execute(
                            "INSERT into TB_action_progress_chapter (board,subject,grade,element,action,chapter,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                            [key[0:4], key[4:7], key[7:], element, action, chapter,
                             action_status[key][element][action][chapter]])
        self.mydb.commit()
        # self.mycursor.close()
        print("Done")

    def action_progress(self):
        self.mycursor.execute("DELETE from tb_data")
        present_date = self.data["Date"][len(self.data["Date"]) - 1]
        present_date = datetime.strptime(present_date, "%d-%m-%Y")
        present_week = present_date.isocalendar()[1]
        min_week = 12456
        max_week = -4
        calculated_data = {}
        for i, j in self.data.iterrows():
            action=j[6][6][3]
            week=j[7]
            key=j[0][2:6]+""+j[0][8:11]+""+j[0][6:8]+""+j[6][6][2]
            if key not in calculated_data:
                calculated_data[key]={}
            if j[0] not in calculated_data[key]:
                calculated_data[key][j[0]] = {}
            if action not in calculated_data[key][j[0]]:
                calculated_data[key][j[0]][action] = {}
            if min_week > j[7]:
                min_week = j[7]
            if max_week < j[7]:
                max_week = j[7]
            if week not in calculated_data[key][j[0]][action]:
                calculated_data[key][j[0]][action][week] = "Closed"
            if j[5] =="In Progress":
                calculated_data[key][j[0]][action][week] = "In Progress"
            if j[5] =="Closed":
                calculated_data[key][j[0]][action][week] = "Closed"
        weeks = []
        for i in range(min_week, max_week +1):
            weeks.append(i)
        # print(calculated_data)
        pd_board=[]
        pd_subject=[]
        pd_grade=[]
        pd_elemet=[]
        pd_mid = []
        pd_action = []
        pd_week = []
        pd_status = []
        previous_week = 0
        status=""
        for key in calculated_data:
            for mid in calculated_data[key]:
                for action in calculated_data[key][mid]:
                    for week in weeks:
                        if week in calculated_data[key][mid][action]:
                            previous_week = week
                            status=calculated_data[key][mid][action][week]
                            if status=="Closed":
                                pd_board.append(key[0:4])
                                pd_subject.append(key[4:7])
                                pd_grade.append(key[7:9])
                                pd_elemet.append(key[9:])
                                pd_mid.append(mid)
                                pd_action.append(action)
                                pd_week.append(week)
                                pd_status.append("Closed")
                            else:
                                pd_board.append(key[0:4])
                                pd_subject.append(key[4:7])
                                pd_grade.append(key[7:9])
                                pd_elemet.append(key[9:])
                                pd_mid.append(mid)
                                pd_action.append(action)
                                pd_week.append(week)
                                pd_status.append("In Progress")
                        else:
                            if status=="Closed":
                                pd_board.append(key[0:4])
                                pd_subject.append(key[4:7])
                                pd_grade.append(key[7:9])
                                pd_elemet.append(key[9:])
                                pd_mid.append(mid)
                                pd_action.append(action)
                                pd_week.append(week)
                                pd_status.append("Closed")
                            else:
                                pd_board.append(key[0:4])
                                pd_subject.append(key[4:7])
                                pd_grade.append(key[7:9])
                                pd_elemet.append(key[9:])
                                pd_mid.append(mid)
                                pd_action.append(action)
                                pd_week.append(week)
                                pd_status.append("In Progress")
        DATA = {"Board":pd_board,"Subject":pd_subject,"Grade":pd_grade,"Element":pd_elemet,"MID": pd_mid, "Action": pd_action, "Week": pd_week, "Status": pd_status}
        pd_data = pd.DataFrame(DATA)
        for i,j in pd_data.iterrows():
            self.mycursor.execute("Insert into tb_data(board,subject,grade,element,mid,action,week,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",[j[0],j[1],j[2],j[3],j[4],j[5],j[6],j[7]])
        self.mydb.commit()
        return pd_data

    def getBoards(self):
        boards = (self.getboard)
        return sorted(boards)

    def getSubjects(self):
        subjects = self.getsubject
        return sorted(subjects)

    def getGrades(self):
        grades = (self.getgrade)
        return sorted(grades)

    def getElements(self):
        elements = Counter(self.modified_data["Element"])
        return elements.keys()

    def getActions(self):
        action = Counter(self.modified_data["Action"])
        return action.keys()

    def getMID(self):
        mid = []
        for i, j in self.modified_data.iterrows():
            if j[0] not in mid:
                mid.append(j[0])
        return sorted(mid)

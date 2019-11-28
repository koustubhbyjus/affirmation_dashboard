import numpy as np
import pandas as pd
from datetime import datetime
from collections import Counter
from statistics import stdev
from statistics import mean
from pandas import ExcelWriter
from collections import OrderedDict


class map:
    modified_data = {}

    def __init__(self, data):
        self.data = data

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
                    pd_DATE
                    pd_XP.append(calculated_data[mid][element][action]["XP"])
                    pd_STATUS.append(calculated_data[mid][element][action]["Status"])
        DATA = {"MID": pd_MID, "Trade": pd_TRADE, "Element": pd_ELEMENT, "Action": pd_ACTION, "XP": pd_XP,
                "Date": pd_DATE, "Status": pd_STATUS}
        self.modified_data = pd.DataFrame(DATA)
        # writer = ExcelWriter('Pandas-Example3.xlsx')
        # self.modified_data.to_excel(writer,'Sheet1',index=False)
        # writer.save()
        # print(self.modified_data)


    def gradeswise_progress(self, board, subject):
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
        for i in mid_status:
            if i[4:6] == board and i[2:4] == "SB" and i[8:11] == subject and i[8:11] != "XX" and i[8:11] != "" and i[6:8] != "XX" and i[6:8] != "" and len(i) == 13:
                if i[6:8] not in grades_status:
                    grades_status[i[6:8]] = {}
                    grades_status[i[6:8]]["Closed"] = 0
                    grades_status[i[6:8]]["In Progress"] = 0
                if mid_status[i] == "In Progress":
                    grades_status[i[6:8]]["In Progress"] += 1
                elif mid_status[i] == "Closed":
                    grades_status[i[6:8]]["Closed"] += 1

        grades_status = OrderedDict(sorted(grades_status.items()))
        # writer = ExcelWriter('Pandas-Example3.xlsx')
        # self.modified_data.to_excel(writer,'Sheet1',index=False)
        # writer.save()
        # print(grades_status)
        return grades_status

    def element_grades_progress(self, board, subject, grade):
        element_status = {}
        for i, j in self.modified_data.iterrows():
            if len(j[0]) == 23:
                mid = j[0][0:13]
            else:
                mid = j[0]
            if mid[4:6] == board and mid[2:4] == "SB" and mid[6:8] == grade and mid[8:11] == subject and len(mid)==13:
                if j[2] not in element_status:
                    element_status[j[2]] = {}
                if mid not in element_status[j[2]]:
                    element_status[j[2]][mid] = {}
                    element_status[j[2]][mid]["Status"] = "Closed"
                if j[6] == "In Progress":
                    element_status[j[2]][mid]["Status"] = "In Progress"
        element_status2 = {}
        for i in element_status:
            for j in element_status[i]:
                if i not in element_status2:
                    element_status2[i] = {}
                    element_status2[i]["Closed"] = 0
                    element_status2[i]["In Progress"] = 0
                if element_status[i][j]["Status"] == "Closed":
                    element_status2[i]["Closed"] += 1
                elif element_status[i][j]["Status"] == "In Progress":
                    element_status2[i]["In Progress"] += 1
        print(element_status2)
        return element_status2


    def grade_element_action_progress(self, board, subject, grade, element):
        action_status = {}
        for i, j in self.modified_data.iterrows():
            if j[0][4:6] == board and j[0][2:4] == "SB" and j[0][6:8] == grade and j[0][8:11] == subject and j[2] == element and len(j[0]) == 13:
                if j[3] not in action_status:
                    action_status[j[3]] = {}
                if j[0] not in action_status[j[3]]:
                    action_status[j[3]][j[0]] = {}
                    action_status[j[3]][j[0]]["Status"] = "Closed"
                if j[6] == "In Progress":
                    action_status[j[3]][j[0]]["Status"] = "In Progress"
        print(action_status)
        action_status2 = {}
        for i in action_status:
            for j in action_status[i]:
                if i not in action_status2:
                    action_status2[i] = {}
                    action_status2[i]["Closed"] = 0
                    action_status2[i]["In Progress"] = 0
                if action_status[i][j]["Status"] == "Closed":
                    action_status2[i]["Closed"] += 1
                if action_status[i][j]["Status"] == "In Progress":
                    action_status2[i]["In Progress"] += 1
        print(action_status2)
        return [action_status, action_status2]

    def action_progress(self, board, subject, grade, element):
        present_date = self.data["Date"][len(self.data["Date"]) - 1]
        present_date = datetime.strptime(present_date, "%d-%m-%Y")
        present_week = present_date.isocalendar()[1]
        min_week = 12456
        max_week = -4
        calculated_data = {}
        for i, j in self.data.iterrows():
            if j[0][4:6] == board and j[0][2:4] == "SB" and j[0][8:11] == subject and j[0][6:8] == grade and element == element and len(j[0]) == 13:
                if j[0] not in calculated_data:
                    calculated_data[j[0]] = {}
                if action not in calculated_data[j[0]]:
                    calculated_data[j[0]][action] = {}
                if min_week > j[6]:
                    min_week = j[6]
                if max_week < j[6]:
                    max_week = j[6]
                if j[6] not in calculated_data[j[0]][action]:
                    calculated_data[j[0]][action][j[6]] = 0
                calculated_data[j[0]][action][j[6]] += j[4]
        weeks = []
        if present_week - max_week >= 3:
            for i in range(min_week, max_week + 4):
                weeks.append(i)
        else:
            for i in range(min_week, max_week + 1):
                weeks.append(i)
        pd_MID = []
        pd_ACTION = []
        pd_WEEK = []
        pd_STATUS = []

        previous_week = 0
        for mid in calculated_data:
            for action in calculated_data[mid]:
                xp = 0
                for week in weeks:
                    if week in calculated_data[mid][action]:
                        previous_week = week
                        xp += calculated_data[mid][action][week]
                        calculated_data[mid][action][week] = xp
                        if len(mid) == 13:
                            mid_key = mid[0:11]
                        elif len(mid) == 11:
                            mid_key = mid[0:8]
                        elif len(mid) == 8:
                            mid_key = mid[0:6]
                        else:
                            mid_key = mid

                        if mid_key in self.trades[element + " " + action]:
                            if calculated_data[mid][action][week] > self.trades[element + " " + action][mid_key][
                                "Threshold"]:
                                pd_MID.append(mid)
                                pd_ACTION.append(action)
                                pd_WEEK.append(week)
                                pd_STATUS.append("Closed")
                            else:
                                pd_MID.append(mid)
                                pd_ACTION.append(action)
                                pd_WEEK.append(week)
                                pd_STATUS.append("In Progress")
                        else:
                            pd_MID.append(mid)
                            pd_ACTION.append(action)
                            pd_WEEK.append(week)
                            pd_STATUS.append("In Progress")
                    else:
                        calculated_data[mid][action][week] = 0
                        if week - previous_week >= 2:
                            pd_MID.append(mid)
                            pd_ACTION.append(action)
                            pd_WEEK.append(week)
                            pd_STATUS.append("Closed")
                        else:
                            pd_MID.append(mid)
                            pd_ACTION.append(action)
                            pd_WEEK.append(week)
                            pd_STATUS.append("In Progress")
        DATA = {"MID": pd_MID, "Action": pd_ACTION, "Week": pd_WEEK, "Status": pd_STATUS}
        pd_data = pd.DataFrame(DATA)
        return pd_data

    def getBoards(self):
        boards = ["MH", "AP"]
        return boards

    def getSubjects(self):
        subjects = ["MAT", "PHY", "CHE", "BIO"]
        return subjects

    def getGrades(self):
        grades = ["06", "07", "08", "09", "10"]
        return grades

    def getElements(self):
        elements = ["Team Activity", "RTE", "Assessments", "Practice", "Learn Journeys", "Interactive Questions",
                    "Mapping", "Product", "Knowledge Graphs", "Videos", "Questions", "Raw Questions", "Management",
                    "Scripts", "Pre-Production", "Images", "S2", "APTS", "Artworks", "QR Codes", "Chapter", "Worksheet",
                    "Quick Notes", "Chapter Structure"]
        return elements

    def getMID(self):
        mid = []
        for i, j in self.modified_data.iterrows():
            if j[0] not in mid:
                mid.append(j[0])
        return sorted(mid)

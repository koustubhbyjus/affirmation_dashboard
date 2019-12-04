loc="D:/Progress_Dashboard/data/data.csv"
data=pd.read_csv(loc)
print(datetime.strptime(data["Date"][17504], "%d-%m-%Y")-datetime.strptime(data["Date"][0], "%d-%m-%Y"))


# print(modified_data["Date"][2][len(modified_data["Date"][2])-1])

writer = ExcelWriter('Pandas-Example3.xlsx')
DATA1={"MID":list(mid_status.keys()),"Status":list(mid_status.values())}
pd1=pd.DataFrame(DATA1)
# print(pd1)
# pd1.to_excel(writer,'Sheet1',index=False)
# writer.save()

for week in calculated_data[mid][action]:
	xp+=calculated_data[mid][action][week]
	calculated_data[mid][action][week]=xp
	if len(mid)==13:
		mid_key=mid[0:11]
	elif len(mid)==11:
		mid_key=mid[0:8]
	elif len(mid)==8:
		mid_key=mid[0:6]
	else:
		mid_key=mid
	if calculated_data[mid][action][week]>=self.trades[element+" "+action][mid_key]["Threshold"]:
		status.append("Closed")
	else:
		status.append("Open")

	if
	print(mid,action,week,calculated_data[mid][action][week],status[l])
	l+=1





	data=ob.action_progress(board,subject,grade,element)
	headers=[]
	weeks=[]
	rows_table=[]
	print(board)
	print(subject)
	print(grade)
	print(element)
	if board!="null" or subject!="null" or grade!="null" or element!="null":
		weeks=Counter(data["Week"])
		weeks=weeks.keys()
		actions=Counter(data["Action"])
		actions=actions.keys()
		headers.append("Week Number")
		for i in actions:
			headers.append(i+" Open")
			headers.append(i+" Closed")
		table_data={}
		for i,j in data.iterrows():
			if j[1] not in table_data:
				table_data[j[1]]={}
			if j[2] not in table_data[j[1]]:
				table_data[j[1]][j[2]]={}
				table_data[j[1]][j[2]]["Open"]=0
				table_data[j[1]][j[2]]["Closed"]=0
			if j[3]=="Open":
				table_data[j[1]][j[2]]["Open"]+=1
			else:
				table_data[j[1]][j[2]]["Closed"]+=1
		data_to_be_pushed={}
		for action in actions:
			for week in weeks:
				if action+" Open" not in data_to_be_pushed :
					data_to_be_pushed[action+" Open"]=[]
					data_to_be_pushed[action+" Closed"]=[]
				data_to_be_pushed[action+" Open"].append(table_data[action][week]["Open"])
				data_to_be_pushed[action+" Closed"].append(table_data[action][week]["Closed"])
		rows_table.append(weeks)
		for i in data_to_be_pushed:
			rows_table.append(data_to_be_pushed[i])
		print(headers)
		print(rows_table)

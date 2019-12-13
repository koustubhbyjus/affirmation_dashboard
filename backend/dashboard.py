import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import mapping
from flask import Flask
from flask import redirect
import plotly.graph_objects as go
from collections import Counter
import pymysql

external_stylesheets = ["https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css",
                        "https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js",
                        "https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"]
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets, url_base_pathname='/dashboard/')

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
MID = []
Activity_Name = []
User = []
Filled_Date = []
Filled_Xp = []
Status = []
for x in myresult:
    MID.append(x[0])
    Activity_Name.append(x[1])
    User.append(x[2])
    Filled_Date.append(x[3])
    Filled_Xp.append(x[4])
    Status.append(x[5])
DATA = {"MID": MID, "Activity Name": Activity_Name, "User": User, "Date": Filled_Date, "Filled XP": Filled_Xp,
        "Status": Status}
data = pd.DataFrame(DATA)
ob = mapping.map(data)
ob.mapping()
ob.calculations()
boards = ob.getBoards()
subjects = ob.getSubjects()
grades = ob.getGrades()
elements = ob.getElements()
actions = ob.getActions()
mids = ob.getMID()
mydb.commit()
mycursor.close()

app.layout = html.Div(children=[
    html.Div(
        html.H1(
            children='Progress(Unit: Chapters)',
            style={'textAlign': 'center'}
        ),
        className='jumbotron'
    ),

    html.Div([

        html.Div([
            html.Label("Select Board"),
            dcc.Dropdown(
                id='boardId',
                options=[{'label': i, 'value': i} for i in boards],
                value=[],
                multi=True,
                placeholder="Select Boards"
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),

        html.Div([
            html.Label("Select Subject"),
            dcc.Dropdown(
                id='subjectId',
                options=[{'label': i, 'value': i} for i in subjects],
                value=[],
                multi=True,
                placeholder="Select Subjects"
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),

        html.Div([
            html.Label("Select Grades"),
            dcc.Dropdown(
                id='gradeId',
                options=[{'label': i, 'value': i} for i in grades],
                value=[],
                multi=True,
                placeholder="Select Grades"
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),

        html.Div([
            html.Label("Select Element"),
            dcc.Dropdown(
                id='elementId',
                options=[{'label': i, 'value': i} for i in elements],
                value=[],
                multi=True,
                placeholder="Select Elements"
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),

        html.Div([
            html.Label("Select Actions"),
            dcc.Dropdown(
                id='actionId',
                options=[{'label': i, 'value': i} for i in actions],
                value=[],
                multi=True,
                placeholder="Select Actions"
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),

        html.Div([
            html.Label("Select MID"),
            dcc.Dropdown(
                id='MIDid',
                options=[{'label': i, 'value': i} for i in mids],
                value=[],
                placeholder="Select MID"
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),

    ], style={'borderBottom': 'thin lightgrey solid',
              'backgroundColor': 'rgb(250, 250, 250)',
              'padding': '10px 5px'}),

    html.Div([
        html.Div([
            dcc.Graph(
                id='gradewise_table',
            ),
            html.I(
                "This table gives status(closed/in progress) of each grade by choosing board and subject. The objective is to find lagging grades.")
        ], style={'width': '98%', 'display': 'inline-block', 'padding': '0 20'}),

    ], className='well'),

    html.Div([
        html.Div([
            dcc.Graph(
                id='grade_elements'
            ),
            html.I(
                "This table gives the status of all the elements of the selected grade. The objective is to find the lagging element")
        ], style={'width': '49%', 'float': 'left', 'display': 'inline-block', 'padding': '0 20'}),

        html.Div([
            dcc.Graph(
                id='grades_actions'
            ),
            html.I(
                "This table shows the status of all the actions for the selected element. The objective is to find lagging actions.")
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    ], className='well'),

    html.Div([
        html.Div([
            dcc.Graph(
                id='actions_of_element'
            ),
            html.I(
                "This table shows the status of all the element for the selected action. The objective is to find lagging actions.")
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([
            dcc.Graph(
                id='elements_of_action'
            ),
            html.I(
                "This table shows the status of all the element for the selected action. The objective is to find lagging actions.")
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    ], className='well'),

    html.Div([
        html.Label("Select Actions"),
        dcc.Dropdown(
            id='action_select_id',
            options=[{'label': i, 'value': i} for i in actions],
            value=[],
            multi=True,
            placeholder="Select Actions"
        ),
    ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),
    html.Div([
        html.Div([
            dcc.Graph(
                id='weekswise_action_of_element'
            ),
            html.I(
                "This table shows weeks' progress in actions. This was done so that we can view how many chapters were closed in a particular week.")
        ], style={'width': '98%', 'display': 'inline-block', 'padding': '0 20'})
    ], className='well'),

    html.Div([
        html.Div([
            dcc.Graph(
                id='chapter_of_element'
            ),
            html.I(
                "This table shows truncated MIDs and in how many actions it's been closed/in progress. If you see chapter as " + "01" + " , it means 19SBAP10PHY" + "01" + "This view represent state of each chapter")
        ], style={'width': '98%', 'display': 'inline-block', 'padding': '0 20'}),

    ], className='well'),

    html.Div([
        html.Div([
            dcc.Graph(
                id='particular_mid'
            ),
            html.I(
                "This table shows weeks' progress of actions for a particular mid. For this, you have to select MID and it should match all the options you have selected so far. This was done so that we can view the progress of a particular MID")
        ], style={'width': '98%', 'display': 'inline-block', 'padding': '0 20'})
    ], className='well'),

], className='well')


@app.callback(
    dash.dependencies.Output('gradewise_table', 'figure'),
    [dash.dependencies.Input('boardId', 'value'), dash.dependencies.Input('subjectId', 'value'),
     ])
def outputTable(board, subject):
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="koustubh28",
        database="db_affirmation"
    )
    c1 = []
    closed = []
    in_progress = []
    mycursor = mydb.cursor()
    print("Started gradewise_table")
    grades = {}
    print(board, subject)
    if len(board) != 0 or len(subject) != 0:
        if len(board) == 0:
            board = boards
        elif len(subject) == 0:
            subject = subjects
        query = "SELECT * FROM TB_gradewise_progress where board in %s and subject in %s"
        tempStr = query % (board, subject)
        print(tempStr)
        mycursor.execute(query, (board, subject))
        myresult = mycursor.fetchall()
        for row in myresult:
            if row[2] not in grades:
                grades[row[2]] = {}
                grades[row[2]]["Closed"] = 0
                grades[row[2]]["In Progress"] = 0
            grades[row[2]]["Closed"] += int(row[3])
            grades[row[2]]["In Progress"] += int(row[4])
        for grade in grades:
            c1.append(grade)
            closed.append(grades[grade]["Closed"])
            in_progress.append(grades[grade]["In Progress"])
    layout = go.Layout(title='Gradewise Project Progress', )
    print("Ended gradewise_table")
    mydb.commit()
    mycursor.close()
    return {
        'data': [go.Table(
            columnwidth=[80, 80],
            header=dict(values=['Grade', 'Closed', 'In Progress'],
                        line_color='darkslategray',
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[c1, closed, in_progress],
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')

        )],
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('grade_elements', 'figure'),
    [dash.dependencies.Input('boardId', 'value'), dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     ])
def outputTable(board, subject, grade):
    print("Started grade_elements")
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="koustubh28",
        database="db_affirmation"
    )
    mycursor = mydb.cursor()
    element = {}
    c1 = []
    closed = []
    in_progress = []
    if (len(board) != 0 or len(subject) != 0 or len(grade) != 0):
        if len(board) == 0:
            board = boards
        if len(subject) == 0:
            subject = subjects
        if len(grade) == 0:
            grade = grades
        query = "SELECT * FROM TB_element_grades_progress where board in %s and subject in %s and grade in %s"
        mycursor.execute(query, (board, subject, grade))
        myresult = mycursor.fetchall()
        for row in myresult:
            if row[3] not in element:
                element[row[3]] = {}
                element[row[3]]["Closed"] = 0
                element[row[3]]["In Progress"] = 0
            element[row[3]]["Closed"] += int(row[4])
            element[row[3]]["In Progress"] += int(row[5])
        for i in element:
            c1.append(i)
            closed.append(element[i]["Closed"])
            in_progress.append(element[i]["In Progress"])
    layout = go.Layout(title='Elements  of grade  Progress')
    print("Ended grade_elements")
    mydb.commit()
    mycursor.close()

    return {
        'data': [go.Table(
            columnwidth=[80, 80],
            header=dict(values=['Element', 'Closed', 'In Progress'],
                        line_color='darkslategray',
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[c1, closed, in_progress],
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')

        )],
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('grades_actions', 'figure'),
    [dash.dependencies.Input('boardId', 'value'), dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     ])
def outputTable(board, subject, grade):
    print("Started grades_actions")
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="koustubh28",
        database="db_affirmation"
    )
    mycursor = mydb.cursor()
    action = {}
    c1 = []
    closed = []
    in_progress = []
    if (len(board) != 0 or len(subject) != 0 or len(grade) != 0):
        if len(board) == 0:
            board = boards
        if len(subject) == 0:
            subject = subjects
        if len(grade) == 0:
            grade = grades
        query = "SELECT * FROM TB_action_grades_progress where board in %s and subject in %s and grade in %s"
        mycursor.execute(query, (board, subject, grade))
        myresult = mycursor.fetchall()
        for row in myresult:
            if row[3] not in action:
                action[row[3]] = {}
                action[row[3]]["Closed"] = 0
                action[row[3]]["In Progress"] = 0
            action[row[3]]["Closed"] += int(row[4])
            action[row[3]]["In Progress"] += int(row[5])
        for i in action:
            c1.append(i)
            closed.append(action[i]["Closed"])
            in_progress.append(action[i]["In Progress"])
    layout = go.Layout(title='Actions  of grade Progress')
    print("Ended grade_elements")
    mydb.commit()
    mycursor.close()

    return {
        'data': [go.Table(
            columnwidth=[80, 80],
            header=dict(values=['Action', 'Closed', 'In Progress'],
                        line_color='darkslategray',
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[c1, closed, in_progress],
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')

        )],
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('actions_of_element', 'figure'),
    [dash.dependencies.Input('boardId', 'value'),
     dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     dash.dependencies.Input('elementId', 'value'),
     ])
def outputTable(board, subject, grade, element):
    print("Started actions_of_element ")
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="koustubh28",
        database="db_affirmation"
    )
    mycursor = mydb.cursor()
    action = {}
    c1 = []
    closed = []
    in_progress = []
    if (len(board) != 0 or len(subject) != 0 or len(grade) != 0 or len(element) != 0):
        if len(board) == 0:
            board = boards
        if len(subject) == 0:
            subject = subjects
        if len(grade) == 0:
            grade = grades
        if len(element) == 0:
            element = elements
        query = "SELECT * FROM TB_action_progress where board in %s and subject in %s and grade in %s and element in %s"
        mycursor.execute(query, (board, subject, grade, element))
        myresult = mycursor.fetchall()
        for row in myresult:
            if row[4] not in action:
                action[row[4]] = {}
                action[row[4]]["Closed"] = 0
                action[row[4]]["In Progress"] = 0
            action[row[4]]["Closed"] += int(row[5])
            action[row[4]]["In Progress"] += int(row[6])
        for i in action:
            c1.append(i)
            closed.append(action[i]["Closed"])
            in_progress.append(action[i]["In Progress"])

    layout = go.Layout(title='Actions  of  grade ')
    print("ended actions_of_element")
    mydb.commit()
    mycursor.close()
    return {
        'data': [go.Table(
            columnwidth=[80, 80],
            header=dict(values=['Action', 'Closed', 'In Progress'],
                        line_color='darkslategray',
                        fill_color='paleturquoise'),
            cells=dict(values=[c1, closed, in_progress],
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')
        )],
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('elements_of_action', 'figure'),
    [dash.dependencies.Input('boardId', 'value'),
     dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     dash.dependencies.Input('actionId', 'value'),
     ])
def outputTable(board, subject, grade, action):
    print("Started elements_of_action ")
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="koustubh28",
        database="db_affirmation"
    )
    mycursor = mydb.cursor()
    element = {}
    c1 = []
    closed = []
    in_progress = []
    if (len(board) != 0 or len(subject) != 0 or len(grade) != 0 or len(action) != 0):
        if len(board) == 0:
            board = boards
        if len(subject) == 0:
            subject = subjects
        if len(grade) == 0:
            grade = grades
        if len(action) == 0:
            action = actions
        query = "SELECT * FROM TB_action_progress where board in %s and subject in %s and grade in %s and action in %s"
        mycursor.execute(query, (board, subject, grade, action))
        myresult = mycursor.fetchall()
        for row in myresult:
            if row[3] not in element:
                element[row[3]] = {}
                element[row[3]]["Closed"] = 0
                element[row[3]]["In Progress"] = 0
            element[row[3]]["Closed"] += int(row[5])
            element[row[3]]["In Progress"] += int(row[6])
        for i in element:
            c1.append(i)
            closed.append(element[i]["Closed"])
            in_progress.append(element[i]["In Progress"])

    layout = go.Layout(title='Elements  of grade ')
    print("ended elements_of_action")
    mydb.commit()
    mycursor.close()
    return {
        'data': [go.Table(
            columnwidth=[80, 80],
            header=dict(values=['Element', 'Closed', 'In Progress'],
                        line_color='darkslategray',
                        fill_color='paleturquoise'),
            cells=dict(values=[c1, closed, in_progress],
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')
        )],
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('weekswise_action_of_element', 'figure'),
    [dash.dependencies.Input('boardId', 'value'),
     dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     dash.dependencies.Input('elementId', 'value'),
     dash.dependencies.Input('action_select_id', 'value'),
     ])
def outputTable(board, subject, grade, element, action_select):
    print("Started weekswise_action_of_element ")
    headers = []
    weeks = []
    rows_table = []
    if (len(board) != 0 or len(subject) != 0 or len(grade) != 0 or len(element) != 0):
        if len(board) == 0:
            board = boards
        if len(subject) == 0:
            subject = subjects
        if len(grade) == 0:
            grade = grades
        if len(element) == 0:
            element = elements
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            passwd="koustubh28",
            database="db_affirmation"
        )
        mycursor = mydb.cursor()
        if len(action_select) != 0:
            query = "select mid,action,week,status from TB_data where board in %s and subject in %s and grade in %s and element in %s and action in %s"
            mycursor.execute(query, (board, subject, grade, element, action_select))
        else:
            query = "select mid,action,week,status from TB_data where board in %s and subject in %s and grade in %s and element in %s"
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
        weeks = Counter(data["Week"])
        weeks = weeks.keys()
        actions = Counter(data["Action"])
        actions = actions.keys()
        headers.append("Week Number")
        for i in actions:
            headers.append(i + " In Progress")
            headers.append(i + " Closed")
        table_data = {}
        for i, j in data.iterrows():
            if j[1] not in table_data:
                table_data[j[1]] = {}
            if j[2] not in table_data[j[1]]:
                table_data[j[1]][j[2]] = {}
                table_data[j[1]][j[2]]["In Progress"] = 0
                table_data[j[1]][j[2]]["Closed"] = 0
            if j[3] == "In Progress":
                table_data[j[1]][j[2]]["In Progress"] += 1
            else:
                table_data[j[1]][j[2]]["Closed"] += 1
        data_to_be_pushed = {}
        for action in actions:
            for week in weeks:
                if action + " In Progress" not in data_to_be_pushed:
                    data_to_be_pushed[action + " In Progress"] = []
                    data_to_be_pushed[action + " Closed"] = []
                data_to_be_pushed[action + " In Progress"].append(table_data[action][week]["In Progress"])
                data_to_be_pushed[action + " Closed"].append(table_data[action][week]["Closed"])
        rows_table.append(list(weeks))
        for i in data_to_be_pushed:
            rows_table.append(data_to_be_pushed[i])
    layout = go.Layout(title='Week wise progress of Actions of element of grade of subject of Board')
    print("Ended weekswise_action_of_element")
    return {
        'data': [go.Table(
            header=dict(values=headers,
                        line_color='darkslategray',
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=rows_table,
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')
        )],
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('chapter_of_element', 'figure'),
    [dash.dependencies.Input('boardId', 'value'),
     dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     dash.dependencies.Input('elementId', 'value'),
     dash.dependencies.Input('action_select_id', 'value'),
     ])
def outputTable(board, subject, grade, element, action_select):
    print("started 5 ")
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="koustubh28",
        database="db_affirmation"
    )
    mycursor = mydb.cursor()
    headers = []
    table_values = []
    # board = tuple(board)
    # subject = tuple(subject)
    # grade = tuple(grade)
    # element = tuple(element)
    if (len(board) != 0 or len(subject) != 0 or len(grade) != 0 or len(element) != 0):
        if len(board) == 0:
            board = boards
        if len(subject) == 0:
            subject = subjects
        if len(grade) == 0:
            grade = grades
        if len(element) == 0:
            element = elements
        if len(action_select) != 0:
            query = "SELECT * FROM TB_action_progress_chapter where board in %s and subject in %s and grade in %s and element in %s and action in %s"
            mycursor.execute(query, (board, subject, grade, element, action_select))
        else:
            query = "SELECT * FROM TB_action_progress_chapter where board in %s and subject in %s and grade in %s and element in %s"
            mycursor.execute(query, (board, subject, grade, element))
        myresult = mycursor.fetchall()
        headers.append("Chapter Name")
        chapters_headers = []
        action_headers = []
        status = []
        for row in myresult:
            if row[4] not in action_headers:
                action_headers.append(row[4])
            if row[5] not in chapters_headers:
                chapters_headers.append(row[5])

        action_status = {}
        action_headers = sorted(action_headers)
        for i in action_headers:
            headers.append(i)
        chapters_headers = sorted(chapters_headers)
        for i in action_headers:
            for j in chapters_headers:
                query = 'SELECT * FROM TB_action_progress_chapter where board in %s and subject in %s and grade in %s and element in %s and action in (%s) and chapter in (%s) '
                mycursor.execute(query, (board, subject, grade, element, i, j))
                myresult = mycursor.fetchall()
                if i not in action_status:
                    action_status[i] = []
                if len(myresult) == 0:
                    action_status[i].append('null')
                for row in myresult:
                    action_status[i].append(row[6])

        table_values.append(chapters_headers)
        for i in action_status:
            table_values.append(action_status[i])
    layout = go.Layout(title='Chapters of element vs Actions ')
    print("Ended 5")
    mydb.commit()
    mycursor.close()
    return {
        'data': [go.Table(
            columnwidth=[80, 80],
            header=dict(values=headers,
                        line_color='darkslategray',
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=table_values,
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')

        )],
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('particular_mid', 'figure'),
    [dash.dependencies.Input('boardId', 'value'),
     dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     dash.dependencies.Input('elementId', 'value'),
     dash.dependencies.Input('MIDid', 'value'),
     dash.dependencies.Input('action_select_id', 'value'),
     ])
def outputTable(board, subject, grade, element, mid, action_select):
    print("started particular_mid")
    header = []
    table_data = {}
    headers = []
    data_pushed = []
    board = tuple(board)
    subject = tuple(subject)
    grade = tuple(grade)
    element = tuple(element)
    # mid=tuple(mid)
    if (len(board) != 0 or len(subject) != 0 or len(grade) != 0 or len(element) != 0 or len(mid) != 0):
        if len(board) == 0:
            board = boards
        if len(subject) == 0:
            subject = subjects
        if len(grade) == 0:
            grade = grades
        if len(element) == 0:
            element = elements
        if len(mid) == 0:
            mid = mids
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            passwd="koustubh28",
            database="db_affirmation"
        )
        mycursor = mydb.cursor()
        if len(action_select) != 0:
            query = "select mid,action,week,status from TB_data where board in %s and subject in %s and grade in %s and element in %s and action in %s"
            mycursor.execute(query, (board, subject, grade, element, action_select))
        else:
            query = "select mid,action,week,status from TB_data where board in %s and subject in %s and grade in %s and element in %s"
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
    layout = go.Layout(title='MID progress weekwise')
    print(header)
    print(data_pushed)
    print("ended particular_mid")

    return {
        'data': [go.Table(
            columnwidth=[80, 80],
            header=dict(values=headers,
                        line_color='darkslategray',
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=data_pushed,
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')
        )],
        'layout': layout
    }


@server.route('/')
def render_dashboard():
    return redirect('/dashboard/')


if __name__ == '__main__':
    app.run_server(port=3000)
# host='0.0.0.0'

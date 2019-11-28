import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import mapping
from flask import Flask
from flask import redirect
import plotly.graph_objects as go
from collections import Counter

external_stylesheets = ["https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css",
                        "https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js",
                        "https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"]
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets, url_base_pathname='/dashboard/')

loc = "data/data.csv"
data = pd.read_csv(loc)
ob = mapping.map(data)
ob.mapping()
ob.calculations()
ob.closed_threshold_date()
ob.closed_threshold_xp_mean()

boards = ob.getBoards()
subjects = ob.getSubjects()
grades = ob.getGrades()
elements = ob.getElements()
mids = ob.getMID()

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
                value='null'
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),

        html.Div([
            html.Label("Select Subject"),
            dcc.Dropdown(
                id='subjectId',
                options=[{'label': i, 'value': i} for i in subjects],
                value='null'
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),

        html.Div([
            html.Label("Select Grades"),
            dcc.Dropdown(
                id='gradeId',
                options=[{'label': i, 'value': i} for i in grades],
                value='null'
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),

        html.Div([
            html.Label("Select Element"),
            dcc.Dropdown(
                id='elementId',
                options=[{'label': i, 'value': i} for i in elements],
                value='null'
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),
        html.Div([
            html.Label("Select MID"),
            dcc.Dropdown(
                id='MIDid',
                options=[{'label': i, 'value': i} for i in mids],
                value='null'
            ),
        ], style={'width': '19%', 'float': 'center', 'display': 'inline-block', 'padding-left': '70px'}),

    ], style={'borderBottom': 'thin lightgrey solid',
              'backgroundColor': 'rgb(250, 250, 250)',
              'padding': '10px 5px'}),

    html.Div([
        html.Div([
            dcc.Graph(
                id='1',

            ),
            html.I("This table gives status(closed/in progress) of each grade by choosing board and subject. The objective is to find lagging grades.")          
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

        html.Div([
            dcc.Graph(
                id='2'
            ),
            html.I("This table gives the status of all the elements of the selected grade. The objective is to find the lagging element")
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block', 'padding': '0 20'})
    ], className='well'),

   

    html.Div([
        html.Div([
            dcc.Graph(
                id='3'
            ),
            html.I("This table shows the status of all the actions for the selected element. The objective is to find lagging actions.")
        ], style={'width': '98%', 'display': 'inline-block', 'padding': '0 20'}),
    ], className='well'),

    html.Div([
        html.Div([
            dcc.Graph(
                id='4'
            ),
            html.I("This table shows weeks' progress in actions. This was done so that we can view how many chapters were closed in a particular week.")
        ], style={'width': '98%','display': 'inline-block', 'padding': '0 20'})
    ], className='well'),


    html.Div([
        html.Div([
            dcc.Graph(
                id='5'
            ),
            html.I("This table shows truncated MIDs and in how many actions it's been closed/in progress. If you see chapter as "+"01"+" , it means 19SBAP10PHY"+"01"+"This view represent state of each chapter")
        ], style={'width': '98%', 'display': 'inline-block', 'padding': '0 20'}),

    ], className='well'),

    html.Div([
        html.Div([
            dcc.Graph(
                id='6'
            ),
            html.I("This table shows weeks' progress of actions for a particular mid. For this, you have to select MID and it should match all the options you have selected so far. This was done so that we can view the progress of a particular MID")
        ], style={'width': '98%','display': 'inline-block', 'padding': '0 20'})
    ], className='well'),

], className='well')


@app.callback(
    dash.dependencies.Output('1', 'figure'),
    [dash.dependencies.Input('boardId', 'value'), dash.dependencies.Input('subjectId', 'value'),
     ])
def outputTable(board, subject):
    print("Started 1")
    prog = ob.gradeswise_progress(board, subject)
    grades = []
    closed = []
    in_progress = []
    if (board != "null" or subject != "null"):
        for i in prog:
            grades.append(i)
            closed.append(prog[i]['Closed'])
            in_progress.append(prog[i]['Open'])
    layout = go.Layout(title='Gradewise  ' + board + ' ' + subject + ' Project Progress',)
    print("Ended 1")
    return {
        'data': [go.Table(
            columnwidth = [80,80],
            header=dict(values=['Grade', 'Closed', 'In Progress'],
                        line_color='darkslategray',
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[grades, closed, in_progress],
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')

        )],
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('2', 'figure'),
    [dash.dependencies.Input('boardId', 'value'), dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     ])
def outputTable(board, subject, grade):
    print("Started 2")
    prog = ob.element_grades_progress(board, subject, grade)
    element = []
    closed = []
    in_progress = []
    if (board != "null" or subject != "null" or grade != "null"):
        for i in prog:
            element.append(i)
            closed.append(prog[i]['Closed'])
            in_progress.append(prog[i]['Open'])
    layout = go.Layout(title='Elements  of grade ' + grade + ' Progress')
    print("Ended 2")

    return {
        'data': [go.Table(
            columnwidth = [80,80],
            header=dict(values=['Element', 'Closed', 'In Progress'],
                        line_color='darkslategray',
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[element, closed, in_progress],
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')

        )],
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('3', 'figure'),
    [dash.dependencies.Input('boardId', 'value'),
     dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     dash.dependencies.Input('elementId', 'value'),
     ])
def outputTable(board, subject, grade, element):
    print("Started 3 ")
    prog = ob.grade_element_action_progress(board, subject, grade, element)[1]
    action = []
    closed = []
    in_progress = []
    if (board != "null" or subject != "null" or grade != "null"):
        for i in prog:
            action.append(i)
            closed.append(prog[i]['Closed'])
            in_progress.append(prog[i]['Open'])

    layout = go.Layout(title='Actions  of ' + element + ' of grade ' + grade + ' Progress')
    print("ended 3")
    return {
        'data': [go.Table(
            columnwidth = [80,80],
            header=dict(values=['Element', 'Closed', 'In Progress'],
                        line_color='darkslategray',
                        fill_color='paleturquoise'),
            cells=dict(values=[action, closed, in_progress],
                       line_color='darkslategray',
                       fill_color='white',
                       align='left')
        )],
        'layout': layout
    }


@app.callback(
    dash.dependencies.Output('5', 'figure'),
    [dash.dependencies.Input('boardId', 'value'),
     dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     dash.dependencies.Input('elementId', 'value'),
     ])
def outputTable(board, subject, grade, element):
    print("started 5 ")
    prog = ob.grade_element_action_progress(board, subject, grade, element)[0]
    headers = []
    headers.append("Chapter Name")
    mids = []
    chapters = []
    status = {}
    if (board != "null" or subject != "null" or grade != "null"):
        for i in prog:
            headers.append(i)
            for j in prog[i]:
                if j not in mids:
                    if len(j) == 13:
                        chapters.append(j[len(j) - 2:len(j)])
                    elif len(j) == 11:
                        chapters.append(j[len(j) - 3:len(j)])
                    elif len(j) == 23:
                        chapters.append(j[len(j) - 12:len(j)])
                    else:
                        chapters.append(j)

                    mids.append(j)
        mids = sorted(mids)
        chapters = sorted(chapters)
        for i in prog:
            if i not in status:
                status[i] = []
            for j in mids:
                try:
                    status[i].append(prog[i][j]["Status"])
                except KeyError:
                    status[i].append("null")
    table_values = []

    table_values.append(chapters)
    for i in status:
        table_values.append(status[i])

    layout = go.Layout(title='Chapters of ' + element + ' vs Actions ')
    print("Ended 5")
    return {
        'data': [go.Table(
            columnwidth = [80,80],
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
    dash.dependencies.Output('4', 'figure'),
    [dash.dependencies.Input('boardId', 'value'),
     dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     dash.dependencies.Input('elementId', 'value'),
     ])
def outputTable(board, subject, grade, element):
    print("Started 4 ")
    data = ob.action_progress(board, subject, grade, element)
    headers = []
    weeks = []
    rows_table = []
    if (board != "null" or subject != "null" or grade != "null" or element != "null"):
        weeks = Counter(data["Week"])
        weeks = weeks.keys()
        actions = Counter(data["Action"])
        actions = actions.keys()
        headers.append("Week Number")
        for i in actions:
            headers.append(i + " Open")
            headers.append(i + " Closed")
        table_data = {}
        for i, j in data.iterrows():
            if j[1] not in table_data:
                table_data[j[1]] = {}
            if j[2] not in table_data[j[1]]:
                table_data[j[1]][j[2]] = {}
                table_data[j[1]][j[2]]["Open"] = 0
                table_data[j[1]][j[2]]["Closed"] = 0
            if j[3] == "Open":
                table_data[j[1]][j[2]]["Open"] += 1
            else:
                table_data[j[1]][j[2]]["Closed"] += 1
        data_to_be_pushed = {}
        for action in actions:
            for week in weeks:
                if action + " Open" not in data_to_be_pushed:
                    data_to_be_pushed[action + " Open"] = []
                    data_to_be_pushed[action + " Closed"] = []
                data_to_be_pushed[action + " Open"].append(table_data[action][week]["Open"])
                data_to_be_pushed[action + " Closed"].append(table_data[action][week]["Closed"])
        rows_table.append(list(weeks))
        for i in data_to_be_pushed:
            rows_table.append(data_to_be_pushed[i])
        layout = go.Layout(
            title='Week wise progress of Actions of element ' + element + 'of grade ' + grade + ' of subject ' + subject + ' of Board ' + board)
        print("Ended 4")
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
    dash.dependencies.Output('6', 'figure'),
    [dash.dependencies.Input('boardId', 'value'),
     dash.dependencies.Input('subjectId', 'value'),
     dash.dependencies.Input('gradeId', 'value'),
     dash.dependencies.Input('elementId', 'value'),
     dash.dependencies.Input('MIDid', 'value'),
     ])
def outputTable(board, subject, grade, element, mid):
    print("started 6")
    data = ob.action_progress(board, subject, grade, element)
    header = []
    table_data = {}
    headers = []
    data_pushed = []
    if (board != "null" or subject != "null" or grade != "null" or element != "null" or mid != "null"):
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
    layout = go.Layout(title='MID ' + mid + ' progress weekwise')
    print(header)
    print(data_pushed)
    print("ended 6")

    return {
        'data': [go.Table(
            columnwidth = [80,80],
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

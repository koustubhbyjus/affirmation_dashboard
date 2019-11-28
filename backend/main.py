import time
from datetime import datetime
import pandas as pd
import mapping
from collections import Counter

class main:
	boards=["MH","AP"]
	subjects=["PHY","MAT","BIO","CHE"]
	grades=["06","07","08","09","10"]
	elements=["Team Activity","RTE","Assessments","Practice","Learn Journeys","Interactive Questions","Mapping","Product","Knowledge Graphs","Videos","Questions","Raw Questions","Management","Scripts","Pre-Production","Images","S2","APTS","Artworks","QR Codes","Chapter","Worksheet","Quick Notes","Chapter Structure"]

	board="AP"
	subject="MAT"
	grade="10"
	element="Assessments"
	mid="19SBAP10PHY03"
	start_time = time.time()

	loc="data/sample_data.csv"
	data=pd.read_csv(loc)
	# print(data)
	ob=mapping.map(data)
	ob.mapping()
	ob.calculations()
	# ob.closed_threshold_date()
	# ob.closed_threshold_xp_mean()
	# ob.gradeswise_progress(board,subject)
	# ob.element_grades_progress(board,subject,"10")
	ob.grade_element_action_progress(board,subject,"10",element)
	# ob.action_progress(board,subject,"10",element)
	print("--- %s seconds ---" % (time.time() - start_time))

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import sys

connection = sqlite3.connect("DataBase/FaceBase.db")

cursor = connection.cursor()

query = "SELECT * FROM People"
df = pd.read_sql(query, connection)

df = df.sort_values(by=['Attendance'])

print(df)

courses = df['Name']
values = df['Attendance']

y = df['Attendance']
mylabels = df['Name']

figure, axis = plt.subplots(2, 2)

axis[0, 0].bar(courses, values, color ='green',
		width = 0.2)
axis[0, 0].set_xlabel("Names of employes")
axis[0, 0].set_ylabel("No. of days present")
axis[0, 0].set_title("Attendance graph")

axis[0, 1].pie(y,labels = mylabels)
axis[0, 1].set_title("Attendance by Percentage")
axis[0, 1].legend(title = "Names")

xaxis = ([] for i in range(len(mylabels)))
yaxis = ([] for i in range(len(mylabels)))

axis[1, 0].plot([5,4,3,2,1,0], [5,4,3,2,1,0],color='white')
for i in range(len(mylabels)):
	axis[1, 0].text(0, i, str(i+1), style='italic')
	axis[1, 0].text(1, i, mylabels[i], style='italic')
	axis[1, 0].text(2, i, y[i], style='italic')

axis[1, 1].plot(courses, values)
axis[1, 1].set_title("Line Graph Of Attendance")

plt.show()

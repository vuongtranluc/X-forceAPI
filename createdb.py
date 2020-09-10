import sqlite3, csv
###
### Create Final Score
###
# connection = sqlite3.connect("database1.db")
# cursor = connection.cursor()

# with open('FinalScore.csv', 'r') as file:
#     no_records = 0

#     for row in file:
#         cursor.execute("INSERT INTO finalScore VALUES (?,?,?,?,?,?,?,?,?)", row.split(','))
#         connection.commit()
#         no_records += 1

# connection.close()


###
### Create Final Mapping
###
connection = sqlite3.connect("/Users/vuongtranluc/Documents/self_study/python_selfstudy/API2/FinalMapping.db")
cursor = connection.cursor()

with open('/Users/vuongtranluc/Documents/self_study/python_selfstudy/API2/X-forceAPI/FinalMapping.csv', 'r') as file:
    no_records = 0

    for row in file:
        cursor.execute("INSERT INTO FinalMapping VALUES (?,?,?,?)", row.split(','))
        connection.commit()
        no_records += 1

connection.close()



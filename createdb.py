import sqlite3, csv

connection = sqlite3.connect("database1.db")
cursor = connection.cursor()

with open('FinalScore.csv', 'r') as file:
    no_records = 0

    for row in file:
        cursor.execute("INSERT INTO finalScore VALUES (?,?,?,?,?,?,?,?,?)", row.split(','))
        connection.commit()
        no_records += 1

connection.close()


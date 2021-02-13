from sys import argv, exit
import cs50

if len(argv) != 2:
    print("Usage: python roster.py house_name")
    exit(1)

db = cs50.SQL("sqlite:///students.db")

entered_house = argv[1]

rows = db.execute("SELECT * FROM students WHERE house = ? ORDER BY last, first", entered_house)

for row in rows:
    first = row["first"]
    middle = row["middle"]
    last = row["last"]
    birth = row["birth"]

    if row["middle"] != None:
        print(f"{first} {middle} {last}, born {birth}")
    if row["middle"] == None:
        print(f"{first} {last}, born {birth}")
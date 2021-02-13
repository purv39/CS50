# TODO
from sys import argv, exit
import csv
import cs50


def main():
    if len(argv) != 2:
        print("Usage: pyhton import.py filename.csv")
        exit(1)

    db = cs50.SQL("sqlite:///students.db")

    csv_path = argv[1]
    with open(csv_path) as file:

        reader = csv.DictReader(file)

        for row in reader:
            names = partition_name(row["name"])

            db.execute("INSERT INTO students(first, middle, last, house,birth) VALUES(?, ? ,? ,?, ?)",
                       names[0], names[1], names[2], row["house"], row["birth"])


def partition_name(full_name):
    names = full_name.split()
    return names if len(names) >= 3 else [names[0], None, names[1]]


main()
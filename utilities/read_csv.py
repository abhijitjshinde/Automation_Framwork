import csv

def getCSVData(filename):
    rows = []
    dataFile = open(filename, "r")
    reader = csv.reader(dataFile)
    next(reader)
    for row in reader:
        rows.append(row)
    return rows

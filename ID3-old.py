import csv
import math




# Compute last column's entropy
def entropyclass():
    countone = 0
    countzero = 0
    for row in csvTestReader:
        curr = row[classcolumn]   # 用变量取代
        if curr == "0":
            countzero = countzero + 1
        elif curr == "1":
            countone = countone + 1
    temp = countone / (countzero + countone)
    entro = -temp * math.log2(temp) - (1 - temp) * math.log2(1 - temp)
    return entro


def entropyattr(columnno):
    countone = 0
    countzero = 0
    YY = 0
    YZ = 0  # attribute=1,class=0
    ZY = 0
    ZZ = 0
    for row in csvTestReader:
        curr = row[columnno]
        if curr == "0":
            countzero = countzero + 1
            if row[classcolumn] == '0':
                ZZ = ZZ + 1
            elif row[classcolumn] == '1':
                ZY = ZY + 1
        elif curr == "1":
            countone = countone + 1
            if row[classcolumn] == '0':
                YZ = YZ + 1
            elif row[classcolumn] == '1':
                YY = YY + 1
    HY = -YY / countone * math.log2(YY / countone) - YZ / countone * math.log2(YZ / countone)
    HZ = -ZY / countzero * math.log2(ZY / countzero) - ZZ / countzero * math.log2(ZZ / countzero)
    H = countone / (countone + countzero) * HY + countzero / (countone + countzero) * HZ
    return H


csvTestReader = csv.reader(open('training_set.csv', 'r'))
classcolumn = len(next(csvTestReader))-1   # Get the column number of class



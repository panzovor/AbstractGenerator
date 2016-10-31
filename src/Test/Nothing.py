__author__ = 'E440'
import codecs

def readData(filename):
    result = {}
    file  = codecs.open(filename,"r","utf-8")
    firstline = True
    for line in file.readlines():
        if firstline:
            firstline = False
            continue
        tmp = line.split("\t")
        if tmp[1] not in result.keys():
            result[tmp[1].lower()] = tmp[1:]
    return result


def compare(filename,filename1):
    data1 = readData(filename)
    data2 = readData(filename1)
    result = []
    for key in data1.keys():
        if key not in data2.keys():
            if data1[key][2] == "1":
                tmp = data1[key][0]
                # tmp.append(data1[key][5])
                result.append(tmp.lower())
    string =""
    for tmp in result:
        for stri in tmp:
            string += stri+"\t"
        string+="\n"
    return result
    # print(string)
    # print(result.__len__())

filename1 = "D:\workspace\AbstractGenerator\\resource\ObservationResult\\xf.txt"
filename = "D:\workspace\AbstractGenerator\\resource\ObservationResult\kh.txt"
result = compare(filename,filename1)
data1 = readData(filename)
print(data1.__len__())
for id in result:
    data1.pop(id)

for key in data1.keys():
    print(data1[key][0]+"\t"+data1[key][1]+"\t"+data1[key][5])


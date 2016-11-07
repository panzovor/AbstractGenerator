__author__ = 'E440'
import jieba
import codecs
import os
import Dir


def checkFile(filepath):
    exits = os.path.exists(filepath)
    if exits:
        return
    else:
        filepathDir = os.path.dirname(filepath)
        if os.path.exists(filepathDir):
            return
        else:
            os.makedirs(filepathDir)
            return

def read(filepath,encoding ="utf-8"):
    result = codecs.open(filepath,"r",encoding).read()
    result = result.replace("\r\n","")
    return  result

def nothing(s):
    return False

def get_filelist(dir, fileList,filter=nothing):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            #如果需要忽略某些文件夹，使用以下代码
            if filter(s):
                continue
            newDir=os.path.join(dir,s)
            get_filelist(newDir, fileList)
    return fileList

def read_dir(file_dir,encoding = "utf-8"):
    if not os.path.exists(file_dir):
        return
    file_list = []
    get_filelist(file_dir,file_list)
    result ={}
    for file in file_list:
        result[file]  = (read(file))
    return result

# def readLines(filepath,encoding ="utf-8"):
#     tmp = codecs.open(filepath,"r",encoding).read()
#     return tmp.split("\r\n")

def readLines(filepath,encoding ="utf-8"):
    result =[]
    file = codecs.open(filepath,"r",encoding)
    for line in file.readlines():
        if "\r\n" in line:
            line = line.replace("\r\n","")
        if line.strip().__len__()>1:

            result.append(line.strip())
    return result

    ## write a string
def write(filepath,content,encoding ="utf-8",append = False):
    checkFile(filepath)
    file = None
    if not append:
        file = codecs.open(filepath,"w",encoding)
    else:
        file = codecs.open(filepath,"a",encoding)
    file.write(content)
    file.flush()
    file.close()

def get_filename(file):
    index = file.rindex("\\")
    return str(file[index+1:])

def demo():
    path = Dir.resourceDir+"摘要文书\离婚纠纷"
    file_list = read_dir(path)
    print(path)
    print(file_list)
    print(get_filename(file_list[0]))


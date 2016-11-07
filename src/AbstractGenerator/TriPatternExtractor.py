__author__ = 'E440'
import re
import Dir
import src.FileTools.Tools as tools
import jieba.posseg as pseg
import jieba


def contain_laws_name(sentence,lawsName):
    for name in lawsName:
        if name in sentence:
            return True
    return False

def seperate_sentences(text):
    regex = "！|。|？"
    return re.split(regex,text)

def seperate_words(sentence,porperty = True):
    if porperty:
        words  = pseg.cut(sentence)
        result = []
        for w in words:
            tmp =[]
            tmp.append(w.word)
            tmp.append(w.flag)
            result.append(tmp)
        return result
    else:
        return list(jieba.cut(sentence))

def extract_laws(text):
    path = Dir.resourceDir+"dict\\LawsName"
    laws_name = tools.readLines(path)
    lines = seperate_sentences(text)
    middle_result =[]
    for line in lines:
        if "《" in line:
            middle_result.append(line)
    result = []
    for line in middle_result:
        index = int(line.find("《"))
        line = line[index:]
        end = int(line.find("规定"))
        words = str(line[:end])
        if words.__len__()>0:
        # if True:
            if re.match("的|之",words[-1]) !=None:
                words=  str(words[:-1])
            index_end = int(words.find("》"))
            if "第" not in words[index_end:index_end+10]:
                words = str(words[:index_end+1])
            if contain_laws_name(words,laws_name):
                result.append(words)
            elif "中华人民共和国" in words:
                    result.append(words)
    return result

def extract_result(text):
    result =set()
    path1 = Dir.resourceDir+"dict\\guilty_name.txt"
    guilty_names = tools.readLines(path1)
    sentences = seperate_sentences(text)
    for sentence in sentences:
        for guilty_name in guilty_names:
            if guilty_name in sentence:
                index = sentence.find(guilty_name)
                if "构成" in sentence[index-10:index] and ("，" in sentence[index:index+guilty_name.__len__()+2] or index+guilty_name.__len__()+2>sentence.__len__()):
                    result.add(guilty_name)
    return list(result)

def extract_result_simple_rule(text):
    result = []
    sentences = seperate_sentences(text)
    for sentence in sentences:
        if "被害人" in sentence and "被告人" in sentence and  "处罚" in sentence:
            result.append(sentence)
        elif ("从轻" in sentence or "从重" in sentence) and "处罚" in sentence:
            result.append(sentence)
    # print(result)
    return result

def extract_fact_from_guilty(text):
    result = []
    sentences = seperate_sentences(text)
    for sentence in sentences:
        path1 = Dir.resourceDir+"dict\\guilty_name.txt"
        guilty_names = tools.readLines(path1)
        for guilty_name in guilty_names:
            if guilty_name in sentence:
                index = sentence.find(guilty_name)
                if "，" in sentence[:index]:
                    index = sentence[:index].rfind("，")
                start = sentence[:index].find("被告人")
                if index > start+10:
                    result.append(guilty_name+":"+ str(sentence[start:index]))
    return result

def extract_fact(text):
    result = []
    sentences = seperate_sentences(text)
    for sentence in sentences:
        index  = sentence.find("已构成")
        if index >0:
            former_index = sentence[:index].rfind("，")
            if index- former_index<5:
                index = former_index
            start  = sentence.find("本院认为")
            if start >=0:
                start = 4
                if sentence[start] =="，" or sentence[start] =="：" :
                    start  = 5
            else:
                start  =0
            tmp  = str(sentence[start:index])
            result.append(tmp)
    return result

def extract_from_text(text,func):
    result =[]
    for fun in func:
        tmp = str(fun(text))
        if tmp.__len__()>3:
            result.append(tmp)
        else:
            result.append(None)
    if result.__len__() == func.__len__() or True:
        return result
    else :
        return None

def extract_from_texts(text_dict,func):
    result={}
    for file in text_dict.keys():
        text = text_dict[file]
        tmp  = extract_from_text(text,func)

        if tmp != None:
            result[tools.get_filename(file)] = tmp
    return result

def demo(func):

    # path = Dir.resourceDir+"\\摘要文书\\故意伤害罪"
    paths = [
    Dir.resourceDir+"\\摘要文书\\故意伤害罪"
             # ,Dir.resourceDir+"\\摘要文书\\离婚纠纷",
             # Dir.resourceDir+"\\摘要文书\\盗窃罪"
             # Dir.resourceDir+"\\摘要文书\\民间借贷纠纷"
    ]
    final_result = []
    for path in paths:
        text_list = tools.read_dir(path)
        result = extract_from_texts(text_list,func)

        string =""
        for res in result.keys():
            string+= res+"\t"
            for tmp in result[res]:
                string+= str(tmp)+"\t"
            string+="\n"
        print(string)
        # count=0
        # for res in result:
        #     if res.__len__()>0:
        #         count+=1
        #
        # # print(str(path[path.rfind("\\")+1:]),count,result.__len__())
        # if result.__len__()>0:
        #     print(result)

demo([extract_laws,extract_fact_from_guilty,extract_result,extract_result_simple_rule])

# string  ="本院认为，检察机关申请撤诉符合法律规定，应予准许，依照最高人民法院关于适用《中华人民共和国刑事诉讼法》的解释第二百四十二条之规定，裁定如下："
# result = extract_from_text(string,[extract_laws])
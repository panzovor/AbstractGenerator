# -*- coding: utf-8 -*-
__author__ = 'E440'
import re
import Dir
import jieba
import src.FileTools.Tools as tools

debug = False

def seperate_sentences(text):
    regex = "！|。|？|；"
    return re.split(regex,text)

def loadWords():
    file = Dir.resourceDir+"dict\civil_marriage"
    words = tools.readLines(file)
    return words

def sepearate(text):
    regex = "。|？|！|；"
    temp = re.split(regex,text)
    result =[]
    for tem in temp:
        if tem.strip() =="":
            continue
        else:
            result.append(tem)
    return result

def sepearate_details(text):
    regex = "。|？|！|；|，"
    temp = re.split(regex,text)
    result =[]
    for tem in temp:
        if tem.strip() =="":
            continue
        else:
            result.append(tem)
    return result

def extract_result(text):
    sentences = sepearate(text)
    regex = "，"
    file_path = Dir.resourceDir+"dict/civil_mariiage_result"
    judge_words = tools.readLines(file_path)
    result = {}
    for sentence in sentences:
        flag = False
        details_sentences = re.split(regex,sentence)
        for details_sentence in details_sentences:
            words = list(jieba.cut(details_sentence))
            count =0
            for word in judge_words:
                if word in words:
                    count+=1
            if count/ words.__len__()>0.3:
                words_sent = list(jieba.cut(sentence))
                inter = set(words_sent).intersection(set(words))
                sentence_simple = ""
                if "由此" in sentence:
                    sentence_simple = sentence[sentence.find("由此")+2:]
                elif "，故" in sentence:
                    sentence_simple = sentence[sentence.find("，故")+2:]
                else:
                    sentence_simple = sentence
                if sentence_simple not in result.keys():
                    result[sentence_simple] = inter.__len__() / words_sent.__len__()
                    flag = True
                    break;
            else:
                if re.findall("\d*?元",sentence):
                    result[sentence] = "元"
            if flag:
                break
    return list(result.keys())

def extract_fact(text):
    pos_words = loadWords()
    result ={}
    sentences = sepearate(text)
    if debug:
        print("============================================")
        print(text)
        print("############################################")
    for sentence in sentences:
        words  = list(jieba.cut(sentence))
        hit =0
        for word in words:
            if word in pos_words:
                hit+=1
        score = hit/words.__len__()
        if sentence not in result.keys():
            result[sentence] = score
    n = 1
    if debug:
        for sentence in result.keys():
            print(sentence+":"+str(result[sentence]))
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    sent = getBeyondAverageSentence(result,n)
    result_order = order(sent,sentences)
    if debug:
        print("***********************************************")
        for sentence in result_order:
            print(sentence)
    return result_order

def extract_laws(text):
    result =[]
    sentences = sepearate(text)
    for sentence in sentences:
        if "《" in sentence:
            index = sentence.find("《")
            sentence= sentence[index:]
            laws = sentence[:sentence.find("》")]
            if laws.__len__()>7:
                if "的规定" in sentence:
                    result.append(sentence[:sentence.rfind("的规定")])
                elif "之规定" in sentence:
                    result.append(sentence[:sentence.rfind("之规定")])
                else:
                    result.append(sentence)
    return result


def getHighestSentence(sentence_score,n):
    result,max ={},0
    if sentence_score.__len__() < n:
        n = sentence_score.__len__()
    for i in range(n):
        sentence_hightest =""
        for sentence in sentence_score.keys():
            if sentence not in result.keys():
                if sentence_score[sentence] > max:
                    max = sentence_score[sentence]
                    sentence_hightest = sentence
        result[sentence_hightest] = max
    return result

def getBeyondAverageSentence(sentence_score,n=1):
    average_score,result  = 0,[]
    for sentence in sentence_score.keys():
        average_score += sentence_score[sentence]
    average_score = average_score/sentence_score.__len__()
    for sentence in sentence_score.keys():
        if sentence_score[sentence] > average_score:
            string = sentence
            result.append(string)
    if debug:
        print(average_score)
        for sentence in result:
            print(sentence+":"+str(sentence_score[sentence]))
    return result

def order(result_sentences,text_sentences):
    result = []
    for text_sentence in text_sentences:
        if text_sentence in result_sentences:
            result.append(text_sentence)
    if result.__len__() != result_sentences.__len__():
        result = None
    return result


def demo():
    paths = [
             Dir.resourceDir+"\\摘要文书\\离婚纠纷"
             # ,
             # Dir.resourceDir+"\\摘要文书\\民间借贷纠纷"
    ]
    filepath = Dir.resourceDir+"/结果/离婚纠纷结果/result.txt"
    for path in paths:
        text_list = tools.read_dir(path)
        string = ""
        for file in text_list.keys():
            text = text_list[file]

            result_laws = extract_laws(text)
            result_fact = extract_fact(text)
            result_result = extract_result(text)
            # print(text)
            string += tools.get_filename(file)+"\t"+text+"\t"+str(result_laws)+"\t"+str(result_fact)+"\t"+str(result_result)+"\n"

        tools.write(filepath,string)


            # string = tools.get_filename(file)+"\t"+str(result[0])[1:-1]+"\t"+str(result[1])[1:-1]+"\t"+str(result[2])[1:-1]+"\t"+str(result[3])[1:-1]
            # print(string)

def demo_text():
    text ="本院认为，被告人赵某某因琐事故意伤害他人身体，致一人轻伤二级，侵犯他人身体健康权，其行为已构成《中华人民共和国刑法》第二百三十四条第一款规定的故意伤害罪。西安市灞桥区人民检察院指控被告人所犯罪名成立，依法应予惩处。被告人赵某某系东江花园小区业主委员会负责人，因小区公共事务与被害人发生争吵，二人在相互谩骂过程中，赵某某持马扎致伤被害人，双方对矛盾激化均负有责任，案件审理过程中，赵某某已积极赔偿被害人经济损失，取得被害人谅解，依法可从轻处罚。"
    regex = "《.*?规定"
    result = re.findall(regex,text)
    print(result)
    # print(result)

# demo_text()



demo()
# print(list(jieba.cut("依法应予准许")))

# text = "(构成.*?罪)"
# judges = re.findall(text,sentence)
# print(judges)
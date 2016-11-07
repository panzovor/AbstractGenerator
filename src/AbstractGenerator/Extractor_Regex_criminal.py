# -*- coding: utf-8 -*-
__author__ = 'E440'
import re
import Dir
import src.FileTools.Tools as tools

def seperate_sentences(text):
    regex = "！|。|？|；"
    return re.split(regex,text)

def extract(text):
    regex_laws = ["《.*?规定","我国刑法规定","(触犯了.*?)(，|。)"]
    regex_facts = "(被告人|；)(.*?)构成"
    regex_guiltys = "(构成.*罪)"
    regex_judges =".*被告人.*处罚.*"
    laws_result,fact_result,guilty_result,judge_result=[],[],[],[]
    tmp_result =[]
    for sentence in seperate_sentences(text):
        ####提取法律
        for regex_law in regex_laws:
            if "《.*?规定" ==  regex_law:
                laws = re.findall(regex_law,sentence)
                for law in laws:
                    law = re.sub("的|之","",law)
                    laws_result.append(law[:-2])
                if laws.__len__() >0 :
                    break
            elif "我国刑法规定" == regex_law:
                index = sentence.find(regex_law)
                if index>=0:
                    if "不" not in sentence[:index]:
                        string  ="《中华人民共和国刑法》"
                        string+= ":"+sentence[index+6:]
                        laws_result.append(string)
                        break;
            else:
                laws = re.findall(regex_law,sentence)
                for law in laws:
                    law = law[0]
                    law = re.sub("(我国|，|。)","",law)
                    string = law[3:]
                    if string =="刑法" or string == "刑律":
                        string = "《中华人民共和国刑法》"
                    laws_result.append(string)
                if laws.__len__() >0 :
                    break
        ####提取事实
        facts = re.findall(regex_facts,sentence)
        for fact in facts:
            fact = str(fact[1])
            string = fact[:fact.rfind("，")]
            fact_result.append(string)

        ####提取罪名
        for subsentence in sentence.split("，"):
            guiltys = re.findall(regex_guiltys,subsentence)
            for guilty in guiltys:
                # if tmp  == None:
                #     print(guilty)
                string= guilty[2:]
                # print(string)
                if "了" in string:
                    string = re.sub("了","",string)
                if "规定" in string:
                    string = string[string.rindex("规定")+2:]
                    string = re.sub("的|了","",string)
                if string.__len__()>50:
                    if "犯" in string:
                        string = string[string.rindex("犯"):]
                if string.__len__()<=2:
                    continue
                # print(string)
                tmp_result.append(string)
        # print(guilty_result)


        ####提取判决
        judges = re.findall(regex_judges,sentence)
        for judge in judges:
            judge_result.append(judge)

    guilty_result.extend(list(set(tmp_result)))

    return laws_result,fact_result,guilty_result,judge_result

def demo():
    paths = [
    # Dir.resourceDir+"\\摘要文书\\故意伤害罪"
    # ,
             Dir.resourceDir+"\\摘要文书\\盗窃罪"
    ]
    content =""
    for path in paths:
        text_list = tools.read_dir(path)
        for file in text_list.keys():
            text = text_list[file]
            result = extract(text)

            string = tools.get_filename(file)+"\t"+text+"\t"+str(result[0])[1:-1]+"\t"+str(result[1])[1:-1]+"\t"+str(result[2])[1:-1]+"\t"+str(result[3])[1:-1]
            content +=string+"\n"
            print(string)

    filepath = Dir.resourceDir+"结果\\盗窃罪结果\\result.txt"
    tools.write(filepath,content)

def demo_text():
    text ="本院认为，被告人赵某某因琐事故意伤害他人身体，致一人轻伤二级，侵犯他人身体健康权，其行为已构成《中华人民共和国刑法》第二百三十四条第一款规定的故意伤害罪。西安市灞桥区人民检察院指控被告人所犯罪名成立，依法应予惩处。被告人赵某某系东江花园小区业主委员会负责人，因小区公共事务与被害人发生争吵，二人在相互谩骂过程中，赵某某持马扎致伤被害人，双方对矛盾激化均负有责任，案件审理过程中，赵某某已积极赔偿被害人经济损失，取得被害人谅解，依法可从轻处罚。"
    regex = "《.*?规定"
    result = re.findall(regex,text)
    print(result)
    # print(result)

# demo_text()

demo()
# text = "(构成.*?罪)"
# judges = re.findall(text,sentence)
# print(judges)
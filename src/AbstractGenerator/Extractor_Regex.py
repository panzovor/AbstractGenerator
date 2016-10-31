__author__ = 'E440'
import re
import Dir
import src.FileTools.Tools as tools

def seperate_sentences(text):
    regex = "！|。|？"
    return re.split(regex,text)

def extract(text):
    regex_laws = "《.*?规定"
    regex_facts = "(被告人|；)(.*?)构成"
    regex_guiltys = "(构成.*?罪)"
    regex_judges =".*被告人.*处罚.*"
    laws_result,fact_result,guilty_result,judge_result=[],[],[],[]
    for sentence in seperate_sentences(text):
        ####提取法律
        laws = re.findall(regex_laws,sentence)
        for law in laws:
            if re.match("的|之",law[-3]) !=None:
                laws_result.append(law[:-3])

        ####提取事实
        facts = re.findall(regex_facts,sentence)
        for fact in facts:
            fact = str(fact[1])
            string = fact[:fact.rfind("，")]
            fact_result.append(string)

        ####提取罪名
        guiltys = re.findall(regex_guiltys,sentence)
        for guilty in guiltys:
            guilty_result.append(guilty[2:])

        ####提取判决
        judges = re.findall(regex_judges,sentence)
        for judge in judges:
            judge_result.append(judge)

    return laws_result,fact_result,guilty_result,judge_result

def demo():
    paths = [
    Dir.resourceDir+"\\摘要文书\\故意伤害罪"
             # ,Dir.resourceDir+"\\摘要文书\\离婚纠纷",
             # Dir.resourceDir+"\\摘要文书\\盗窃罪"
             # Dir.resourceDir+"\\摘要文书\\民间借贷纠纷"
    ]
    for path in paths:
        text_list = tools.read_dir(path)
        for file in text_list.keys():
            text = text_list[file]
            result = extract(text)


            print(tools.get_filename(file),result)


demo()
# text = "(构成.*?罪)"
# judges = re.findall(text,sentence)
# print(judges)
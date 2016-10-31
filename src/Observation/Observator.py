__author__ = 'E440'
import Dir
import re
import src.FileTools.Tools as tools

def observate_sentence_lenth(filepath,savepath=Dir.resourceDir+"\\ObservationResult\\result_"):
    savepath += tools.get_filename(filepath)+".txt"
    result = tools.read_dir(filepath)
    split_regex = "。|？|！"
    observation_result =""
    print(filepath)
    tmp_result = {}
    for i in range(result.__len__()):
        length = re.split(split_regex,result[i]).__len__()
        if length not in tmp_result.keys():
            tmp_result[length] = 0
        tmp_result[length]+=1
        observation_result+= str(i)+"\t"+str(length)+"\n"
    # print(observation_result)
    for key in tmp_result.keys():
        print(str(key)+"\t"+str(tmp_result[key]))
    tools.write(savepath,observation_result)

observate_sentence_lenth(Dir.resourceDir+"摘要文书\离婚纠纷")
observate_sentence_lenth(Dir.resourceDir+"摘要文书\盗窃罪")
observate_sentence_lenth(Dir.resourceDir+"摘要文书\故意伤害罪")
observate_sentence_lenth(Dir.resourceDir+"摘要文书\民间借贷纠纷")
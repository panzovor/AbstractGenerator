__author__ = 'E440'
import jieba
import src.FileTools.Tools as tools
import math
import re
import Dir

def getTf(text):
    result ={}
    for sentence in re.split("。|！|？|；",text):
        words = jieba.cut(sentence)
        for word in words:
            if word not in result.keys():
                result[word] =0
            result[word]+=1
    return result

def combineTextAndGetTf(text_list):
    content,result = "",{}
    for name in text_list.keys():
        content += text_list[name]
    for sentence in content.split("。|？|！|；"):
        words = jieba.cut(sentence)
        for word in words :
            if word not in result.keys():
                result[word] = 0
            result[word]+=1

    for word in result.keys():
        print(word, "\t",result[word])

def gettfidf(text_list):
    tf,count ={},0
    for key in text_list.keys():
        text = text_list[key]
        tf[key]={}
        tf[key] = getTf(text)
    count = tf.__len__()
    reversed_index = {}
    for key in tf.keys():
        for word in tf[key].keys():
            if word not in reversed_index.keys():
                reversed_index[word] = []
            reversed_index[word].append(key)

    word_idf = {}
    for word in reversed_index.keys():
        # print(count,reversed_index[word].__len__()+1)
        idf = math.log(float(count)/float(reversed_index[word].__len__()+1),math.e)
        if word not in word_idf.keys():
            word_idf[word] = idf

    tfidf = {}
    for index in tf.keys():
        if index not in tfidf.keys():
            tfidf[index] = {}
        words  = tf[index]
        for word in words.keys():
            if word not in tfidf[index].keys():
                tfidf[index][word] = [words[word],word_idf[word],words[word]*word_idf[word]]
            print(word,tfidf[index][word])
    return tfidf

file_dir = Dir.resourceDir+"摘要文书\\离婚纠纷\\"
text_list = tools.read_dir(file_dir)
combineTextAndGetTf(text_list)
# result =gettfidf(text_list)
# for key in result.keys():
#     string =""
#     for word in result[key].keys():
#         string += word+":"+str(result[key][word])
#         string+="##"
#     string+="\n"
    # print(string)



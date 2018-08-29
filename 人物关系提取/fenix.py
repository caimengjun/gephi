
import jieba,codecs, math
import jieba.posseg as pseg

#这是我从网上找来的权利的游戏剧本，又有编码格式不对，我重新进行了编码，得到utf8的剧本
# with codecs.open("a.txt","r","GBK") as f:
#     p = f.read()
# with codecs.open("b.txt","w","utf8")as g:
#     g.write(p)
names = {}
relationships = {}
lineNames = []

jieba.load_userdict("dict.txt")        # 加载字典
with codecs.open("busan.txt", "r", "utf8") as f:
    for line in f.readlines():
        poss = pseg.cut(line)
        # 分词并返回该词词性
        lineNames.append([])        # 为新读入的一行添加人物名称列表
        for w in poss:
            # print(w.word,w.flag) #返回单词和单词类型
            if w.flag != "nr" or len(w.word) < 2:
                continue            # 当分词长度小于2或该词词性不为nr时认为该词不为人名
            lineNames[-1].append(w.word)        # 为当前段的环境增加一个人物
            if names.get(w.word) is None:
                names[w.word] = 0
                relationships[w.word] = {}
            names[w.word] += 1  # 该人物出现次数加 1


for line in lineNames:# 对于每一行
    for name1 in line:
        for name2 in line:                # 每段中的任意两个人
            if name1 == name2:
                continue
            if relationships[name1].get(name2) is None:        # 若两人尚未同时出现则新建项
                relationships[name1][name2]= 1
            else:
                relationships[name1][name2] = relationships[name1][name2]+ 1        # 两人共同出现次数加 1

with codecs.open("b_node.txt","w","utf8") as f:
    f.write("Id Lable Weight\r\n")  # \r默认表示将输出的内容返回到第一个指针，这样的话，后面的内容会覆盖前面的内容
    for name ,times in names.items():
        f.write(name +" "+str(times)+"\r\n")

with codecs.open("b_edge.txt", "w", "utf8") as f:
    f.write("Source Target Weight\r\n")
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 3:
                f.write(name + " " + v + " " + str(w) + "\r\n")



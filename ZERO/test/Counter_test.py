import re
from collections import Counter
from pprint import pprint
import jieba





with open(r"C:\Users\qhj01\Desktop\test.txt", "r",encoding="gbk") as f:
    txt = f.read()
txt = re.sub(r"[\s，的我你“”是了，在有很、就都！。]","",txt)

extracts = jieba.cut(txt, cut_all = False)
# extracts = jieba.cut_for_search(txt)
# l = []
# for word in extracts:
#     l.append(word)

word_counts = Counter(extracts)
pprint(word_counts.most_common(20))
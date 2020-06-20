# -*- coding: utf-8 -*-
"""
Created on Sun May 10 11:36:12 2020

@author: zxcvb
"""

import numpy as np
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import inaugural



def make_ngram(splited, n):
    """
    list(contain splited words) -> dict{tuple(word1, word2) : #of tuple}    
    """
    ngram_dict = dict()
    for i in range(len(splited)-(n-1)):
        tmp = []
        for w in splited[i:i+n]:
            tmp.append(w)
        agram  = tuple(tmp)
        if not agram in ngram_dict:
            ngram_dict[agram] = 1
        else:
            ngram_dict[agram] = ngram_dict[agram] + 1
            
    return ngram_dict




def getval(d, key):
    """
    return 0 when dict not contain that key
    """
    try: 
        return d[key]
    except KeyError:
        return 0
    


def cos_similarity(dict1, dict2):
    """
    cos-similarity test btw two dict{key : num} form
    """
    word_pool = list(set(list(dict1.keys()) + list(dict2.keys())))
    lst1, lst2 = [], []
    for word in word_pool:
        lst1.append(getval(dict1, word))
        lst2.append(getval(dict2, word))
    
    # vectors    
    vec1 = np.array(lst1)
    vec2 = np.array(lst2)
    
    # manually compute cosine similarity
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    cos = dot / (norm1 * norm2)
    
    return cos


"""
a = "hello world"
b = "hello world hello world"


bigram_a = make_ngram(a.split(), 1)
bigram_b = make_ngram(b.split(), 1)

print(cos_similarity(bigram_a, bigram_b))
"""





## main --------

## make corpus by crwaled articles
forward = PlaintextCorpusReader('./theforward', '.*')
fox = PlaintextCorpusReader('./foxnews', '.*')
## print(forward.fileids())
## print(fox.fileids())
## print(len(forward.words()))
## print(len(fox.words()))
## print(inaugural.words('1789-Washington.txt'))
## print(inaugural.fileids())


## make bigram
bigram_fox = make_ngram(forward.words(), 2)
bigram_forward = make_ngram(fox.words(), 2)

angle_dist = dict()
fox_dist = dict()
forward_dist = dict()

## 
for name in inaugural.fileids():

    bigram_speech = make_ngram(inaugural.words(name), 2)
    fox_cos = cos_similarity(bigram_fox, bigram_speech)
    forward_cos = cos_similarity(bigram_forward, bigram_speech)
    angle_dist[name] = fox_cos - forward_cos
    fox_dist[name] = fox_cos
    forward_dist[name] = forward_cos
    #print("foxnews : " + str(fox_cos))
    #print("forward : " + str(forward_cos))

"""
def f_val(x) :
    return x[1]

angle_dist_sorted = sorted(angle_dist.items(), key = f_val)
"""
## print(angle_dist)

  
f = open('output.csv', 'w')
f.write("""president name, cos_similarity with Fox, cos_similarity with Forward, difference btw two news company, year\n""")
for key in angle_dist:
    name = key[5:].replace(".txt", "")
    year = key[0:4]
    btw = angle_dist[key]
    fox = fox_dist[key]
    forward = forward_dist[key]
    
    f.write(f"""{name},{fox},{forward},{btw},{year}\n""")
    
f.close()

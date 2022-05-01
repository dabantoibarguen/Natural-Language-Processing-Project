import spacy
from sklearn.model_selection import StratifiedKFold
from EvoMSA.utils import LabelEncoderWrapper, bootstrap_confidence_interval
from microtc.utils import tweet_iterator
from b4msa.textmodel import TextModel
from spacy.vocab import Vocab
import numpy as np
from collections import Counter
from os.path import join
import random
import json
from matplotlib import pylab as plt
from sklearn.metrics.pairwise import cosine_distances
from sqlalchemy import false, true
from text_models import Vocabulary
from collections import Counter, defaultdict
from SparseArray import SparseArray
from tqdm import tqdm
from sklearn.svm import LinearSVC  
import sklearn   



D = json.load(open('export_2018-07-04_train.json'))
nlp = spacy.load("en_core_web_lg")
print('Wait until it says ready, then type. Say bye to end.\n')

sentences = []
vectors = []
D = D[::-1]
y = ''
prevpart = ""
pairs = dict()
for d in D:
    for i in reversed(range(len(d['dialog']))):
        s = d['dialog'][i]['text'].lower().strip()
        if("/" in s):
            prevpart = ""
            continue
        part = d['dialog'][i]['sender'].lower().strip()
        if(s not in pairs):
            pairs[s] = []
        sentences.append(s)
        vectors.append(nlp(s).vector)
        if(part == prevpart or prevpart == ""):            
            prevpart = part
            y = s
            continue
        else:
            pairs[s].append(y)
            y = s
            prevpart = part


# sentences = dict()
# y = ''
# for x in range(len(D)):
#     for i in range(len(D[x]['dialog'])):
#         temp = D[x]['dialog'][i]['text'].lower().strip()
#         if(D[x]['dialog'][i]['sender'] == 'participant1'):
#             if temp not in sentences.keys():
#                 sentences[temp] = list()
#                 y = temp
#             if(x<len(D)-1):
#                 sentences[temp].append(D[x+1]['dialog'][0]['text'].lower().strip())

#         if (D[x]['dialog'][i]['sender'] == 'participant2'):
#             if y in sentences.keys(): 
#                 sentences[y].append(temp)

# nlp = spacy.load("en_core_web_lg")
# def word2vector(word):
#   return nlp(word.lower().strip()).vector 

# W = []
# words = []

# strings = set([w.lower().strip() for w in sentences])
# for word in strings:
#     vector = nlp(word).vector
#     if np.fabs(vector).sum() > 0:
#         words.append(word)
#         W.append(vector)

# print(W)

loop = true

# for x in sentences:
#     if len(sentences[x]) ==0:
#         print(x)
print('Ready to Start\n')
while(loop):
    userinput = input()
    v = nlp(userinput.lower().strip()).vector
    if userinput == 'bye':
        break
    min = float('inf')
    minpos = 0
    for i in range(len(vectors)):
        cur = (np.linalg.norm(v-vectors[i]))
        if(cur < min):
            min = cur
            minpos = i

    arr = pairs[sentences[minpos]]
    rand = random.choice(arr)
    if pairs[rand] == None:
        print('unable to reply')
    else:
        printout = random.choice(pairs[rand])
        print(printout)

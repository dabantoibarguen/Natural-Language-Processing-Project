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


first = ''
second = ''
third = ''
fourth = ''

while(true):
    lan = input("Please choose a language (en for English, es for Spanish, fr for French): ")

    if(lan.lower() == 'es' or lan.lower() == 'spanish'):
        first = 'SPANISH_'
        second = 'SPANISH_'
        third = 'SPANISH_'
        fourth = 'SPANISH_'
        break
    elif(lan.lower() == 'fr' or lan.lower() == 'french'):
        first = 'FRENCH_'
        second = 'FRENCH_'
        third = 'FRENCH_'
        fourth = 'FRENCH_'
        break

    elif(lan.lower() == 'en' or lan.lower() == 'english'):        
        first = ''
        second = ''
        third = ''
        fourth = ''
        break
    else:
        print("please choose a valid language (en, es, fr): ")

first += 'export_2018-07-04_train.json'
second += 'export_2018-07-05_train.json'
third += 'export_2018-07-06_train.json'
fourth += 'export_2018-07-07_train.json'


if(lan == 'en'):
    print('Wait until it says ready, then type. Say bye to end.\n')
elif(lan == 'es'):
    print('Wait until it says ready, then type. Say adios to end.\n')
elif(lan == 'fr'):
    print('Wait until it says ready, then type. Say au revoir to end.\n')
corpuses = []

corpuses.append(first)
corpuses.append(second)
corpuses.append(third)
corpuses.append(fourth)
for i in range(len(corpuses)):

    D = json.load(open(corpuses[i]))

    sentences = dict()
    y = ''
    for x in range(len(D)):
        for i in range(len(D[x]['dialog'])):
            temp = D[x]['dialog'][i]['text'].lower().strip()
            if(D[x]['dialog'][i]['sender'] == 'participant1'):
                if temp not in sentences.keys():
                    sentences[temp] = list()
                    y = temp
                if(x<len(D)-1):
                    #sentences[temp].append(D[x+1]['dialog'][0]['text'].lower().strip())
                    
                    
                    for k in range(len(D[x+1]['dialog'])):
                        #p2 = p2 + (D[x+1]['dialog'][k]['text'].lower().strip())
                        sentences[temp].append(D[x+1]['dialog'][k]['text'].lower().strip())
                    
        '''
            if (D[x]['dialog'][i]['sender'] == 'participant2'):
                if y in sentences.keys(): 
                    sentences[y].append(temp)
        '''
nlp = spacy.load("en_core_web_lg")
def word2vector(word):
  return nlp(word.lower().strip()).vector 

W = []
words = []

strings = set([w.lower().strip() for w in sentences])
for word in strings:
    vector = nlp(word).vector
    if np.fabs(vector).sum() > 0:
        words.append(word)
        W.append(vector)

loop = true
print('Ready to Start\n')
while(loop):
    userinput = input()
    if(lan == 'en' and userinput.lower() == 'bye'):
        print('bot: Bye!')
    elif(lan == 'es' and userinput.lower() == 'adios'):
        print("bot: Adios!")
        break
    elif(lan == 'fr' and userinput.lower() == 'au revoir'):
        print("bot: Au revoir!")
        break
    dis = cosine_distances(np.atleast_2d(word2vector(userinput)), W)

    r = np.argsort(dis[0])
    arr = [words[x] for x in r[:2]]
    rand = random.choice(arr)
    
    if sentences[rand] == None:
        print('unable to reply')
    else:
        printout = random.choice(sentences[rand])
        print('bot: ' + printout)
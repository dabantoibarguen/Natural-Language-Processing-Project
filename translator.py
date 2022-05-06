from matplotlib.font_manager import json_dump
from sklearn.ensemble import GradientBoostingClassifier
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
from googletrans import Translator, constants


D = json.load(open('export_2018-07-07_train.json'))
trans = Translator()
file = open("FRENCH_export_2018-07-07_train.json", "w")

# Choose a language: (make lan en for English, es for Spanish, ar for Arabic)
lan = 'fr'

count = 0
for x in range(len(D)):
    for i in range(len(D[x]['dialog'])):
        temp = D[x]['dialog'][i]['text']
        if(lan != "en"):
            temp = trans.translate(temp, dest=lan).text
        D[x]['dialog'][i]['text'] = temp

json.dump(D, file)
"""# -*- c77777oding: utf-8 -*-
import os
#import warnings
#warnings.filterwarnings("ignore", category=FutureWarning)

import pandas as pd

df = pd.read_csv("fb_charts_parsed_tab_211118.csv", header=0, sep="\t", index_col=0, parse_dates=True, error_bad_lines=False)
#

print(df.shape)

print(list(df.tail(10)))

exit(8)



print(df.shape)

df.to_csv("ciao.csv", sep=";")

print(df.head(5))
#print(str.encode(df.iloc[0], 'utf-8'))
#print(df.iloc[0])
"""


"""
print(str(df['lyrics_body'].iloc[0]).replace("\n\n","\n").replace("\n", " "))
print("\n\n\n")
print(str(df['translation_lyrics_body_nmt'].iloc[0]).replace("\n\n","\n").replace("\n", " "))


import gensim 
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from scipy import spatial

fname = "apnews_dbow/doc2vec.bin"
model = Doc2Vec.load(fname) 

#a1 = [str(df['lyrics_body'].iloc[0]).replace("\n\n","\n").replace("\n", " ")]
#a2 = [str(df['translation_lyrics_body_nmt'].iloc[0]).replace("\n\n","\n").replace("\n", " ")]

a1 = str(df['lyrics_body'].iloc[0]).replace("\n\n","\n")
a2 = str(df['translation_lyrics_body_nmt'].iloc[10]).replace("\n\n","\n")

a1 = a1.split("\n")
a2 = a2.split("\n")

print(len(a1))
print(len(a2))

for i in range(len(a1)):
    vector1 = model.infer_vector(a1[i])
    vector2 = model.infer_vector(a2[i])
    similarityDoc2Vec = 1 - spatial.distance.cosine(vector1,vector2)

    print(a1[i])
    print(a2[i])
    print(similarity)
    print("\n\n")
"""

import os
import pandas as pd
import scipy
import re
import nltk
import numpy as np
from math import fabs
import scipy.spatial.distance as dist
import gensim

from nltk.corpus import stopwords
from nltk import download
download('stopwords')  # Download stopwords list.


from gensim.models import Word2Vec
if not os.path.exists('w2v_googlenews/GoogleNews-vectors-negative300.bin.gz'):
    raise ValueError("SKIP: You need to download the google news model")

print("Loading W2V.....")
model = gensim.models.KeyedVectors.load_word2vec_format('w2v_googlenews/GoogleNews-vectors-negative300.bin.gz', binary=True)
print("......Loaded")

df_input = pd.read_csv('fb_charts_parsed_tab_211118.csv', sep="\t", parse_dates=True, error_bad_lines=False)


df = df_input[['lyrics_body','translation_lyrics_body_nmt']]

from service.client import BertClient
bc = BertClient(ip='192.168.20.113', port=5555)

scores = []

for i in range(len(df)):

    print(str(i) + "/" + str(len(df)-1))
    
    a1 = str(df['lyrics_body'].iloc[i])
    a1 = re.sub(r'\n+', '\n', a1)

    a2 = str(df['translation_lyrics_body_nmt'].iloc[i])
    a2 = re.sub(r'\n+', '\n', a2)

    a1 = a1.split("\n")
    a2 = a2.split("\n")

    if len(a1)!=len(a2):
        scores.append(-1)
        continue

    not_good = 0
    good = 0

    for line in range(len(a1)):

        str1 = str(a1[line]).decode('ascii',errors='ignore').encode().lower()
        str2 = str(a2[line]).decode('ascii',errors='ignore').encode().lower()
        
        v1, v2 = bc.encode([str1,str2])

        similarity = scipy.spatial.distance

        diff_len_words = int(fabs(len(a1[line].split(" ")) - len(a2[line].split(" "))))

        # Remove stopwords.
        stop_words = stopwords.words('english')

        str1_w2v = [w for w in str1 if w not in stop_words]
        str2_w2v = [w for w in str2 if w not in stop_words]

        #print 'Chebyshev similarity is', 1/(1+dist.chebyshev(v1, v2))
        #print 'Cosine similarity is', 1 - dist.cosine(v1, v2)
        #print 'WMT similarity (WORD2VEC)', 1/(1+model.wmdistance(str1_w2v,str2_w2v))
        

        if 1/(1+dist.chebyshev(v1, v2)) + 1 - dist.cosine(v1, v2) + 1/(1+model.wmdistance(str1_w2v,str2_w2v)) > 1.70:
            good+=1
        else:
            not_good+=1

    scores.append( round( 1.* good/(good+not_good) , 2) ) 

df_input['translation_quality'] = pd.Series(scores, index=df.index)

cols = df_input.columns.tolist()
df = df_input [ cols[:14] + [cols[-1]] + cols[14:-1] ] 

df.to_csv('output_fb_charts_parsed_tab_211118.csv', sep="\t")
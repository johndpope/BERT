
#BERT_paper_50k-100k.txt
#BERT_paper_1-50k.txt
import os
import sys
import pandas as pd
import numpy as np

filename="BERT_paper_50k-100k.txt"

if len(sys.argv) !=2:
    print("USAGE: " + str(sys.argv[0]) + " filename")
    exit(1)

fin = open(filename,'r', encoding="utf-8")

lines = fin.readlines()
fin.close()

print(lines[0])

data = pd.read_csv(str(sys.argv[1]), sep=",")
print(data.columns)

ids = data['id'].values.tolist()
c_IDs= data['commontrack_id'].values.tolist()
starts = data['start'].values.tolist()

import json

if os.path.exists("BERT.embedding") and filename == "BERT_paper_1-50k.txt":
    os.remove("BERT.embedding")

with open("BERT.embedding", "a") as fout:
    if filename == 'BERT_paper_1-50k.txt':
        fout.write("id,id_start,bert\n")

    for index, l in enumerate(lines):
        if index % 1000 == 0:
            print(index+50000)
            
        data = json.loads(l)
        features = data['features']
        tokens_features = []

        for f in features:
            if str(f['token'])=='[CLS]' or str(f['token'])=='[SEP]':
                continue
            tokens_features.append(list(f['layers'][0]['values']))

        mean = np.mean(tokens_features, axis=0)

        fout.write(str(ids[index+50000]) +"," +str(c_IDs[index+50000]) + str(starts[index+50000]) +  ",")
        np.savetxt(fout, np.array([mean]))#, fmt='%.5f')

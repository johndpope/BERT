# -*- coding: utf-8 -*-
import sys
import pandas as pd
import os
import numpy as np


os.environ['BERT_BASE_DIR'] = 'multilingual_L-12_H-768_A-12'

if len(sys.argv) !=3:
    print("USAGE: " + str(sys.argv[0]) + " filename column_name")
    exit(1)

data = pd.read_csv(str(sys.argv[1]), sep=",")
print(data.columns)

ids = data['id'].values.tolist()
c_IDs= data['commontrack_id'].values.tolist()
starts = data['start'].values.tolist()

data= data[[str(sys.argv[2])]].values.tolist()



fin = open("sentences.txt",'w', encoding="utf-8")

for i, line in enumerate(data[50000:]):
    line = str(line[0])
    fin.write(line + "\n")

fin.close()
os.system("wc -l sentences.txt")
print("Extracting features.........")
os.system(
            'python3 extract_features.py \
              --input_file=sentences.txt \
              --output_file=output.txt \
              --vocab_file=$BERT_BASE_DIR/vocab.txt \
              --bert_config_file=$BERT_BASE_DIR/bert_config.json \
              --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
              --layers=-2 \
              --max_seq_length=128 \
              --batch_size=8'
        )


os.system('rm sentences.txt')

exit(6) 

fin = open("output.txt",'r', encoding="utf-8")

lines = fin.readlines()
fin.close()

import json

if os.path.exists("BERT.embedding"):
    os.remove("BERT.embedding")

with open("BERT.embedding", "a") as fout:
    fout.write("id,id_start,bert\n")
    for index, l in enumerate(lines):
        data = json.loads(l)
        features = data['features']
        tokens_features = []

        for f in features:
            if str(f['token'])=='[CLS]' or str(f['token'])=='[SEP]':
                continue
            print(f['token'])
            tokens_features.append(list(f['layers'][0]['values']))

        mean = np.mean(tokens_features, axis=0)

        fout.write(str(ids[i]) +"," +str(c_IDs[i]) + str(starts[i]) +  ",")
        np.savetxt(fout, np.array([mean]))#, fmt='%.5f')
        

       

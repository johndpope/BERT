#!/bin/bash


apt-get update &&  apt-get install -y  git     curl     wget     vim     apt-utils     nano     unzip     python3-pip python3-dev     python3-tk --allow-unauthenticated
pip3 install -r requirements.txt

cd src/

#wget https://storage.googleapis.com/bert_models/2018_11_03/multilingual_L-12_H-768_A-12.zip
#unzip multilingual_L-12_H-768_A-12.zip
#rm multilingual_L-12_H-768_A-12.zip


#python3 download_glue_data.py --data_dir glue_data --tasks all

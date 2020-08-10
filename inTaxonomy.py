from bs4 import BeautifulSoup 
import codecs
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.corpus import stopwords  
from nltk.tokenize import regexp_tokenize
import pandas as pd
import numpy as np
import nltk
import os
import random
bigrams_dataset=[]
nltk.download('stopwords')
stop_words = set(stopwords.words('english')) 
vectorizer = CountVectorizer(ngram_range = (2,2)) 

def uniqued(list1): 
    x = np.array(list1) 
    y=np.unique(x)
    return y

def inTaxonomy(df,bigrams):
  bigraminT=[]
  for ele in bigrams:
    if ele in df.values:
      #print(ele,':present')
      bigraminT.append(ele)
  return bigraminT

def removeElements(features):
    w=[]
    for ele in features:
        w=ele.split()
        count=0
        for ment in w:
            if ment in stop_words:
                count +=1
        if count>0:
            features.remove(ele) 

    return features
         

def remove_string_special_characters(s): 
      
    # removes special characters with ' ' 
    stripped = re.sub('[^a-zA-z\s]', '', s) 
    stripped = re.sub('_', '', stripped) 
      
    # Change any white space to one space 
    stripped = re.sub('\s+', ' ', stripped) 
      
    # Remove start and end white spaces 
    stripped = stripped.strip() 
    if stripped != '': 
            return stripped.lower() 


#reading the taxonomy file
df = pd.read_csv (r'C:\Users\saran\Downloads\lemmatisation_final.csv') 

#path of xml files
path ='C:/Users/saran/Documents/Git/Dataset/Ontology/HTML'

for file in os.listdir(path):
  i=1
  os.chdir(path)
  f = codecs.open(path + '/' + file, 'r', 'utf-8', errors= 'ignore')
  g = f.read()
  bsdata = BeautifulSoup(g, 'html.parser')


  

  
  try:
        data_details = bsdata.find('div', {'class':"Concept_Details"}).string.strip()
  except (AttributeError, KeyError):
        data_details = ""
  #html_dataset.append(data_title)

  text=remove_string_special_characters(data_details) #removing special characters and converting lo lower case
  #to obtain bigrams
  bigrams=[]

  try:
      vectorizer = CountVectorizer(ngram_range = (2,2)) 
      X1 = vectorizer.fit_transform([text]) 
      bigrams = (vectorizer.get_feature_names())
      #print(features)
      bigrams=removeElements(bigrams)
      bigrams=inTaxonomy(df, bigrams)
      bigrams=uniqued(bigrams)
      for i in range(len(bigrams)):
          head = bsdata.find('head')
          meta = bsdata.new_tag('meta')
          meta['content'] =bigrams[i]
          head.insert(0,meta)

  except(AttributeError, KeyError,ValueError):
        continue




  #to obtain unigrams
  modified_text=regexp_tokenize(text, "[\w']+")
  filtered_sentence = [w for w in modified_text if not w in stop_words] 
  unigrams=[]
  unigrams=inTaxonomy(df,filtered_sentence)
  unigrams=uniqued(unigrams)

  for i in range(len(unigrams)):
    head = bsdata.find('head')
    meta = bsdata.new_tag('meta')
    meta['content'] =unigrams[i]
    
    head.insert(0,meta)
  
  

 




  
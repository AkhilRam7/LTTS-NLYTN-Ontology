from urllib.parse import urlparse
base_url='http://lookup.dbpedia.org/api/search/KeywordSearch?QueryClass&QueryString={}'

from bs4 import BeautifulSoup 
import codecs
import os
import nltk
import re
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import regexp_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()   
nltk.download('wordnet')
nltk.download('stopwords')
stop_words = set(stopwords.words('english')) 

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


#path ='C:/Users/saran/Documents/Git/Dataset/Ontology/HTML'
path = 'C:/Users/saran/Desktop/checking'

for file in os.listdir(path):
  
  os.chdir(path)
  f = codecs.open(path + '/' + file, 'r', 'utf-8', errors= 'ignore')
  g = f.read()
  bsdata = BeautifulSoup(g, 'html.parser')
  try:
      data_details = bsdata.find('div', {'class':"Concept_Title"}).string.strip()
  except (AttributeError, KeyError):

      data_details = ""

  text=remove_string_special_characters(data_details) #removing special characters and converting lo lower case
  print(text)

  modified_text=regexp_tokenize(text, "[\w']+")
  filtered_sentence = [w for w in modified_text if not w in stop_words] 

  for ele in filtered_sentence:
      
      ele=lemmatizer.lemmatize(ele)
  hyperlink_format = '<a href="{link}">{text}</a>'
  link_text = hyperlink_format.format
  link_text(link='http://foo/bar', text='foo bar')
  import functools

  link_text = functools.partial(hyperlink_format.format)
  bsdata.body.find('div', {'class':'Concept_Title'}).string = ''

  for token in filtered_sentence:
      new = bsdata.new_tag("a", href=base_url.format(lemmatizer.lemmatize(token)))
      new.string = token
      bsdata.body.find('div', {'class':'Concept_Title'}).append(new)
  #f = codecs.open('/content/Abstract_PID_000124.html','w','utf-8',errors='ignore' )
  f = codecs.open(path + '/' + file, 'w', 'utf-8', errors= 'ignore')
  f.write(str(bsdata)) 
  f.close()
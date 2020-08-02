import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle 
import json
import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')


sw = set(stopwords.words('english'))
#stopwords = nltk.corpus.stopwords.words('english')
ps = PorterStemmer()

# ps.stem("jumping")        # It reduces the size of the vocabulary
# ps.stem("jumped")

def clean_text(sample):
    sample = sample.lower()
    sample = sample.replace("<br /><br />", " ")
    sample = re.sub("[^a-zA-Z]+", " ", sample)
    
    sample = sample.split()
    
    sample = [ps.stem(s) for s in sample if s not in sw] 
    # List Comprehension -> Doing this it will remove all the stopwords from sample
    
    sample = " ".join(sample)

    return sample


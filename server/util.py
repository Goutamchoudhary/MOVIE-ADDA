import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle 
import json
import pandas as pd
import numpy as np
from tensorflow import keras
import tensorflow as tf

import nltk


classifier = None
_cv = None
_tfidf = None
movies_list = None
corrMatrix = None


sw = set(stopwords.words('english'))
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


def load_saved_artifacts():
  print("loading saved artifacts......start")
  
  global classifier
  global _cv
  global _tfidf
  global movies_list
  global corrMatrix
  
  # Below code is just to handle the error->failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED

  gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.333)
  sess = tf.compat.v1.Session(config = tf.compat.v1.ConfigProto(gpu_options=gpu_options))
  tf.compat.v1.keras.backend.set_session(sess)

  
  # Load the Movie Rating Prediction model  
  classifier = keras.models.load_model("./artifacts/my_model")
 
  # Load the CountVectorizer object and TfidfTransformer from disk
  _cv = pickle.load(open('./artifacts/cv-transform.pkl','rb'))
  _tfidf = pickle.load(open('./artifacts/tfidf-transform.pkl','rb'))
  
  # Load the list of movies of our recommender system
  movies_list = json.load(open('./artifacts/List_of_movies.json', 'r'))['Movie_titles']
  
  # Load correlation Matrix pickle file
  corrMatrix = pd.read_pickle('./artifacts/corrMatrix.pkl')


  print("loading saved artifacts...done")


# First you convert the matrix to COO format. Then you extract the indices,   values, and shape
# and pass those directly to the SparseTensor constructor

def convert_sparse_matrix_to_sparse_tensor(X):
    coo = X.tocoo()
    indices = np.mat([coo.row, coo.col]).transpose()
    return tf.SparseTensor(indices, coo.data, coo.shape)


def prediction(review):
  cleaned_review = clean_text(review)
  cleaned_review = [cleaned_review]
  vect = _cv.transform(cleaned_review).toarray()
  rev = _tfidf.transform(vect)
  
  rev_sparse_tensor = convert_sparse_matrix_to_sparse_tensor(rev)
  final_review = tf.sparse.reorder(rev_sparse_tensor)

  my_prediction = classifier.predict(final_review)
  predicted_value = my_prediction.item(0)
  print(predicted_value)

  if predicted_value >= 0.5:
    prediction_status = "Great! This is the Positive review."
  else:
    prediction_status = "Oops! This is the Negative review."
  

  return prediction_status
  

# Movie Recommendation Engine

def get_movies_list():
  return movies_list


def get_similar(movie_name,rating):
  similar_ratings = corrMatrix[movie_name]*(rating-2.5)
  similar_ratings = similar_ratings.sort_values(ascending=False)
  # print(type(similar_ratings))
  return similar_ratings

def Recommendation(movies_sample):
  similar_movies = pd.DataFrame()
  for movie,rating in movies_sample:
    similar_movies = similar_movies.append(get_similar(movie,rating),ignore_index = True)
  
  similar_movies_final = similar_movies.sum().sort_values(ascending=False).head(20)
  recommendation = pd.DataFrame(similar_movies_final, columns=['Correlation'])
  recommendation2 = recommendation.dropna().reset_index()
  recommendation2.rename(columns= {'index':'title'}, inplace=True)
  final_recommendation = recommendation2.iloc[2:, :]
  recommendations_list = []
  for ind in final_recommendation.index:
    recommendations_list.append(final_recommendation['title'][ind])

  return recommendations_list  



if __name__ == '__main__':
  load_saved_artifacts()
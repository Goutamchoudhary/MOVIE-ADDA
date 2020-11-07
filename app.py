# Importing essential libraries
from flask import Flask, render_template, request, url_for, jsonify
import util
import pickle 
import json
import pandas as pd
import numpy as np
from tensorflow import keras
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1" 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf


app = Flask(__name__)

# Load the Movie Rating Prediction model  
classifier = keras.models.load_model("my_model")
# Load the CountVectorizer object and TfidfTransformer from disk
_cv = pickle.load(open('cv-transform.pkl','rb'))
_tfidf = pickle.load(open('tfidf-transform.pkl','rb'))
# Load the list of movies of our recommender system
movies_list = json.load(open('List_of_movies.json', 'r'))['Movie_titles']
# Load correlation Matrix pickle file
corrMatrix = pd.read_pickle('corrMatrix.pkl')

def convert_sparse_matrix_to_sparse_tensor(X):
  coo = X.tocoo()
  indices = np.mat([coo.row, coo.col]).transpose()
  return tf.compat.v1.sparse.SparseTensor(indices, coo.data, coo.shape)


def prediction(review):
  global classifier
  global _cv
  global _tfidf
  cleaned_review = util.clean_text(review)
  cleaned_review = [cleaned_review]
  vect = _cv.transform(cleaned_review).toarray()
  rev = _tfidf.transform(vect)
  
  rev_sparse_tensor = convert_sparse_matrix_to_sparse_tensor(rev)
  ordered_sparse_tensor = tf.compat.v1.sparse.reorder(rev_sparse_tensor)
  my_prediction = classifier.predict(ordered_sparse_tensor)
  predicted_value = my_prediction.item(0)
  print(predicted_value)

  if predicted_value >= 0.5:
    prediction_status = "Great! This is the Positive review."
    print("Hello1")
  elif predicted_value < 0.5:
    prediction_status = "Oops! This is the Negative review."
    print("Hello2")
  
  return prediction_status


@app.route('/')
def home():
  return render_template("index.html")

@app.route('/Home')
def index():
  return render_template("index.html")

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/contact')
def contact():
  return render_template("contact.html")


@app.route('/get_movies_list')
def get_movies_list():
 
  response = jsonify({
      'movies_list':  movies_list
  })
  response.headers.add('Access-Control-Allow-Origin', '*')

  return response


@app.route('/predict_review', methods=['POST'])
def predict_review():

  review = str(request.form['review'])
            
  response = jsonify({
      'my_prediction': prediction(review)
  })
  
  response.headers.add('Access-Control-Allow-Origin', '*')

  return response


def get_similar(movie_name,rating):
  global corrMatrix
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


@app.route('/predict_movies', methods=['POST'])
def predict_movies():
  movie_name_1 = request.form['movie_name_1']
  movie_name_2 = request.form['movie_name_2']
  rating_1 = int(request.form['rating_1'])
  rating_2 = int(request.form['rating_2'])
  movie_name_1 = str(movie_name_1)
  movie_name_2 = str(movie_name_2)
  tuplex_1 = (movie_name_1, rating_1)
  tuplex_2 = (movie_name_2, rating_2)
  movies_sample = []
  movies_sample.extend([tuplex_1, tuplex_2])
  movies_recom_list = Recommendation(movies_sample)

  response = jsonify({
      'movie1': movies_recom_list[0],
      'movie2': movies_recom_list[1],
      'movie3': movies_recom_list[2],
      'movie4': movies_recom_list[3],
      'movie5': movies_recom_list[4]
  })
  response.headers.add('Access-Control-Allow-Origin', '*')

  return response


 
if __name__ == '__main__':
 
  app.run(debug=True)
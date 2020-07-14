# Importing essential libraries
from flask import Flask, render_template, request, url_for, jsonify
import util


app = Flask(__name__)


@app.route('/get_movies_list')
def get_movies_list():
  response = jsonify({
      'movies_list': util.get_movies_list()
  })
  response.headers.add('Access-Control-Allow-Origin', '*')

  return response


@app.route('/predict_review', methods=['POST'])
def predict_review():
  review = request.form['review']
            
  response = jsonify({
      'my_prediction': util.prediction(review)
  })
  
  """response.headers.add('Access-Control-Allow-Origin', '*') """

  return response


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
  movies_recom_list = util.Recommendation(movies_sample)

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
  
  util.load_saved_artifacts()
  
  app.run(debug=True)
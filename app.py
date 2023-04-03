import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, db_drop_and_create_all, Movies, Actors
from auth.auth import requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  db_drop_and_create_all(app)
  CORS(app)


  # @app.route('/', methods = ['GET'])
  # def index():

  #     return jsonify({
  #         'success': True,
  #         'message':'Backend of Capstone casting project is  Successfully connected.'})


  @app.route('/', methods=['GET'])
  def index():
    return jsonify({"HelDDlo":'World'})

  @app.route('/movies',methods=['GET'])
  @requires_auth('get:movies')
  def movies(payload):
    movies = Movies.query.all()
    
    resp=[]
    for movie in movies:
      mov = {

      
        'id' :  movie.id,
        'title' : movie.title,
        'date' : movie.date,
        'actors': []
      }
      actors=movie.actors
      print('movie.actors')
      print(movie.actors)
      movActors = []
      for actor in actors:
        movActors.append({
          'id':actor.id,
          'name':actor.name,
          'age':actor.age,
          'gender': actor.gender

        })
      mov['actors'] = movActors
      resp.append(mov)
      
    return jsonify({"resp":resp})


  @app.route('/actors',methods=['POST'])
  @requires_auth('post:actors')
  def postactor(payload):
    # actors = Actors.query.all()
    req = request.get_json()

    req_recipe = req['recipe']
    movie = Movies()
    movie.title = req['title']
    
    resp=[]
    for actor in actors:
      movie = Movies.query.get(actor.movie_id)

      act = {

      
        'id' :  actor.id,
        'name' : actor.name,
        'age' : actor.age,
        'gender' : actor.gender,
        'movie': movie.title
        

      }
      resp.append(act)
      
    return jsonify({"resp":resp})



  @app.route('/actors',methods=['GET'])
  @requires_auth('get:actors')
  def actors(payload):
    actors = Actors.query.all()
    
    resp=[]
    for actor in actors:
      movie = Movies.query.get(actor.movie_id)

      act = {

      
        'id' :  actor.id,
        'name' : actor.name,
        'age' : actor.age,
        'gender' : actor.gender,
        'movie': movie.title
        

      }
      resp.append(act)
      
    return jsonify({"resp":resp})



  return app


app = create_app()

if __name__ == '__main__':

  app.run(host='0.0.0.0', port=8080, debug=True)
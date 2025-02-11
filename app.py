import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import requires_auth
from models import setup_db, Movie, Actor

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    with app.app_context():
      @app.route('/movies', methods=['GET'])
      @requires_auth('get:movies')
      def get_movies(payload):
          movies = Movie.query.all()
          return jsonify({'movies': [movie.format() for movie in movies]}), 200

      @app.route('/actors', methods=['GET'])
      @requires_auth('get:actors')
      def get_actors(payload):
          actors = Actor.query.all()
          return jsonify({'actors': [actor.format() for actor in actors]}), 200

      @app.route('/movies', methods=['POST'])
      @requires_auth('post:movies')
      def create_movie(payload):
          data = request.get_json()
          if not data or 'title' not in data or 'release_date' not in data:
              abort(400, "title and release_date is required")
          
          new_movie = Movie(title=data['title'], release_date=data['release_date'])
          new_movie.insert()
          return jsonify({'message': 'Movie added successfully!'}), 201
      
      @app.route('/actors', methods=['POST'])
      @requires_auth('post:actors')
      def create_actor(payload):
          data = request.get_json()

          if not data or 'name' not in data or 'age' not in data or 'gender' not in data:
              abort(400, "Name, age, and gender are required.")

          new_actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
          new_actor.insert()
          
          return jsonify({
              'success': True,
              'actor': new_actor.format()
          }), 201

      @app.route('/actors/<int:actor_id>', methods=['PATCH'])
      @requires_auth('patch:actors')
      def update_actor(payload, actor_id):
          actor = Actor.query.get(actor_id)
          if not actor:
              abort(404, "actor not found")
          
          data = request.get_json()
          actor.name = data.get('name', actor.name)
          actor.age = data.get('age', actor.age)
          actor.gender = data.get('gender', actor.gender)
          actor.update()
          
          return jsonify({'message': 'Actor updated successfully!'}), 200
      
      @app.route('/movies/<int:movie_id>', methods=['PATCH'])
      @requires_auth('patch:movies')
      def update_movie(payload, movie_id):
          movie = Movie.query.get(movie_id)
          if not movie:
              abort(404, "Movie not found.")
          
          data = request.get_json()
          movie.title = data.get('title', movie.title)
          movie.release_date = data.get('release_date', movie.release_date)
          movie.update()

          return jsonify({'message': 'Movie updated successfully!'}), 200

      @app.route('/actors/<int:actor_id>', methods=['DELETE'])
      @requires_auth('delete:actors')
      def delete_actor(payload, actor_id):
          actor = Actor.query.get(actor_id)
          if not actor:
              abort(404, "Actor not found.")
          
          actor.delete()
          return jsonify({'message': 'Actor deleted successfully!'}), 200


      @app.route('/movies/<int:movie_id>', methods=['DELETE'])
      @requires_auth('delete:movies')
      def delete_movie(payload, movie_id):
          movie = Movie.query.get(movie_id)
          if not movie:
              abort(404,"Movie not found")
          
          movie.delete()
          return jsonify({'message': 'Movie deleted successfully!'}), 200

      from flask import jsonify

      # Error handler for 400 - Bad Request
      @app.errorhandler(400)
      def bad_request(error):
          return jsonify({
              "success": False,
              "error": 400,
              "message": str(error)
          }), 400

      # Error handler for 404 - Not Found
      @app.errorhandler(404)
      def not_found(error):
          return jsonify({
              "success": False,
              "error": 404,
              "message": str(error)
          }), 404

      # Error handler for 422 - Unprocessable Entity
      @app.errorhandler(422)
      def unprocessable(error):
          return jsonify({
              "success": False,
              "error": 422,
              "message": "Unprocessable entity"
          }), 422

      # Error handler for 405 - Method Not Allowed
      @app.errorhandler(405)
      def method_not_allowed(error):
          return jsonify({
              "success": False,
              "error": 405,
              "message": "Method not allowed"
          }), 405

      # Error handler for 500 - Internal Server Error
      @app.errorhandler(500)
      def internal_server_error(error):
          return jsonify({
              "success": False,
              "error": 500,
              "message": "Internal server error"
          }), 500


      return app

APP = create_app()

if __name__ == '__main__':
    APP.run(debug=True)

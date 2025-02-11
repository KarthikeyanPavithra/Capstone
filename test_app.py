import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import db

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_path = "postgresql://localhost:5432/casting_test"

        self.production_exec_token = os.environ['PRODUCER_TOKEN']
        self.assistant_token = os.environ['ASSISTANT_TOKEN']
        self.director_token = os.environ['ASSISTANT_TOKEN']
        self.invalid_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVpNk11SmdGUE1qNTVrYUR1X0MxSSJ9.eyJpc3MiOiJodHRwczovL3Bhdmlkc25kLmpwLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2FiOGVjYzI0ZTA2NDI2ZTU5NTkzZGUiLCJhdWQiOiJtZWRpYSIsImlhdCI6MTczOTI5NjU0NiwiZXhwIjoxNzM5MzAzNzQ2LCJzY29wZSI6IiIsImF6cCI6IkxWM1gxVmJvT2JFZno2bVIxRXhJWTJQYkhneExnbEltIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.QbXr8z_lHA-qemrQi0_-vPoX7tEPeaZnlIIwdZBxFGCyfV4K-DVEhlJ7M4_aNPh-KnuJlALXEpGSyw3hZBzgAz3xuAyxyo1-G5ZeaNuiE87-dJgYfxzVt4VQPNAEZZ7OAEsPIALbya_Y97kLZq_wmWMShNZOW2j6ZGBUQ0_OXi8yN5BTNHFh2hikGwqHqqujEVWlzdSMBx01eVS3lfDqSKx5MKMpk3f5p7Q2rHprLZmrsMRcfnw5n6u4fXL-fX4TgZQk8F3MvcdwN7sCvd7VlE_X9uD8k5-Pjwz3asMgojfDmkxDGN6KUX8B2JDYDAzQVXDNcVYrQ611xH492pKzag"
        

        with self.app.app_context():
           db.create_all()

    def get_headers(self, token):
        return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    def test_get_movies_as_director(self):
        res = self.client().get('/movies', headers=self.get_headers(self.director_token))
        self.assertEqual(res.status_code, 200)

    def test_get_movies_as_actor(self):
        res = self.client().get('/movies', headers=self.get_headers(self.assistant_token))
        self.assertEqual(res.status_code, 200)

    def test_get_movies_as_production_exec(self):
        res = self.client().get('/movies', headers=self.get_headers(self.production_exec_token))
        self.assertEqual(res.status_code, 200)

    def test_add_movie_as_director(self):
        new_movie = {"title": "New Movie", "release_date": "2025-01-01"}
        res = self.client().post('/movies', headers=self.get_headers(self.director_token), json=new_movie)
        self.assertEqual(res.status_code, 403)

    def test_add_movie_as_production_exec(self):
        new_movie = {"title": "New Movie", "release_date": "2025-01-01"}
        res = self.client().post('/movies', headers=self.get_headers(self.production_exec_token), json=new_movie)
        self.assertEqual(res.status_code, 201)

    def test_add_actor_as_director(self):
        new_actor = {"name": "New Actor", "age": 30, "gender": "male"}
        res = self.client().post('/actors', headers=self.get_headers(self.director_token), json=new_actor)
        self.assertEqual(res.status_code, 201)

    def test_add_actor_as_actor(self):
        new_actor = {"name": "New Actor", "age": 30, "gender": "male"}
        res = self.client().post('/actors', headers=self.get_headers(self.assistant_token), json=new_actor)
        self.assertEqual(res.status_code, 403)

    def test_delete_movie_as_director(self):
        res = self.client().delete('/movies/1', headers=self.get_headers(self.director_token))
        self.assertEqual(res.status_code, 403)

    def test_delete_actor_as_director(self):
        # First, add an actor to ensure it exists
        new_actor = {"name": "Test Actor", "age": 35, "gender": "male"}
        add_res = self.client().post('/actors', headers=self.get_headers(self.director_token), json=new_actor)
        actor_id = add_res.json.get("actor", {}).get("id")  # Get the created actor ID

        # Now, attempt to delete the actor
        res = self.client().delete(f'/actors/{actor_id}', headers=self.get_headers(self.director_token))
        print(res)
        self.assertEqual(res.status_code, 200)  # Ensure successful deletion

    def test_delete_actor_as_actor(self):
        res = self.client().delete('/actors/1', headers=self.get_headers(self.assistant_token))
        self.assertEqual(res.status_code, 403)

    def test_unauthorized_access(self):
        res = self.client().get('/movies', headers=self.get_headers(self.invalid_token))
        self.assertEqual(res.status_code, 401)

if __name__ == "__main__":
    unittest.main()

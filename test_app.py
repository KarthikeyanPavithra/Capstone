import unittest
import json
from app import create_app

# Sample tokens for different roles (Replace with actual tokens)
CASTING_ASSISTANT_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVpNk11SmdGUE1qNTVrYUR1X0MxSSJ9.eyJpc3MiOiJodHRwczovL3Bhdmlkc25kLmpwLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2FiOGVjYzI0ZTA2NDI2ZTU5NTkzZGUiLCJhdWQiOiJtZWRpYSIsImlhdCI6MTczOTI5NjU0NiwiZXhwIjoxNzM5MzAzNzQ2LCJzY29wZSI6IiIsImF6cCI6IkxWM1gxVmJvT2JFZno2bVIxRXhJWTJQYkhneExnbEltIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.QbXr8z_lHA-qemrQi0_-vPoX7tEPeaZnlIIwdZBxFGCyfV4K-DVEhlJ7M4_aNPh-KnuJlALXEpGSyw3hZBzgAz3xuAyxyo1-G5ZeaNuiE87-dJgYfxzVt4VQPNAEZZ7OAEsPIALbya_Y97kLZq_wmWMShNZOW2j6ZGBUQ0_OXi8yN5BTNHFh2hikGwqHqqujEVWlzdSMBx01eVS3lfDqSKx5MKMpk3f5p7Q2rHprLZmrsMRcfnw5n6u4fXL-fX4TgZQk8F3MvcdwN7sCvd7VlE_X9uD8k5-Pjwz3asMgojfDmkxDGN6KUX8B2JDYDAzQVXDNcVYrQ611xH492pKzag"
CASTING_DIRECTOR_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVpNk11SmdGUE1qNTVrYUR1X0MxSSJ9.eyJpc3MiOiJodHRwczovL3Bhdmlkc25kLmpwLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzliMjJiZmY1NzY4ZDY4N2NiOWM0MjYiLCJhdWQiOiJtZWRpYSIsImlhdCI6MTczOTI5NjM1NiwiZXhwIjoxNzM5MzAzNTU2LCJzY29wZSI6IiIsImF6cCI6IkxWM1gxVmJvT2JFZno2bVIxRXhJWTJQYkhneExnbEltIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.Rk_FhLVpZD6Sie8FR2ge2v85v4czfrKfSdUaohFd7YLwsMRWz2ogS0VmUvYpnK-uQ-zwpjGy6JZb6wI0kAsDXx1IjT2eVNvAGydNYDz5q5S9POYInB4CIuTPuMsWUkTsdVav-oMnpkZ82UXLvZdrlTO4fFLkJwH8ifuMUDHni2AjZBLcCwksTNbvar6EL3Cx781WIFz3FRq2teKILMoQBEJ8c6k6gpI_Zw2rmGNBknCePSNjWm6pO2yw1Z1KyFB7jbzDSGEDMsVkeRTufziTMBQFvohJyZIC03ZjL1794zPM3D6U4XyNVtwgHQ1lo-_B5T9Q5aisl7GCPO_C-CBkqA"
EXECUTIVE_PRODUCER_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVpNk11SmdGUE1qNTVrYUR1X0MxSSJ9.eyJpc3MiOiJodHRwczovL3Bhdmlkc25kLmpwLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2Nzk0OTEwZDZmZTZkNTIzZDMwNjgwYjYiLCJhdWQiOiJtZWRpYSIsImlhdCI6MTczOTI5NjA1NiwiZXhwIjoxNzM5MzAzMjU2LCJzY29wZSI6IiIsImF6cCI6IkxWM1gxVmJvT2JFZno2bVIxRXhJWTJQYkhneExnbEltIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.iqh0yYA7hYS563FpQyWwPij7SmNMTciQtlLOlRKDn_t16Lwg8uED9syaYJ8Z0Is0Jb3NyRza-Jqe9PLJH7xJ5jvMLiexmlB2lMLEHuKLqxngNC-9C2gToss1Yg-eracP3gP3PtGO0RsQUuPl2mxNTpDWpFhYIkGJef4DceBKsibMNUIxChIh5J97F0dTsOczIpBsd7ZBM4xvpzh8jcBdwMmsS7Ab-bPL1mWwyz3MrtyYht8EP5Ek1eMjevctL8mbbQaQtEC_DlCR8fnJDN8wrYcsKh-QCzBMgaS_Ob2aS4N_ULbm2YGoLuo5upsxCxSrSvXzWZ0cfW37DNw78u6aqQ"
INVALID_TOKEN = "Bearer invalid_token"

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.headers_assistant = {"Authorization": CASTING_ASSISTANT_TOKEN}
        self.headers_director = {"Authorization": CASTING_DIRECTOR_TOKEN}
        self.headers_producer = {"Authorization": EXECUTIVE_PRODUCER_TOKEN}
        self.headers_invalid = {"Authorization": INVALID_TOKEN}

    def test_get_actors_success(self):
        res = self.app.get("/actors", headers=self.headers_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("actors", data)

    def test_get_actors_unauthorized(self):
        res = self.app.get("/actors", headers=self.headers_invalid)
        self.assertEqual(res.status_code, 401)

    def test_add_actor_success(self):
        new_actor = {"name": "John Doe", "age": 30, "gender": "male"}
        res = self.app.post("/actors", json=new_actor, headers=self.headers_director)
        self.assertEqual(res.status_code, 201)

    def test_add_actor_forbidden(self):
        new_actor = {"name": "Jane Doe", "age": 25, "gender": "female"}
        res = self.app.post("/actors", json=new_actor, headers=self.headers_assistant)
        self.assertEqual(res.status_code, 403)

    def test_delete_actor_success(self):
        res = self.app.delete("/actors/1", headers=self.headers_producer)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_forbidden(self):
        res = self.app.delete("/actors/1", headers=self.headers_assistant)
        self.assertEqual(res.status_code, 403)

    def test_get_movies_success(self):
        res = self.app.get("/movies", headers=self.headers_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("movies", data)

    def test_add_movie_success(self):
        new_movie = {"title": "New Movie", "release_date": "2025-01-01"}
        res = self.app.post("/movies", json=new_movie, headers=self.headers_producer)
        self.assertEqual(res.status_code, 201)

    def test_add_movie_forbidden(self):
        new_movie = {"title": "Restricted Movie", "release_date": "2025-01-01"}
        res = self.app.post("/movies", json=new_movie, headers=self.headers_assistant)
        self.assertEqual(res.status_code, 403)

    def test_delete_movie_success(self):
        res = self.app.delete("/movies/1", headers=self.headers_producer)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_forbidden(self):
        res = self.app.delete("/movies/1", headers=self.headers_assistant)
        self.assertEqual(res.status_code, 403)

if __name__ == "__main__":
    unittest.main()


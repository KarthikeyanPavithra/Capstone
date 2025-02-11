**CAPSTONE PROJECT - RENDER HOSTED**

**Casting Agency Management System**

The Casting Agency Management System is a web application designed to manage actors, movies, and their relationships efficiently. It provides endpoints for adding, updating, and deleting actors and movies, as well as retrieving information about them. The system is built using Flask, a popular Python web framework, and uses SQLAlchemy for database interactions.

### **Features:**

#### **Actor Management**
- **List Actors:** Retrieve a list of all actors with their details including name, age, and gender.
- **Add Actor:** Add a new actor to the database by providing the name, age, and gender.
- **Update Actor:** Update details of an existing actor, such as name, age, and gender.
- **Delete Actor:** Remove an actor from the database by specifying their ID.

#### **Movie Management**
- **List Movies:** Retrieve a list of all movies, including title, release date, and actors associated with them.
- **Add Movie:** Add a new movie by specifying the title, release date, and actor IDs.
- **Update Movie:** Update details of an existing movie, such as title, release date, and associated actors.
- **Delete Movie:** Remove a movie from the database by specifying its ID.

### **To Test the Project Locally:**

1. Fork this project - `<Your GitHub Repository Link>`
2. Setup this project by running this command:
   ```bash
   pip install -r requirements.txt
   ```
3. Create database tables:
   ```bash
   python create-db-tables.py
   ```
4. Run the app:
   ```bash
   flask run --reload
   ```
5. Test the application after generating a valid token with required permissions from Auth0 and run:
   ```bash
   pytest test-app.py
   ```

### **Roles and Permissions:**

There are two roles associated with this project:

1. **Casting Director**
   - `get:actors`
   - `get:movies`
   - `post:actors`
   - `patch:actors`
   - `patch:movies`
   - `delete:actors`
   
2. **Casting Assistant**
   - `get:actors`
   - `get:movies`

3. **Executive Producer**
   - `get:actors`
   - `get:movies`
   - `post:actors`
   - `post:movies`
   - `patch:actors`
   - `patch:movies`
   - `delete:actors`
   - `delete:movies`

The Executive Producer has full access to manage actors and movies, while the Casting Assistant can only view them and Casting Director  can manage actors and movies, but cannot delete/add movies.

### **Render Deployment Details:**

This application is hosted on Render at:
**[https://your-casting-agency.onrender.com/](https://your-casting-agency.onrender.com/)**

### **API Endpoints:**

#### **Actor Endpoints:**
- `GET /actors`: Lists all actors.
- `POST /add-actor`: Adds a new actor.
- `PATCH /actors/<int:actor_id>`: Updates details of an existing actor.
- `DELETE /actors/<int:actor_id>`: Deletes a specific actor.

#### **Movie Endpoints:**
- `GET /movies`: Lists all movies.
- `POST /add-movie`: Adds a new movie.
- `PATCH /movies/<int:movie_id>`: Updates details of an existing movie.
- `DELETE /movies/<int:movie_id>`: Deletes a specific movie.

### **Example Requests and Responses:**

#### **GET /actors**
**Description:** Fetches the list of all actors.

**Response:**
```json
[
    {
        "id": 1,
        "name": "Leonardo DiCaprio",
        "age": 48,
        "gender": "Male"
    },
    {
        "id": 2,
        "name": "Scarlett Johansson",
        "age": 39,
        "gender": "Female"
    }
]
```

#### **GET /movies**
**Description:** Fetches the list of all movies.

**Response:**
```json
[
    {
        "id": 1,
        "title": "Inception",
        "release_date": "2010-07-16",
        "actors": [1]
    },
    {
        "id": 2,
        "title": "Black Widow",
        "release_date": "2021-07-09",
        "actors": [2]
    }
]
```

#### **POST /add-actor**
**Request:**
```json
{
    "name": "Tom Cruise",
    "age": 61,
    "gender": "Male"
}
```

**Success Response:**
```json
{
    "success": true,
    "created": 3
}
```

#### **POST /add-movie**
**Request:**
```json
{
    "title": "Mission Impossible",
    "release_date": "1996-05-22",
    "actors": [3]
}
```

**Success Response:**
```json
{
    "success": true,
    "created": 4
}
```

#### **PATCH /actors/<int:actor_id>**
**Request:**
```json
{
    "name": "Tom Cruise Updated"
}
```

**Error Response if Actor ID is Not Found:**
```json
{
    "success": false,
    "error": "Actor not found"
}
```

#### **DELETE /movies/<int:movie_id>**
**Response:**
```json
{
    "success": true,
    "message": "Movie deleted successfully"
}
```

**Error Response if Movie ID is Not Found:**
```json
{
    "success": false,
    "error": "Movie not found"
}
```

---

### **About**
No description, website, or topics provided.

### **Resources**
- **Readme**
- **Activity**

### **Statistics**
- **Stars:** 0 stars
- **Watchers:** 1 watching
- **Forks:** 0 forks

### **Report Repository**

### **Releases**
- No releases published

### **Packages**
- No packages published

### **Languages**
- Python 100%

---
**Footer**


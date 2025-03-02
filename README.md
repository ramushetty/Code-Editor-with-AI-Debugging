# Code Editor with AI Debugging

This project is a collaborative code editor with AI debugging capabilities. It's built using a FastAPI backend, a React frontend, and utilizes WebSockets for real-time code synchronization.

**Important Note:** This project is currently under active development and is not yet production-ready. Specifically, the frontend-backend WebSocket connection is still being refined.

## Prerequisites

* Docker and Docker Compose installed on your system.
* Node.js and npm (or yarn) installed (for frontend development).

## Getting Started

1.  **Clone the Repository:**

    ```bash
    git clone git@github.com:ramushetty/Code-Editor-with-AI-Debugging.git
    cd Code-Editor-with-AI-Debugging
    ```

2.  **Build and Run with Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images for the backend, frontend, database (PostgreSQL), and Redis, and then start the containers.

3.  **Access the Application:**

    * The React frontend will be accessible at `http://localhost:5173`.
    * The FastAPI backend will be accessible at `http://localhost:8000`.
    * Postgresql is running on `http://localhost:5432`
    * Redis is running on `http://localhost:6379`

## Development

### Backend (FastAPI)

* The backend code is located in the `backend/` directory.
* Changes to the backend code will be automatically reflected due to the volume mount and `--reload` flag in the `docker-compose.yml` file.
* Backend API documentation is available at `http://localhost:8000/docs` (Swagger UI).

### Frontend (React)

* The frontend code is located in the `frontend/` directory.
* Changes to the frontend code will be automatically reflected due to the volume mount in the `docker-compose.yml` file.
* To install additional npm packages:

    1.  Open a new terminal.
    2.  Navigate to the `frontend/` directory.
    3.  Run `npm install <package-name>`.
    4.  Rebuild the frontend docker container with `docker-compose up --build frontend`

### Database (PostgreSQL)

* The PostgreSQL database is configured in the `docker-compose.yml` file.
* Database data is persisted in the `db-data` volume.
* You can connect to the database using a PostgreSQL client at `localhost:5432`.

### Redis

* The Redis database is configured in the `docker-compose.yml` file.
* You can connect to the database using a Redis client at `localhost:6379`.
### database layout 

+-----------------+       +-----------------+       +-----------------+
|     users       |       |   code_files    |       |   code_history  |
+-----------------+       +-----------------+       +-----------------+
| id (PK)         |<------| user_id (FK)    |<------| code_file_id (FK)|
| username        |       | id (PK)         |       | id (PK)         |
| email           |       | filename        |       | content         |
| hashed_password |       | file_path       |       | updated_at      |
+-----------------+       +-----------------+       +-----------------+
        |                         |
        |                         |
        v                         v
+-----------------+       +-----------------+
|   room_users    |       |     rooms       |
+-----------------+       +-----------------+
| room_id (FK)    |<------| id (PK)         |
| user_id (FK)    |       | room_number     |
+-----------------+       +-----------------+
## Future Improvements

* Implement robust user authentication and authorization for WebSockets.
* Improve the user interface and user experience.
* Add more robust error handling.
* Write unit tests.
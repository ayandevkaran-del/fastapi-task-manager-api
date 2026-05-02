# fastapi-task-manager-api
# Task Management API with Auth

Hello! This is my submission for the Backend Developer Intern role. I built a secure, scalable REST API using FastAPI, complete with JWT authentication and a task management system.

##  Features
*   **Secure Auth:** Password hashing with Bcrypt and token-based authentication (JWT).
*   **Role-Based Access:** Standard user access with Admin-level permissions for data management.
*   **Live Docs:** Automated interactive API documentation via Swagger UI.
*   **Frontend Integration:** A clean, vanilla JavaScript dashboard to interact with the API in real-time.

##  Tech Stack
*   **Backend:** FastAPI (Python)
*   **Database:** SQLAlchemy with SQLite (easily swappable for Postgres)
*   **Security:** Python-Jose (JWT) and Passlib
*   **Frontend:** HTML5, Tailwind CSS, and Vanilla JS

##  Scalability Note
To prepare this system for a high-traffic production environment, I would implement the following:
1. **Database:** Migrate from SQLite to **PostgreSQL** to handle concurrent writes and scaling.
2. **Caching:** Integrate **Redis** to store JWT blacklists and cache frequent GET requests, reducing database latency.
3. **Deployment:** Containerize the application using **Docker** for consistent deployment across different environments.
4. **Load Balancing:** Use Nginx as a reverse proxy to distribute traffic across multiple API instances.

##  How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Start the server: `uvicorn main:app --reload`
3. View API Docs: `http://127.0.0.1:8000/docs`
4. Open `index.html` in your browser to use the UI.

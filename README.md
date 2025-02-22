
  
# Sports Tracker App
![alt text](https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/sportstracker-benny/blob/main/images/logo.png "Logo Title Text 1")
A microservices-based sports tracking application built with FastAPI, SQLAlchemy, and Streamlit. This app allows you to manage teams, leagues, matches, and view live scores and analytics—all within an intuitive web interface.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Development](#development)

## Features

- **User Management & Authentication:**  
  - Register, login, and logout functionality.
  
- **Management Service:**  
  - Create, update, and delete leagues, teams, and matches.
  - Manage relationships between leagues, teams, and matches.
  
- **Scoreboard Service:**  
  - Update match scores in real time.
  - View live scores for ongoing matches.
  
- **Analytics Service:**  
  - View league standings and other sports analytics.
  
- **User Interface:**  
  - A simple and intuitive GUI built with Streamlit.
  - Responsive navigation between Management, Scoreboard, and Analytics pages.

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, Uvicorn  
- **Frontend:** Streamlit  
- **Authentication:** JWT, PassLib (bcrypt)  
- **Database:** PostgreSQL  
- **Containerization:** Docker, Docker Compose  

## Architecture

This application is divided into four microservices plus a GUI:

- **Management Service:** Handles data management for teams, leagues, matches, and user authentication.
- **Scoreboard Service:** Responsible for updating and displaying live scores.
- **Analytics Service:** Aggregates and displays analytics data such as league standings.
- **Testing Service:** End to end test of the application.
- **GUI:** A lightweight front-end built with Streamlit that interacts with the microservices via REST APIs.
- **Database:** PostgreSQL is used as the central database, with each service connecting to it.

All services run in Docker containers, coordinated by Docker Compose.
![alt text](https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/sportstracker-benny/blob/main/images/mermaid-diagram-2025-02-22-154132.png "Logo Title Text 1")

```
📦 
├─ README.md
├─ analytics_service
│  ├─ Dockerfile
│  ├─ config.py
│  ├─ database.py
│  ├─ main.py
│  ├─ models.py
│  ├─ requirements.txt
│  ├─ routers
│  │  └─ analytics.py
│  ├─ schemas.py
│  └─ tests
│     └─ test_analytics.py
├─ docker-compose
├─ docker-compose.yml
├─ gui
│  ├─ Dockerfile
│  ├─ app.py
│  └─ requirements.txt
├─ integration_tests
│  ├─ Dockerfile
│  ├─ conftest.py
│  ├─ requirements.txt
│  └─ test_system_e2e.py
├─ management_service
│  ├─ Dockerfile
│  ├─ __pycache__
│  │  ├─ auth_utils.cpython-310.pyc
│  │  ├─ config.cpython-310.pyc
│  │  ├─ database.cpython-310.pyc
│  │  ├─ main.cpython-310.pyc
│  │  ├─ models.cpython-310.pyc
│  │  └─ schemas.cpython-310.pyc
│  ├─ alembic.ini
│  ├─ alembic
│  │  ├─ README
│  │  ├─ __pycache__
│  │  │  └─ env.cpython-310.pyc
│  │  ├─ env.py
│  │  ├─ script.py.mako
│  │  └─ versions
│  │     ├─ 418ead1afa78_initial_migration_create_all_tables.py
│  │     ├─ __pycache__
│  │     │  ├─ 418ead1afa78_initial_migration_create_all_tables.cpython-310.pyc
│  │     │  └─ ebecd5ba6a20_add_users_table.cpython-310.pyc
│  │     └─ ebecd5ba6a20_add_users_table.py
│  ├─ auth_utils.py
│  ├─ config.py
│  ├─ database.py
│  ├─ dependencies.py
│  ├─ main.py
│  ├─ models.py
│  ├─ requirements.txt
│  ├─ routers
│  │  ├─ __pycache__
│  │  │  ├─ auth.cpython-310.pyc
│  │  │  ├─ leagues.cpython-310.pyc
│  │  │  ├─ matches.cpython-310.pyc
│  │  │  └─ teams.cpython-310.pyc
│  │  ├─ auth.py
│  │  ├─ leagues.py
│  │  ├─ matches.py
│  │  └─ teams.py
│  ├─ schemas.py
│  └─ tests
│     ├─ test_end_to_end.py
│     └─ test_users.py
└─ scoreboard_service
   ├─ Dockerfile
   ├─ config.py
   ├─ database.py
   ├─ main.py
   ├─ models.py
   ├─ requirements.txt
   ├─ routers
   │  └─ scores.py
   ├─ schemas.py
   └─ tests
      └─ test_score.py
```
## Setup & Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.
- (Optional) Python 3.10+ for local development.

### Running the Application

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/sportstracker-benny
   cd sportstracker-benny
  
2. Build and Run Containers:
From the root directory of the repository (where the `docker-compose.yml` file is located):
`docker-compose up --build` 

	This command builds all the Docker images and starts the containers for management_service, scoreboard_service, analytics_service, integration tests, the GUI, and the PostgreSQL database.
**Access the Application:**

-   **GUI:** Open your browser and navigate to http://localhost:8501
-   **Management API:** [http://localhost:8000](http://localhost:8000)
-   **Scoreboard API:** [http://localhost:8001](http://localhost:8001)
-   **Analytics API:** [http://localhost:8002](http://localhost:8002)

## Usage

1.  **User Registration & Login:**
    
    -   Use the login/register options in the sidebar of the GUI.
    -   After logging in, navigate to the Management page to create or delete leagues, teams, and matches.
2.  **Live Score Updates:**
    
    -   Navigate to the Scoreboard page to update match scores and view live score data.
3.  **Analytics:**
    
    -   The Analytics page displays league standings and other aggregated statistics.

## Development

### Running Locally (Without Docker)

If you prefer to run the application locally without Docker, install the dependencies:

`pip install -r management_service/requirements.txt`
`pip install -r scoreboard_service/requirements.txt`
`pip install -r analytics_service/requirements.txt`
`pip install -r integration_tests/requirements.txt`
`pip install -r gui/requirements.txt` 

Then, run each service using Uvicorn or Streamlit accordingly.

##  Author
-   **Name:**  Benjamin Golber
-   **Email:**  [benigolber25@gmail.com](mailto:ofircohen599@gmail.com)
-   **GitHub:**  [krispybit](https://github.com/krispybit1)

## License

[MIT]() 
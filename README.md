
# Sports Tracker App

A microservices-based sports tracking application built with FastAPI, SQLAlchemy, and Streamlit. This app allows you to manage teams, leagues, matches, and view live scores and analytics—all within an intuitive web interface.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

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

## Architecture

This application is divided into three microservices plus a GUI:

- **Management Service:** Handles data management for teams, leagues, matches, and user authentication.
- **Scoreboard Service:** Responsible for updating and displaying live scores.
- **Analytics Service:** Aggregates and displays analytics data such as league standings.
- **GUI:** A lightweight front-end built with Streamlit that interacts with the microservices via REST APIs.
- **Database:** PostgreSQL is used as the central database, with each service connecting to it.

All services run in Docker containers, coordinated by Docker Compose.

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, Uvicorn  
- **Frontend:** Streamlit  
- **Authentication:** JWT, PassLib (bcrypt)  
- **Database:** PostgreSQL  
- **Containerization:** Docker, Docker Compose  
- **Other Tools:** Alembic for database migrations

## Setup & Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.
- (Optional) Python 3.10+ for local development.

### Running the Application

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/sportstracker-benny
   cd sportstracker-benny

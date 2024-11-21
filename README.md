
# Train Station API

Train Station API is a service designed for booking tickets for international train journeys. 
It provides an efficient and user-friendly platform to search for available routes, manage reservations, 
and access journey details. The API supports user authentication, ticket management, 
and advanced filtering options for routes and destinations.

## Installation

install PostgresSQL and create db

```bash
  git clone https://github.com/struhanets/train-station-project.git
  cd train-station-project
  python -m venv venv
  source venv/bin/activate
  pip install requirements.txt
  SET DB_HOST=<your db host>
  SET DB_NAME=<your db name>
  SET DB_USER=<your db username>
  SET DB_PASSWORD=<your db password>
  SET SECRET_KEY=<your secret key>
  python manage.py migrate
  python manage.py runserver
```

    
## Features

- User Authentication: Secure token-based login system.

- Ticket Booking: Create, view, update, and delete train ticket reservations.

- Route Management: Search for train routes with filtering by source and destination.

- Journey Details: Access comprehensive journey schedules and information.

- Swagger Documentation: Full API documentation with interactive endpoints.

- Request Throttling: Rate limiting to ensure fair usage and API stability.


## Technologies Used

**Backend:** Django REST Framework (DRF), Python 3.13

**Authentication:** Token-based authentication (DRF Tokens)

**Documentation:** Swagger (via drf-spectacular)

**Database:** PostgresSQL (or any preferred relational database)

**Containerization:** Docker

## Run with Docker

# Docker should be installed

```bash
docker-compose build
docker-compose up
```

## Getting access
create user via api/user/register
get access token via api/user/login

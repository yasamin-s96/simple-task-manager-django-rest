# Todolist API

## Table of Contents

- [Todolist API](#todolist-api)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running The Application](#running-the-application)
  - [Environment Variables](#environment-variables)
  - [API Documentation](#api-documentation)
  - [Contribution](#contribution)
  - [License](#license)
  - [Contact](#contact)


## Description

A restful API for easy and seamless task management.

## Features

- Task categorization by custom projects and tags
- Recurring tasks
- Task and project completion history
- Weekly reports

## Technologies Used

- Django
- Django REST Framework
- Docker
- PostgreSQL 
- Redis 
- Celery
- Celery Beat
  
## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yasamin-s96/simple-task-manager-django-rest.git
   cd simple-task-manager-django-rest
   ```
2. Copy .env.example to .env and update the environment variables:
```sh
cp .env.example .env
```
### Running The Application

1. Build and start the Docker containers:
```sh
docker-compose up --build
```
2. The application should now be running at http://localhost:8001.
  

## Environment Variables
Ensure you set the following environment variables in your .env file:

`DJANGO_SECRET_KEY`

`DJANGO_DEBUG`

`POSTGRES_DB`

`POSTGRES_USER`

`POSTGRES_PASSWORD`

`POSTGRES_HOST`

`POSTGRES_PORT`

## API Documentation
The API documentation is available at http://localhost:8001/swagger/.

## Contribution
Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (git checkout -b feature/your-feature)
3. Commit your changes (git commit -m 'Add some feature')
4. Push to the branch (git push origin feature/your-feature)
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any inquiries or questions, please contact:

- Email:  yasamin.s96@gmail.com
- GitHub: [yasamin-s96](https://github.com/yasamin-s96)
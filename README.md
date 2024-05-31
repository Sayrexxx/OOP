# Reshetnev Arseny 253504
# Server application for air travel management 'ЖМЫХ Airlines'
### PROJECT DESCRIPTION
### 1 General information
### 1.1 Purpose of the program 
The purpose of the program is to create an efficient air travel management system that will allow airlines and passengers to interact to book, manage and track air travel. Such a system will help to optimize processes and improve service quality.

### 2 Project Objectives 
### 2.1 Main project objectives
- Realizaof automated control over air travel
- Provide an interface for different roles (administrator, passenger)
- Provide security of data transfer from user to system and vice versa.

### 3 Project Description
### 3.1 Technology Stack
The following software tools will be used to implement the project: Python, SQL, Docker
### 3.2 Functions:
- User registration and authentication.
- Search and book available airline tickets.
- Manage flight, schedule and seat availability information.
- Tracking flight status and notifying passengers of changes.
- Generating reports and statistics on air travel.

### Project launch:
Use the following instructions to launch the application (all steps must be performed in the working directory of the application):

Build a multi-container app (this command create and start containers):  
`docker-compose up --build`  

Run application :  
`docker-compose start` or you can just start multi-container app in Docker Desktop  
  
If you want to create superuser, you can exec 'python manage.py createsuperuser' in your 'django' container shell
  
to see application:

### localhost:8000 (or you can just click working port for 'django' container in 'djangoproject' multi-container

  
  ![uml-1](https://github.com/Sayrexxx/OOP/assets/114809675/a379c8fe-1beb-44be-91a5-8f5127c4f03e)

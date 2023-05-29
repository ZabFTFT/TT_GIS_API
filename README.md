# TT_GIS_API
**GIS API** is a RESTful API that allows you to store and retrieve places with their corresponding coordinates in a GIS database.
It provides endpoints for creating, updating, deleting, and retrieving places.

### Installation
#### To install GIS API using GitHub, follow these steps:

- Install and create PostgreSQL with GIS extension.
- Clone the repository by running the following command:<br>
  ```bash
  git clone https://github.com/ZabFTFT/TT_GIS_API.git
  ```
- Change to the cloned repository directory by running:<br>
    ```bash
  cd TT_GIS_API
  ```
- Create a new virtual environment by running:<br>
    ```bash
   python -m venv venv
   ```
- Activate the virtual environment by running:<br>
    ```bash
   Windows: venv\Scripts\activate
  
   Linux/MacOs: source venv/bin/activate
  ```
- Install the required packages by running:<br>
    ```bash
   pip install -r requirements.txt
   ```
- Set the required environment variables in .env file(use .env.sample) **OR**
- Set the required environment variables by running the following commands:<br>
   ```bash
  For Windows: use <set> <env_variable>
  
   set DB_HOST=YOUR_DB_HOSTNAME
   set DB_NAME=YOUR_DB_NAME
   set DB_USER=YOUR_DB_USER
   set DB_PASSWORD=YOUR_DB_PASSWORD
   set DB_SECRET_KEY=YOUR_SECRET_KEY
   set DJANGO_SECRET_KEY=DJANGO_SECRET_KEY
   set DEBUG=DEBUG
  ```
     ```bash
  For Linux/MacOS: use <export> <env_variable>
  
   export DB_HOST=YOUR_DB_HOSTNAME
   export DB_NAME=YOUR_DB_NAME
   export DB_USER=YOUR_DB_USER
   export DB_PASSWORD=YOUR_DB_PASSWORD
   export DB_SECRET_KEY=YOUR_SECRET_KEY
   export DJANGO_SECRET_KEY=DJANGO_SECRET_KEY
   export DEBUG=DEBUG
  ```
- Apply the database migrations by running:<br>
    ```bash
   python manage.py migrate
   ```
- Start the development server by running:<br>
    ```bash
   python manage.py runserver
   ```

#### Alternatively, you can run GIS API using Docker:
- Install Docker.
- Clone the repository and change to the cloned repository directory.
- Build the Docker image by running:<br>
    ```bash
    docker-compose up --build
    ```

### Demo
![doc_1.png](demo/Screenshot%20from%202023-05-29%2013-22-29.png)
![doc_2.png](demo/Screenshot%20from%202023-05-29%2013-22-49.png)
![doc_3.png](demo/Screenshot%20from%202023-05-29%2013-23-21.png)
# Carpool app API server
This django project is a project for the course M7011E at LTU (Sweden).

## Set up
1. Create a virtual environment:
   ```
   python3 -m venv .env
   ```
2. Activate the virtual environment:
   1. For linux
    ```
    source .env/bin/activate
    ```
    2. For Windows
    ```
    .env/Scripts/Activate.bat
    ```
3. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
4. Migrate:
   ```
   python manage.py migrate
   ```

## Run project
   ```
   python manage.py runserver
   ```

You can find the documentation at You can find the documentation at [localhost:8000/api/v1/schema/swagger-ui](localhost:8000/api/v1/schema/swagger-ui)

## Good to know
There is a second part to this project which can be found [here](https://github.com/AceBasket/carpool-reviews). This is because the project is split into 2 microservices, the microservice deals with the reviews which can be assigned by a user to a trip and another user.
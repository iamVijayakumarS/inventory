Inventory Management System

Overview :

The Inventory Management System is a Django-based web application designed to manage inventory items. This application allows users to register, log in, create items, and manage those items (retrieve, update, delete) securely using token-based authentication.

Features :

   * User registration and authentication.
   * Create, read, update, and delete inventory items.
   * Cache implementation for faster retrieval of item details.
   * Token-based authentication using JWT (JSON Web Tokens).

Technologies Used :
   * Django: Web framework for building the application.
   * Django REST Framework: Toolkit for building Web APIs.
   * Django REST Framework Simple JWT: Library for JSON Web Token authentication.
   * MYSQL : Relational database for storing user and item data.
   * Redis: In-memory data structure store used for caching.

Installation :
   * Prerequisites
   * Python 3.x
   * pip
   * Mysql server or xampp
   * Redis server

Steps to Set Up :

git clone [<repository-url>](https://github.com/iamVijayakumarS/inventory)


STEP 2 : 
pip install -r requirements.txt


STEP 3 : 
python manage.py migrate

STEP 4 :
python manage.py runserver



API ENDPOINTS : 

BASEPATH = http://127.0.0.1:8000/

EG :  http://127.0.0.1:8000{Endpoint}


User Registration
Endpoint: /register/
Method: POST
Request Body: {
    "username": "example_username",
    "password": "example_password"
}


User Login
Endpoint: /login/
Method: POST
Request Body:
{
    "username": "example_username",
    "password": "example_password"
}

Item Management :

Token Authentication
   For endpoints that require authentication (like item creation, updating, deleting, or retrieving), include the JWT token in the Authorization header

Header:
   Authorization: Bearer <access_token>  - get the access token from the succesfull loggedin response

Create Item :
   Endpoint: /items/
   Method: POST
   Header: Authorization: Bearer <access_token>
   Request Body : {
      "name": "Item Name",
      "description": "Item Description"
   }

Get Item :
   Header: Authorization: Bearer <access_token>
   Endpoint: /items/1/
   Method: GET

Update Item :
   Header: Authorization: Bearer <access_token>
   Endpoint: /items/1/
   Method: PUT
      Request Body : {
      "name": "Item Name - Updated",
      "description": "Item Description - Updated"
   }

Delete Item :
   Header: Authorization: Bearer <access_token>
   Endpoint: /items/1/
   Method: DELETE


Caching :
   The application uses Redis for caching item data to improve performance. Cached items are stored for 15 minutes.

Testing :
   To run the test suite, use the following command:
   python manage.py test.

Logging :
   The application logs important actions, such as user registration attempts and authentication, using Python's built-in logging module.


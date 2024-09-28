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

git clone <repository-url>
cd <repository-directory>


STEP 2 : 
pip install -r requirements.txt


STEP 3 : 
python manage.py migrate

STEP 4 :
python manage.py runserver



API ENDPOINTS : 

BASEPATH = http://127.0.0.1:8000/

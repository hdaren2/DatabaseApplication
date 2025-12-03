Grocery Store Database Application
- This project implements a grocery store database management system using SQLite and a Python-based command-line interface.
- Requirements:
  - Python 3.8+
    
  Project Files:
  - grocery.db - SQLite database with full tables & test data
  - db_app.py	- main Python application
  - init_db.py - deletes existing grocery.db and recreates it using grocery_schema.sql + sample_data.sql
  - grocery_schema.sql - table creation SQL
  - sample_data.sql	- dataset inserts SQL
  
  Application Interface Menu
  ==== Grocery Store Application ====
  1. Member login
  2. Manager login
  3. Inventory management
  4. Exit
  
  Member Interface:
    Members authenticate using:
    - Email
    - Password
    Members can:
    - View profile
    - View points balance
    - View purchase history
    - Update email
    - Update password
    - Delete their profile
  
  Manager Interface:
  - Managers log in using Manager ID.
  - Managers can:
   - View list of associates
   - Add an associate
   - Update associate info
   - Delete an associate
  
  Inventory Management Interface:
    Inventory actions:
    - List all products
    - Add a new product
    - Update price or quantity
    - Delete product
  
  Running the App:
    Steps:
    1. Initialize the database
      - python3 init_db.py
    2. Run the app
      - python3 db_app.py

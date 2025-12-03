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
  - test_queries.sql - SQL queries used to verify database functionality
  
  Application Interface Menu:
  
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
  
  Running the App and Test Queries:
    Steps:
    1. Getting the files
      - Extract zip file onto your enviornment (we used VS Code + added python debugger extension)
      OR 
      - Navigate to the extracted folder in your console/command prompt.

    2. Execute the following command in the console to run the database file 
      - python3 init_db.py

    3. Execute the following command in the console to run the app file
      - python3 db_app.py

    4. Testing through App interface 
    Sample access inputs to test with:
      * Select member login | email address input: <mason.reed@outlook.com> | psw input: <aL55ntQ>
      * Select Manager login | Manger id input: <78986> 
      * Select Inventory Managment | Select Delete product | ID input <221> 
    ** For more individual object referencing look at "sample_data.sql" file **

    5. Execute the following command in the console to run the automated database test scripts
      - <sqlite3 grocery.db < test_queries.sql>
    ** this will display the outputted results of the premade test queries **
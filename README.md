# esp-machine-test

Machine Test

## Prerequisites

* python >= 3.8
* pip3

1. Clone the repository on you local machine with the command:
    ```
    git clone https://github.com/Virendra1485/esp-machine-test.git
    ```
2. Now move to repo with command:
    ```
    cd esp-machine-test
    ```
3. Create a virtual environment. If you don't have virtualenv installed, you can download it with the command:
    ```
    pip install virtualenv
    
    ```
4. Create a virtual environment with the following command:
    ```
    virtualenv <virtual environment name>
    ```

5. Activate the virtual environment using the command:

    ```
    source <virtual environment name>/bin/activate
    ```
6. Install the app dependencies by running:
    ```
    pip install -r requirements.txt
    ```
7. Create a .env file in the backend directory using the command line:
    ```
    touch .env
    ```
8. Open the .env file and update it with the Postgres database credentials as follows:
    ```
    POSTGRES_DB=<postgres database name>
    POSTGRES_USER=<postgres user name>
    POSTGRES_PASSWORD=<postgres password>
    POSTGRES_HOST=<host name for postgres>
    POSTGRES_PORT=<postgres port>
    ```
9. For apply migrations run following command:
   ```
   python manage.py migrate
   ```
10. You can now run the backend server by executing the following command:
    ```
    python manage.py runserver
    ```
11. Now you can visit the API endpoints are:
    ```
    http://127.0.0.1:8000/api/user/registration/     
    method: POST
    request payload: 
    {
    "name": "Virendra Singh Rawat",
    "email": "virendrasinghrawat1485@gmail.com",
    "password": "Test@123",
    "phone": "7415144601",
    "address": "Bagli"
    }
    ```

   ```
   http://127.0.0.1:8000/api/user/sign-in/
   method: POST
   request payload: 
   {
    "phone": "7415144601",
    "password": "Test@123"
   }
   ```
   
   ```
   http://127.0.0.1:8000/api/user/update/
   method: PUT
   request payload: 
   {
    "name": "Virendra Rawat",
    "email": "virendrasinghfgsdfsdfsddsfsdfrawat1485@gmail.com",
    "address": "indore"
   }
   Headers: 
   {
   "Authorization": Bearer <access_token>
   }
   ```
   
   ```
   http://127.0.0.1:8000/api/user/delete/
   Method: DELETE
   Headers: 
   {
   "Authorization": Bearer <access_token>
   }
   ```
   
   ```
   http://127.0.0.1:8000/api/business/list/
   Method: GET
   ```
   
   ```
   http://127.0.0.1:8000/api/business/registration/
   Method: POST
   request payload: 
   {
    "name": "abc",
    "registration_number": "4s454545",
    "email": "abc@gmail.com",
    "phone": "74185296321",
    "address": "indore"
   }
   ```

12. To Run test case:

   ```
   python manage.py test
   ```
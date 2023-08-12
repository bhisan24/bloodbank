# Online-Blood-Bank

After opening the online bloodbank folder using cmd terminal or anyother:

1. **Switch to Environment Directory**  
command: **cd env**  
command: **Scripts/activate**  

2. **Install all dependencies required for the project**  
command: **pip install -r requirements.txt**  

3. **Switch to online bloodbank main directory and then again switch to app directory**  

4. **Initiate Db Migrations to Generate Tables**  
command: **python manage.py makemigrations**  
command: **python manage.py migrate**  

5. **Create Superuser (Admin)**  
command: **python manage.py createsuperuser**  

6. **Run Server**  
command: **python manage.py runserver**  
The above command will run django server on localhost i.e. 127.0.0.1:8000/  

# alternative method to run frontend

7. **Run Server using xampp**  
place the online bloodbank folder inside xampp htdocs and use localhost/folder location to access frontend.
all other process are same as mentioned above.

8. **Access Admin Panel**  
command: **127.0.0.1:8000/admin**  

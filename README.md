# Real Estate Listing with google sheets reporting 
A basic userbased listing using Django 


# Project setup
install python3 and pip3

Best pratice is to create the virtualenv first and then installing the project in it.
command for installing virtuaenv
 
pip3 install virtualenv 

After creating the virtual environment or without creating it 
command for project setup
pip3 install -r requirements.txt

After project setup Run the command to get Database enabled with all db changes
Command for applying all migrations
python manage.py migrate

After the DB changes applied successfully
Run the command
python manage.py runserver

After this the local server will start on this RL http://127.0.0.1:8000/ 

# API Documentation using swagger
Using the following endpoint we can access the Docs of all APIS in system and chcek them
http://127.0.0.1:8000/swagger/



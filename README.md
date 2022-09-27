# EmployeesFeedback

## Create Virtual Env
create:

```sh
python -m pip install --user virtualenv
py -m venv <venv>
```
make sure you are in project directory

activate:
```sh
.\<venv>\Scripts\activate
```
## Installation
Install Required Packages. we have a requirement.txt file that contain all required packages list with its versions
```sh
pip install -r requirements.txt
```
After the installation we need to run the project before that reconfirm you are activated the virtual env and you are in project direction and find out there manage.py python file

## Run server
Before run server we need to create out database here i am using sqlite.
so we need to run migration commands are:
```sh
python manage.py makemigrations
python manage.py migrate
```
after that we need to create a superuser by using the command:
```sh
python manage.py createsuperuser
```
follow the commands and create a superuser after that we can run the server:
```sh
python manage.py runserver 
```
here the default port number is 8000 if we want to change the port no we can type the port number after the runserver command:
```sh
python manage.py runserver [port_number]
```
The url be like:[http://127.0.0.1:8000/]

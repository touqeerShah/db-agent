```
python3 -m venv ./path/to/
source ./path/to/bin/activate

```
# create user DB
python manage.py makemigrations
python manage.py migrate 

## Run app by 
python manage.py runserver


## For Token verifications
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install django-cors-headers
pip install psycopg2-binary
pip install python-dotenv
pip install pillow==10.0.0

pip install pip-tools

## API's
```
http://127.0.0.1:8000/api/verify_google_token/
{

"idToken":"TOKEN"
}
```
Setup local env

```
python3 -m venv ./nenv/
source ./nenv/bin/activate
```



```
FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]

```
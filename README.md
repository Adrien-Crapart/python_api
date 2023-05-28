# REST API Python

Get, Put, Update or Delete all the data on user request (with JWT)

## Organisation

- Dags folder
    - Dags run and schedulers
    - Scripts
    - Data files

- Configuration
    - `Change settings for dags runs`

- requirements
    - `Add news libraries for scripts`
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

Flask args

`FLASK_DEBUG=` 1 or 0

`JWT_SECRET_KEY`

Mail server

`SMTP_SERVER`

`SMTP_EMAIL`

`SMTP_PASSWORD`

Database connections

`DATABASE_URL` postgresql://user:password@postgres:5432/data
## Run Locally

Create python env folder

```bash
  python -m venv .
```

Go to python environment

```bash
  .venv\Scripts\activate.ps1
```

Install librairies

```bash
  pip install -r requirements.txt
```

Start the app

```bash
  python app.py
  OR
  flask run
```


## Deployment

To build all images on Docker with separates volumes

```bash
  docker-compose up -d --build
```
Exception for flower Celery mode
```bash
  docker-compose up -d --build flower
```
## Authors

- [@adrien.crapart](https://www.github.com/Adrien-Crapart)

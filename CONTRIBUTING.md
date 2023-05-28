# CONTRIBUTING

## How to run the Dockerfile locally

```
docker run -dp 5000:5000 -w /app/api -v "$(pwd):/app" rest-apis-flask-python sh -c "flask run"
```

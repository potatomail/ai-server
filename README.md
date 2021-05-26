# Initiate Virtual environment
```shell
python -m venv .venv
cd .venv
. ./bin/activate
```

# Running server
python app.py

# Dockerize & test
```shell
docker build -t ai-server .
docker run -p 5000:5000 ai-server
```

# Run with uwsgi
TODO
-------------
# AI Server client
Use `client.py`
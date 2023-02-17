# svc_query

Handles user queries and db operations.

## Usage

Make sure you have virtual env set up and running.

```
pip install -r requirements.txt
```

To run the server:

```
cd svc_query
uvicorn main:app --reload --port 9000
```

We use Qdrant as our db. So, please follow the instruction to get the
Qdrant server up and running.

To set up the db:

```
python3 -m svc_query.db.db_init
```

# FastAPI Web Application

This is a simple **FastAPI** web application. Follow the instructions below to set up and run the project locally.

---

### 1. Create a virtual environment

```bash
python3 -m venv venv
```

### 2. Activate the virtual environment

- On **Linux / macOS**:

  ```bash
  source venv/bin/activate
  ```

- On **Windows (PowerShell)**:

  ```powershell
  .\venv\Scripts\activate
  ```

### 3. Run the application

```bash
fastapi dev main.py
```

---

## Accessing the App

Once running, open your browser at:

- API Root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Interactive API docs (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Alternative API docs (ReDoc): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Example `main.py`

```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

---

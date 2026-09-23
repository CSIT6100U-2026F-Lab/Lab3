# Lab 3 — REST file service

## 1. Overview

Lab 2 implements the basic functionality of an online code explorer. 

Using a browser as entrance, the user can conduct the following things:
+ create new code file.
+ delete a code file.
+ edit and update code file.
+ refresh the code.

From an implementation perspective, these operations will be handled by sending a request to the backend (`backend`) and manipulate the data (`data/*`), and finally send a response back to the frontend. As the following model:

```
Browser --Request--> rest_service.py ----> data_logic.py --manipulate--> data/*
        <-Response--
```

Your task is to fill in the TODOs in rest_service, i.e. to handle the request, manipulate data, and send response. 

We have implemented the others for you:
+ The whole frontend.
+ The data manipulate logic (`backend/data_logic.py`).
  - **NOTE**: if you reuse the code in the file, it won't take too much code to finish the tasks.

## 2. Evaluation

The evaluation will be based on two perspectives (Section 6 will help you with this)
+ Whether the **basic functionalities** are supported
+ Whether the **erroneous cases** are handled

You can test your code based on
+ The browser GUI
+ The test case provided in `frontend/test.py` would test both normal and error behaviors.
  - We will grade your work based on this script.


## 3. File structure
```
Lab1/
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── style.css
|   ├── test.py             # test cases
│   └── serve.py            # static server on :5500
├── backend/
│   ├── data_logic.py       # shared disk layer (provided)
│   └── rest_service.py     # REST on :8000 — fill in the TODOs
├── data/                   # shared store
└── requirements.txt
```

## 4. Setup

```bash
pip install -r requirements.txt
```

## 5. Start

Use two seperate terminals:

The following command starts the backend server. 
```bash
python3 backend/rest_service.py
```


The following command starts the frontend server. 

```bash
python3 frontend/serve.py
```

Then open http://127.0.0.1:5500/ (Front) in your browser to use the frontend.


If a previous run left a port busy:
```bash
lsof -tiTCP:8000,5500 -sTCP:LISTEN | xargs kill
```

The following command runs the test cases.
```bash
python3 frontend/test.py
```


## 6. TODO

Fill in the `# TODO` bodies in `backend/rest_service.py`:

| Location | Function |
|----------|----------|
| `list_files` | List files, sorted by name |
| `get_file` | Return the UTF-8 contents of a file |
| `create_file` | Create a new file |
| `update_file` | Update an existing file |
| `delete_file` | Delete a file |

The interface specifications are listed as follows:

| Method | Path | Status |
|--------|------|--------|
| `GET` | `/files` | 200 |
| `GET` | `/file/{filename}` | 200, 400, 404 |
| `POST` | `/create/{filename}` | 201, 400, 409, 413 |
| `POST` | `/update/{filename}` | 200, 400, 404, 413 |
| `DELETE` | `/file/{filename}` | 200, 400, 404 |

Error codes:

| Status | Reason |
|--------|--------|
| 400 | Filename must be a single path segment under `data/`, such as `main.py`. Empty names, `.`, `..`, and names that contain `..`, `/`, or `\` all return 400. A file that is not valid UTF-8 also returns 400. |
| 404 | File not found |
| 409 | File already exists (create only) |
| 413 | Content larger than 5MB |

## 7. Ports

| Service | Bind | URL |
|---------|------|-----|
| Frontend | `127.0.0.1:5500` | http://127.0.0.1:5500/ |
| REST | `127.0.0.1:8000` | http://127.0.0.1:8000 (`/docs` for backend documentation) |



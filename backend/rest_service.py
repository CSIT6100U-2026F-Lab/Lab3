"""
Online Code Explorer — Lab 1 RESTful API

HTTP / CORS / status-code layer over the shared data_logic module.
Disk I/O lives in data_logic.py; this file must not read or write files.

Start from the project root:
    python3 backend/rest_service.py

Then open http://localhost:8000/docs for the Swagger UI.

Dependencies: fastapi, uvicorn, python-multipart
"""

import os
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import data_logic
from data_logic import (
    MAX_FILE_SIZE,
    DataFileExistsError,
    DataFileNotFoundError,
    FileTooLargeError,
    InvalidFilenameError,
    InvalidUtf8Error,
)

# Used by the direct-run entry point so uvicorn reloads from backend/.
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Pydantic models (HTTP layer only)
# ---------------------------------------------------------------------------


class FileInfo(BaseModel):
    """File metadata: name, size in bytes, last modified time (ISO 8601)."""

    name: str
    size: int
    last_modified: str


class FileContent(BaseModel):
    """File body, always treated as UTF-8 text."""

    content: str


# ---------------------------------------------------------------------------
# FastAPI app and middleware
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Online Code Explorer REST API",
    description="Lab 1: flat file management service (Python + FastAPI)",
    version="1.0.0",
)

# Allow the frontend (e.g. Live Server at http://localhost:5500) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _looks_like_traversal(value: str) -> bool:
    """Return True if a raw or decoded path contains traversal fragments."""
    lowered = value.lower()
    return ".." in value or "%2e%2e" in lowered or "%2f" in lowered or "%5c" in lowered


@app.middleware("http")
async def security_and_size_limits(request: Request, call_next):
    """Reject path traversal and request bodies larger than 5MB."""
    raw_path = request.scope.get("raw_path", b"").decode("latin-1")
    if _looks_like_traversal(request.url.path) or _looks_like_traversal(raw_path):
        return JSONResponse(status_code=400, content={"detail": "Invalid filename"})

    content_length = request.headers.get("content-length")
    if content_length is not None:
        try:
            length = int(content_length)
        except ValueError:
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid Content-Length header"},
            )
        if length > MAX_FILE_SIZE:
            return JSONResponse(
                status_code=413,
                content={"detail": "File too large. Maximum size is 5MB."},
            )
    return await call_next(request)


@app.on_event("startup")
def ensure_data_dir() -> None:
    """Create the data/ directory on startup if it does not exist."""
    data_logic.ensure_data_dir()

# ---------------------------------------------------------------------------
# API endpoints
# Register GET /files before GET /file/{filename} so /files is not captured
# as a path parameter (required if the routes ever share a prefix).
# ---------------------------------------------------------------------------


@app.get("/files", response_model=List[FileInfo])
def list_files() -> List[FileInfo]:
    """List files in data/, sorted by name."""
    # TODO
    raise NotImplementedError


@app.get("/file/{filename:path}", response_model=FileContent)
def get_file(filename: str) -> FileContent:
    """Return the UTF-8 contents of a file."""
    # TODO
    raise NotImplementedError


@app.post("/create/{filename:path}", response_model=FileInfo, status_code=201)
def create_file(filename: str, body: FileContent) -> FileInfo:
    """Create a new file. Returns 409 if it already exists."""
    # TODO
    raise NotImplementedError


@app.post("/update/{filename:path}", response_model=FileInfo)
def update_file(filename: str, body: FileContent) -> FileInfo:
    """Update an existing file. Returns 404 if it does not exist."""
    # TODO
    raise NotImplementedError


@app.delete("/file/{filename:path}")
def delete_file(filename: str) -> dict:
    """Delete a file. Returns 404 if it does not exist."""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Direct-run entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "rest_service:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        app_dir=_BACKEND_DIR,
    )

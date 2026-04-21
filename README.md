## Notebook Backend (FastAPI)

## Backend system inspired by NotebookLM that allows users to create accounts and manage documents with future support for AI-based document querying.

## What has been built so far

- FastAPI backend setup
- User creation API
- Get user API
- User schema validation using pydantic 
- Basic project structure (routes, services, models, db)

## Architecture (current stage)

Client Request -> FastAPI Route -> Service Layer -> Database Layer -> Postgres Database

## Project Structure

app/
 ├── main.py
 ├── routes/
 ├── models/
 ├── schemas/
 ├── services/
 └── db/


## Next Steps

- Document upload system
- Document storage in database
- Document processing layer (chunking)
- Query system for user documents
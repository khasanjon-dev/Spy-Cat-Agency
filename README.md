# Spy Cat Agency

A lightweight Django REST API for managing undercover spy cats, their missions, and mission targets. Breeds are
validated on the fly through TheCatAPI to keep your feline roster authentic.

## Requirements

- Python 3.10+
- pip (bundled with modern Python installs)
- Optional but recommended: `python -m venv` for an isolated environment

## Setup

```bash
git clone https://github.com/khasanjon-dev/Spy-Cat-Agency.git
cd Spy-Cat-Agency
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run The API

```bash
python manage.py migrate
python manage.py runserver
```

The dev server defaults to `http://127.0.0.1:8000/` and all API routes are namespaced under `/api/` (for example,
`http://127.0.0.1:8000/api/spy-cats/`).
Swagger url: http://127.0.0.1:8000/swagger/

## Try The Endpoints

- Import `SpyCatAgency.postman_collection.json` into Postman (or your favorite REST client) to explore the Spy Cats,
  Missions, and Targets endpoints.
- Auth isn’t required; every request is JSON over HTTP.

That’s it—clone, install, migrate, and run to start issuing feline assignments. 🐾

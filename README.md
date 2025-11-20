# Spy Cat Agency – Django REST API

A CRUD backend service for managing spy cats, their missions, and assigned targets.

## Technologies Used

* Python 3.10+
* Django 4.x
* Django REST Framework
* SQLite (default)
* Requests (for TheCatAPI integration)

## Installation & Setup

```bash
git clone <your-repo-url>
cd <repo-folder>

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

The server will run at:

```
http://127.0.0.1:8000/
```

## API Base URL

All endpoints are prefixed with `/api/`:

```
http://127.0.0.1:8000/api/...
```

---

## Endpoints

## Spy Cats

### `POST /api/spy-cats/`

Create a new spy cat.

Example body:

```json
{
  "name": "Agent Whiskers",
  "years_of_experience": 5,
  "breed": "bengal",
  "salary": "5000.00"
}
```

* `breed` is validated via TheCatAPI.
* If the breed is invalid → `400 Bad Request`.

### `GET /api/spy-cats/`

Get a list of all spy cats.

### `GET /api/spy-cats/{id}/`

Get details of a single spy cat.

### `PATCH /api/spy-cats/{id}/`

Only `salary` can be updated.
If any other field is included → `400 Bad Request`.

### `DELETE /api/spy-cats/{id}/`

Delete a spy cat.

---

## Missions

### Create Mission + Targets

### `POST /api/missions/`

Creates a mission along with its targets in one request.

Example body:

```json
{
  "cat": null,
  "targets": [
    {
      "name": "Target A",
      "country": "UK",
      "notes": "Initial info",
      "is_completed": false
    },
    {
      "name": "Target B",
      "country": "US",
      "notes": "",
      "is_completed": false
    }
  ]
}
```

Rules:

* Number of targets must be between **1 and 3**.
* Mission is created with `is_completed = false`.
* Targets must include name, country, notes, and completion status.

### `GET /api/missions/`

List all missions (with targets and assigned cat if available).

### `GET /api/missions/{id}/`

Get details of a mission (including targets and cat).

### `DELETE /api/missions/{id}/`

Delete a mission.

If the mission already has an assigned cat:

* Return `400 Bad Request`.

### Assign a Cat to a Mission

### `POST /api/missions/{id}/assign_cat/`

Request body:

```json
{
  "cat_id": 1
}
```

Rules:

* Invalid `cat_id` → `404 Not Found`
* If the cat already has an active (not completed) mission → `400 Bad Request`
* On success, returns full mission details

---

## Targets

Targets are created only when a mission is created — no separate CREATE endpoint.

### `PATCH /api/targets/{id}/`

Update a target.

Allowed:

* Update `notes`
* Mark `is_completed = true`

Restrictions:

* If a target is already completed → notes **cannot** be changed.
* If the mission is completed → neither notes nor completion can be changed.
* Violations → `400 Bad Request`.

Extra rule:

* If *all* targets of a mission are completed → the mission automatically becomes completed.

### `GET /api/targets/{id}/`

Get details of a single target.

### `GET /api/targets/`

Get a list of all targets (mostly for technical/debugging purposes).

### `DELETE /api/targets/{id}/`

Delete a target. The mission stays intact.

### `POST /api/targets/`

Not allowed.
Returns `405 Method Not Allowed`.

---

## Validation Rules

### SpyCat

* `name` cannot be empty
* `years_of_experience` must be non-negative
* `salary` must be positive
* `breed` must be a valid breed from TheCatAPI

### Mission

* Number of targets must be between 1 and 3
* `cat` is optional, but can be assigned later using `assign_cat`

### Targets

* `name` and `country` required
* `notes` optional
* Completed targets or completed missions cannot be modified

---

## TheCatAPI Integration

Breed validation is performed by calling:

```
https://api.thecatapi.com/v1/breeds
```

The `is_valid_breed` function (in `agency/services.py`) handles this.

If TheCatAPI is unreachable, the current behavior treats the breed as invalid.
You can change this logic if needed.

---

## Postman Collection

Create a full Postman collection that includes:

* Base URL: `http://127.0.0.1:8000/api`
* CRUD operations for:

    * Spy Cats
    * Missions (incl. `assign_cat`)
    * Targets (with PATCH for notes & completion)
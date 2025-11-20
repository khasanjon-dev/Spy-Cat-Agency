import requests

from config.settings import CAT_API_URL


def is_valid_breed(breed_id_or_name: str) -> bool:
    try:
        resp = requests.get(CAT_API_URL, timeout=5)
        resp.raise_for_status()
    except requests.RequestException:
        return False

    breeds = resp.json()
    breed_lower = (breed_id_or_name or "").strip().lower()

    for b in breeds:
        if b.get("id", "").lower() == breed_lower:
            return True
        if b.get("name", "").lower() == breed_lower:
            return True

    return False

from datetime import datetime
from .storage import url_store, store_lock
from .utils import generate_short_code, is_valid_url

def shorten_url(url):
    if not is_valid_url(url):
        raise ValueError("Invalid URL")

    short_code = generate_short_code()
    with store_lock:
        while short_code in url_store:
            short_code = generate_short_code()
        url_store[short_code] = {
            "url": url,
            "created_at": datetime.utcnow().isoformat(),
            "clicks": 0
        }
    return {
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }

def get_original_url(short_code):
    with store_lock:
        data = url_store.get(short_code)
        if not data:
            return None
        data["clicks"] += 1
        return data["url"]

def get_stats(short_code):
    with store_lock:
        data = url_store.get(short_code)
        if not data:
            return None
        return {
            "url": data["url"],
            "clicks": data["clicks"],
            "created_at": data["created_at"]
        }

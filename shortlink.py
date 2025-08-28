import random, requests
from typing import Tuple, Dict, Any, List
from config import SHORTLINK_PROVIDERS

class ShortlinkError(Exception):
    pass

def _shorten_adlinkfly(api: str, key: str, long_url: str) -> str:
    # AdLinkFly pattern: GET {api}?api={key}&url={url}&format=json
    r = requests.get(api, params={"api": key, "url": long_url, "format": "json"}, timeout=15)
    data = r.json()
    # Try common fields
    return data.get("shortenedUrl") or data.get("short") or data.get("result_url") or data.get("result") or data.get("url")

def _shorten_generic_key(api: str, key: str, long_url: str) -> str:
    r = requests.get(api, params={"key": key, "url": long_url}, timeout=15)
    data = r.json()
    return data.get("short") or data.get("result_url") or data.get("result") or data.get("url")

def shorten_once(long_url: str) -> Tuple[str, str]:
    if not SHORTLINK_PROVIDERS:
        raise ShortlinkError("No providers configured")
    providers: List[Dict[str, Any]] = SHORTLINK_PROVIDERS[:]
    random.shuffle(providers)
    last_err = None
    for p in providers:
        try:
            api = p["api_url"].rstrip("/")
            key = p["api_key"]
            ptype = p.get("type", "adlinkfly")
            if ptype == "adlinkfly":
                short = _shorten_adlinkfly(api, key, long_url)
            else:
                short = _shorten_generic_key(api, key, long_url)
            if not short:
                raise ShortlinkError("No short in response")
            return p.get("name", api), short
        except Exception as e:
            last_err = e
            continue
    raise ShortlinkError(f"All providers failed: {last_err}")

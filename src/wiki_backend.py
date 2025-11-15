from typing import List, Dict, Optional

import requests

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {
    "User-Agent": "workflow-test-app/0.1 (https://github.com/k3aworks/workflow-test-app)",
}


def search_occupation(occupation: str, limit: int = 10) -> List[str]:
    """Search Wikipedia for pages related to the given occupation.

    Sub 1.4 scope:
    - Implement real searching logic
    - Replace fake names with actual names from Wikipedia results
    - Return names for the GUI listbox
    """

    occupation = (occupation or "").strip()
    if not occupation:
        return []

    params = {
        "action": "query",
        "list": "search",
        "format": "json",
        "srsearch": occupation,
        "srlimit": limit,
    }

    try:
        response = requests.get(
            WIKIPEDIA_API_URL,
            params=params,
            headers=HEADERS,
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
    except Exception:
        # On any network/parse error, fall back to an empty list
        return []

    search_results = data.get("query", {}).get("search", [])
    titles: List[str] = []

    for item in search_results:
        title = item.get("title")
        if isinstance(title, str) and title.strip():
            titles.append(title.strip())

    return titles


def search_occupation_with_urls(occupation: str, limit: int = 10) -> List[Dict[str, str]]:
    """Search Wikipedia and return both titles and page URLs for each result.

    The existing ``search_occupation`` helper is kept for callers that only need
    a list of titles. This function is used when we need to open the
    corresponding Wikipedia page in a browser.
    """

    occupation = (occupation or "").strip()
    if not occupation:
        return []

    params = {
        "action": "query",
        "list": "search",
        "format": "json",
        "srsearch": occupation,
        "srlimit": limit,
    }

    try:
        response = requests.get(
            WIKIPEDIA_API_URL,
            params=params,
            headers=HEADERS,
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
    except Exception:
        return []

    search_results = data.get("query", {}).get("search", [])
    results: List[Dict[str, str]] = []

    for item in search_results:
        title = item.get("title")
        page_id = item.get("pageid")
        if not (isinstance(title, str) and title.strip()):
            continue
        if not isinstance(page_id, int):
            continue

        url = f"https://en.wikipedia.org/?curid={page_id}"
        results.append({"title": title.strip(), "url": url})

    return results


def _extract_first_wikilink_text(value: str) -> str:
    text = (value or "").strip()
    if text.startswith("[[") and "]]" in text:
        inner = text[2:].split("]]", 1)[0]
        parts = inner.split("|")
        text = parts[-1].strip()
    return text


def _extract_nationality_from_short_description(content: str) -> Optional[str]:
    """Best-effort extraction of nationality from the Short description template.

    Many biographies use a template like::

        {{Short description|Indian actor and politician (born 1974)}}

    We treat the first word of the short description (before any parentheses)
    as the nationality, e.g. "Indian".
    """

    marker = "{{short description|"

    for line in content.splitlines():
        lower = line.lower()
        idx = lower.find(marker)
        if idx == -1:
            continue

        after = line[idx + len(marker) :]
        if "}}" in after:
            desc = after.split("}}", 1)[0].strip()
        else:
            desc = after.strip()

        if not desc:
            continue

        # Drop any trailing parenthetical like "(born 1974)".
        desc_no_paren = desc.split("(", 1)[0].strip()
        if not desc_no_paren:
            continue

        parts = desc_no_paren.split()
        if not parts:
            continue

        first_word = parts[0].strip()
        if first_word:
            return first_word

    return None


def fetch_nationality(page_title: str) -> Optional[str]:
    page_title = (page_title or "").strip()
    if not page_title:
        return None

    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "formatversion": 2,
        "titles": page_title,
        "format": "json",
    }

    try:
        response = requests.get(
            WIKIPEDIA_API_URL,
            params=params,
            headers=HEADERS,
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
    except Exception:
        return None

    pages = data.get("query", {}).get("pages", [])
    if not pages:
        return None

    revisions = pages[0].get("revisions") or []
    if not revisions:
        return None

    slots = revisions[0].get("slots") or {}
    content = slots.get("main", {}).get("content")
    if not isinstance(content, str):
        return None

    nationality_value: Optional[str] = None
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        # Expect lines like "| nationality = [[Indian]]" or "|citizenship=[[Indian]]".
        if "=" not in stripped:
            continue
        field_part, value_part = stripped[1:].split("=", 1)
        field_name = field_part.strip().lower()
        value = value_part.strip()

        if field_name not in {"nationality", "citizenship"}:
            continue

        nationality_value = value
        if nationality_value:
            break

    if not nationality_value:
        nationality_value = _extract_nationality_from_short_description(content)
        if not nationality_value:
            return None

    nationality_value = _extract_first_wikilink_text(nationality_value)
    nationality_value = nationality_value.strip()
    if not nationality_value:
        return None

    return nationality_value

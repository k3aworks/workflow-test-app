from typing import List

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

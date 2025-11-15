from typing import List, Dict, Optional

import re
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


def _extract_first_year(text: str) -> Optional[int]:
    if not text:
        return None

    match = re.search(r"(\d{4})", text)
    if not match:
        return None

    try:
        year = int(match.group(1))
    except ValueError:
        return None

    if 1000 <= year <= 2100:
        return year

    return None


def _extract_birth_year_from_short_description(text: str) -> Optional[int]:
    if not text:
        return None

    # Prefer an explicit "born YYYY" if present anywhere.
    born_match = re.search(r"born\s+(\d{4})", text)
    if born_match:
        try:
            year = int(born_match.group(1))
        except ValueError:
            year = None
        if year is not None and 1000 <= year <= 2100:
            return year

    # Otherwise, look inside the first parentheses, which often contain dates.
    paren_match = re.search(r"\(([^)]*)\)", text)
    if paren_match:
        inner = paren_match.group(1)
        year_in_paren = _extract_first_year(inner)
        if year_in_paren is not None:
            return year_in_paren

    # Fallback: any year in the text.
    return _extract_first_year(text)


def _extract_birth_year_from_infobox(content: str) -> Optional[int]:
    """Best-effort extraction of birth year from infobox lines.

    Looks for fields such as "birth_date" or "born" and extracts a year
    from their value.
    """

    if not content:
        return None

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if "=" not in stripped:
            continue

        field_part, value_part = stripped[1:].split("=", 1)
        field_name = field_part.strip().lower().replace("_", " ")
        value = value_part.strip()

        if field_name not in {"birth date", "birth_date", "born"}:
            continue

        year = _extract_first_year(value)
        if year is not None:
            return year

    return None


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


def fetch_birth_year(page_title: str) -> Optional[int]:
    """Return the birth year for the given page, if it can be inferred.

    For Sub 2.3 we use a pragmatic approach based on the page's short
    description, which often looks like::

        "Indian actor and politician (born 1974)"

    or::

        "German-born theoretical physicist (18791955)".

    In both cases, the first 4-digit year is the birth year.
    """

    page_title = (page_title or "").strip()
    if not page_title:
        return None

    params = {
        "action": "query",
        "prop": "pageprops|revisions",
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

    page = pages[0]

    # First, try to get the birth year from the infobox in the wikitext.
    revisions = page.get("revisions") or []
    if revisions:
        slots = revisions[0].get("slots") or {}
        content = slots.get("main", {}).get("content")
        if isinstance(content, str):
            year = _extract_birth_year_from_infobox(content)
            if year is not None:
                return year

    # Fallback: try to infer from the short description via pageprops.
    pageprops = page.get("pageprops") or {}
    short_desc = pageprops.get("wikibase-shortdesc") or ""

    year = _extract_birth_year_from_short_description(short_desc)
    if year is None:
        return None

    return year

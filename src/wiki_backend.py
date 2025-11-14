from typing import List


def search_occupation(occupation: str) -> List[str]:
    """Return a temporary fake list of names for a given occupation.

    This is a placeholder implementation for Sub 1.3. It does not call any
    external services. Later sub-issues will replace this with real
    Wikipedia-backed logic.
    """

    occupation = occupation.strip().lower()

    if not occupation:
        return []

    if "engineer" in occupation:
        return [
            "Alice Example (Engineer)",
            "Bob Builder (Engineer)",
            "Charlie Circuit (Engineer)",
        ]

    if "doctor" in occupation or "physician" in occupation:
        return [
            "Dana Care (Doctor)",
            "Elliot Heal (Doctor)",
            "Frank Clinic (Doctor)",
        ]

    if "teacher" in occupation or "professor" in occupation:
        return [
            "Grace Guide (Teacher)",
            "Henry Learn (Teacher)",
            "Ivy Mentor (Teacher)",
        ]

    # Default fallback dummy data
    return [
        "Jamie Sample",
        "Kai Placeholder",
        "Lee Demo",
    ]

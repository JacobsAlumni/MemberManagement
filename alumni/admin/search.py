from __future__ import annotations


class AlumniSearch:
    search_fields = [
        "givenName",
        "middleName",
        "familyName",
        "email",
        "existingEmail",
        "approval__gsuite",
        "membership__customer",
    ]

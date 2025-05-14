from enum import Enum
from typing import Literal


class GetSearchFacetId(str, Enum):
    ACCESSRIGHT = "accessRight"
    COLLECTION = "collection"
    CONTENTLENGTH = "contentLength"
    COPYRIGHT = "copyright"
    COUNTRY = "country"
    DATADOMAIN = "dataDomain"
    DATERANGE = "daterange"
    LANGUAGE = "language"
    LOCATION = "location"
    MONTH = "month"
    NAG = "nag"
    NEWSPAPER = "newspaper"
    PARTNER = "partner"
    PERSON = "person"
    TOPIC = "topic"
    TYPE = "type"
    YEAR = "year"

    def __str__(self) -> str:
        return str(self.value)


GetSearchFacetIdLiteral = Literal[
    "accessRight",
    "collection",
    "contentLength",
    "copyright",
    "country",
    "dataDomain",
    "daterange",
    "language",
    "location",
    "month",
    "nag",
    "newspaper",
    "partner",
    "person",
    "topic",
    "type",
    "year",
]

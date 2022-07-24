from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.models.base import BaseModel, IdLookupMixin


def transform_scryfall_data(sf_data):
    return {
        "oracle_id": sf_data["oracle_id"],
        "name": sf_data["name"],
        "image_uri": (sf_data.get("image_uris") or sf_data["card_faces"][0]["image_uris"])[
            "normal"
        ],
        "vrd_legal": sf_data["legalities"]["vintage"] in ["legal", "restricted"],
    }


class Card(BaseModel, IdLookupMixin):
    __tablename__ = "cards"

    oracle_id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    image_uri = Column(String, nullable=False)
    vrd_legal = Column(Boolean, nullable=False)

    @classmethod
    def search_by_name_part(cls, part, session=None):
        return cls.query(session).filter(cls.name.contains(part, autoescape=True))

    @classmethod
    def from_scryfall(cls, sf_data):
        return cls.from_dict(transform_scryfall_data(sf_data))

    def update_from_scryfall(self, sf_data):
        return self.update_from_dict(transform_scryfall_data(sf_data))

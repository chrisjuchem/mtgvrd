from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.session import Session

from app.db.connection import ensure_session


@as_declarative()
class BaseModel:
    @classmethod
    def from_dict(cls, dct, ignore_extra=False):
        class_columns = class_mapper(cls).attrs.keys()
        if ignore_extra:
            dct = {key: val for key, val in dct.items() if key in class_columns}
        return cls(**dct)

    def update_from_dict(self, dct, ignore_extra=False):
        class_columns = class_mapper(self.__class__).attrs.keys()
        if ignore_extra:
            dct = {key: val for key, val in dct.items() if key in class_columns}
        for key, val in dct.items():
            setattr(self, key, val)

    @classmethod
    def query(cls, session=None):
        with ensure_session(session) as ses:
            return ses.query(cls)

    @property
    def session(self):
        return Session.object_session(self)

    def save(self):
        self.session.commit()


class IdLookupMixin:
    @classmethod
    def lookup_by_id(cls, id_, session=None):
        return cls.query(session).get(id_)

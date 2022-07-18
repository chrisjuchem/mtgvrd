from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.session import Session

from app.db.connection import ensure_session


@as_declarative()
class BaseModel(object):
    @classmethod
    def from_dict(cls, d, ignore_extra=False):
        class_columns = class_mapper(cls).attrs.keys()
        if ignore_extra:
            d = {key: val for key, val in d.items() if key in class_columns}
        return cls(**d)

    def update_from_dict(self, d, ignore_extra=False):
        class_columns = class_mapper(self.__class__).attrs.keys()
        if ignore_extra:
            d = {key: val for key, val in d.items() if key in class_columns}
        for key, val in d.items():
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
    def lookup_by_id(cls, id, session=None):
        return cls.query(session).get(id)

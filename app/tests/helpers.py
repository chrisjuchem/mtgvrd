import pytest

from app.db.connection import ensure_session
from app.db.models import BaseModel


def _reset_database():
    with ensure_session() as ses:
        # defer evaluating constraints until commit occurs.
        # With Postgres, this type of setting applies to the current transaction only - not
        #   a global change.
        ses.execute("SET CONSTRAINTS ALL DEFERRED;")
        for table in reversed(BaseModel.metadata.sorted_tables):  # pylint: disable=no-member
            ses.execute(table.delete())
        ses.commit()


class TestBase:
    pass


class TestBaseEphemeral(TestBase):
    @pytest.fixture(autouse=True)
    def reset_database(self):
        _reset_database()


class TestBasePersistent(TestBase):
    @pytest.fixture(scope="class", autouse=True)
    def reset_database(self):
        _reset_database()


class ArgClass:
    """
    Helper class for checking whether mock call args are of a particular class

    ex:
    assert some_function_mock.called_with(1, ArgClass(list))
    """

    def __init__(self, cls):
        self.cls = cls

    def __eq__(self, other):
        return isinstance(other, self.cls)

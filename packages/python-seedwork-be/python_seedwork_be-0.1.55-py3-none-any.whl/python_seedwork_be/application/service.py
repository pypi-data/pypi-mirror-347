from typing import Callable, List

from dino_seedwork_be.adapters.persistance.sql.AbstractUnitOfWork import \
    AbstractUnitOfWork
from dino_seedwork_be.adapters.persistance.sql.DBSessionUser import \
    DBSessionUser

UowFactory = Callable[[List[DBSessionUser]], AbstractUnitOfWork]

# __all__ = ["AbstractUOWApplicationService"]


class AbstractUOWApplicationService:

    _uow: UowFactory

    def uow(self, user_session: List[DBSessionUser]) -> AbstractUnitOfWork:
        return self._uow(user_session)

    def set_uow(self, uow: UowFactory):
        self._uow = uow

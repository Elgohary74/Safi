import logging
from abc import ABC, abstractmethod


class IRepository(ABC):
    def __init__(self):
        from app.services.database import MongoDatabase

        self.db = MongoDatabase().get_db()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def get_by_id(self, id: str):
        pass

    @abstractmethod
    def update(self, id: str, data: dict):
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

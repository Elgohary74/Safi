import logging
from abc import ABC, abstractmethod

from app.services.database import MongoDatabase


class IRepository(ABC):
    def __init__(self):
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

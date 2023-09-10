from abc import ABC, abstractmethod


class JobApi(ABC):

    @abstractmethod
    def get_vacancies(self, search_term: str, city: str = None, experience: str = None, count=None):
        pass

    @staticmethod
    @abstractmethod
    def _parse(response: dict) -> list:
        pass








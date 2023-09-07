import os
from abc import ABC, abstractmethod
import requests

from exception import APIError
from vacancy import Vacancy


class JobApi(ABC):

    @abstractmethod
    def get_vacancies(self, search_term: str, city: str = None, experience: str = None, count=None):
        pass


class HeadHunterAPI(JobApi):
    def get_vacancies(self, search_term: str, city: str = None, experience: str = None, count=None, order_by=None):

        params = {"text": search_term,
                  "area": city,
                  "experience": experience,
                  "per_page": count,
                  "order_by": order_by
                  }
        response = requests.get('https://api.hh.ru/vacancies', params=params)

        vacancies = []

        for one_vac in response.json():
            name = str(one_vac['name'])
            description = str(one_vac['responsibility'])
            company = int(one_vac['employer']['name'])
            salary = int(one_vac['salary']['to'])
            currency = str(one_vac['salary']['currency'])

            vacancy = Vacancy(name,
                              description,
                              company,
                              salary,
                              currency)

            vacancies.append(vacancy)

        return vacancies


class SuperJobAPI(JobApi):
    def get_vacancies(self, search_term: str, city: str = None, experience: str = None, count=None, order_by=None):

        params = {"text": search_term,
                  "area": city,
                  "experience": experience,
                  "per_page": count,
                  "order_by": order_by
                  }
        headers = {"X-Api-App-Id": os.getenv("SJ_API_KEY")} #SJ_API_KEY

        response = requests.get('https://api.superjob.ru/2.0/vacancies', params=params, headers=headers)

        if response.status_code != 200:
            raise APIError('Не верный API')

        vacancies = []

        for one_vac in response.json():
            name = str(one_vac['profession'])
            description = str(one_vac['work'])
            company = int(one_vac['id_client'])
            salary = int(one_vac['payment_from'])
            currency = str(one_vac['currency'])

            vacancy = Vacancy(name,
                              description,
                              company,
                              salary,
                              currency)

            vacancies.append(vacancy)

        return vacancies


hh = HeadHunterAPI()
print(hh.get_vacancies('Python'))

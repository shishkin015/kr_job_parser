import os

import requests

from API_hh_sjob.jobapi import JobApi
from src.vacancy import Vacancy


class SuperJobAPI(JobApi):
    def get_vacancies(self, search_term: str, city: str = None, experience: str = None, count=None, order_by=None):
        """
                    Отправляет запрос к API HeadHunter для поиска вакансий.

                    :param search_term: Термин поиска или ключевая фраза.
                    :type search_term: str

                    :param city: Город для фильтрации результатов (по умолчанию None).
                    :type city: str or None

                    :param experience: Уровень опыта для фильтрации результатов (по умолчанию None).
                    :type experience: str or None

                    :param count: Количество результатов для запроса (по умолчанию None).
                    :type count: int or None

                    :param order_by: Параметр сортировки результатов (по умолчанию None).
                    :type order_by: str or None

                    :return: Список объектов Vacancy, представляющих найденные вакансии.
                    :rtype: list[Vacancy]
                    """

        try:
            params = {"text": search_term,
                      "area": city,
                      "experience": experience,
                      "per_page": count,
                      "order_by": order_by
                      }
            headers = {"X-Api-App-Id": os.getenv("SJ_API_KEY")}  # SJ_API_KEY

            response = requests.get('https://api.superjob.ru/2.0/vacancies', params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if len(data) == 0:
                    print("Нет данных")
                    return []
                else:
                    return SuperJobAPI._parse(data)
            elif response.status_code == 404:
                raise Exception("Запрос не выполнен (статус кода: 404)")

        except requests.exceptions.RequestException:
            return []

    @staticmethod
    def _parse(data: dict) -> list:

        vacancies = []

        for one_vac in data['objects']:
            salary_from = float(one_vac.get('payment_from')) if one_vac.get('payment_from') != 0 else None
            salary_to = float(one_vac.get('payment_to')) if one_vac.get('payment_to') != 0 else None
            currency = str(one_vac.get('currency'))

            vacancy = Vacancy(
                int(one_vac.get('id', 'Нет данных')),
                str(one_vac.get('profession', 'Нет данных')),
                str(one_vac.get('employer', {}).get('name', 'Нет данных')),
                str(one_vac.get('candidat', 'Нет данных')),
                salary_from,
                salary_to,
                currency,
                str(one_vac.get('town', {}).get('title', 'Нет данных')),
                str(one_vac.get('link', 'Нет данных')),
            )

            vacancies.append(vacancy)

        return vacancies


class ControllerSuperJob:
    """
        Класс-контроллер для управления параметрами запросов к API SuperJob.

        Methods:
            validate_city(city: str):
                Проверяет, существует ли указанный город в API SuperJob.

            order_by(param: str):
                Возвращает параметр сортировки для запроса.

    """

    @staticmethod
    def validate_city(city: str):
        """
        Проверяет, существует ли указанный город в API SuperJob.
        :param city: Название города.
        :type city: str
        :return: Название города, если он существует, в противном случае - None.
        :rtype: str or None
        """
        if len(city) == 0:
            return None
        else:
            url = "https://api.superjob.ru/2.0/towns/"

            headers = {
                "X-Api-App-Id": os.getenv("SJ_API_KEY")
            }
            # Getting JSON with cities
            response = requests.get(url, headers=headers).json()

            # Checking if city exists in json
            for item in response["objects"]:
                if item['title'] == city:
                    return city
        return None

    @staticmethod
    def order_by(param: str):
        """
        Возвращает параметр сортировки для запроса.
        :param param: Строковое значение, определяющее параметр сортировки.
        :type param: str
        :return: Параметр сортировки для запроса.
        :rtype: str
        """
        if param == "1":
            return "date"
        elif param == "2":
            return "payment_desc"
        else:
            return "relevance"
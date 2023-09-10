import requests

from API_hh_sjob.jobapi import JobApi
from src.vacancy import Vacancy


class HeadHunterAPI(JobApi):
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
            response = requests.get('https://api.hh.ru/vacancies', params=params)
            if response.status_code == 200:
                data_from_json = response.json()
                if data_from_json['found'] == 0:
                    print("Нет вакансий")
                    return []
                else:
                    return HeadHunterAPI._parse(data_from_json)
            elif response.status_code == 404:
                raise Exception("Request failed (404 status code)")

        except requests.exceptions.RequestException:
            return []

    @staticmethod
    def _parse(data_from_json: dict) -> list:

        vacancies = []

        for one_vac in data_from_json["items"]:

            salary = one_vac.get('salary', {})

            if salary:
                salary_from = float(salary.get('from')) if salary.get('from') is not None else 0
                salary_to = float(salary.get('to')) if salary.get('to') is not None else 0
                salary_currency = str(salary.get('currency'))
            else:
                salary_from = salary_to = 0
                salary_currency = 'Нет данных'

            vacancy_name = str(one_vac['name'])
            description = str(one_vac['snippet']['responsibility']) if one_vac['snippet'][
                                                                      'responsibility'] is not None else "Нет данных"
            company_name = str(one_vac['employer']['name']) if one_vac['employer']['name'] is not None else "Нет данных"
            id_num = int(one_vac['id']) if one_vac['id'] is not None else 0
            area = str(one_vac['area']['name']) if one_vac['area']['name'] is not None else "Нет данных"
            url = str(one_vac['url']) if one_vac['url'] is not None else "Нет данных"

            vacancy = Vacancy(id_num,
                              vacancy_name,
                              company_name,
                              description,
                              salary_from,
                              salary_to,
                              salary_currency,
                              area,
                              url,
                              )

            vacancies.append(vacancy)

        return vacancies


class ControllerHH:
    """
        Класс-контроллер для управления параметрами запросов к API HeadHunter.

        Methods:
            get_city_id(city: str):
                Получает идентификатор города по его названию.

            order_by(param: str):
                Возвращает параметр сортировки для запроса.

        """

    @staticmethod
    def get_city_id(city: str):
        """
        Получает идентификатор города по его названию.
        :param city: Название города.
        :type city: str
        :return: Идентификатор города в API HeadHunter.
        :rtype: int or None
        """
        if len(city) == 0:
            return None
        else:
            response = requests.get("https://api.hh.ru/areas").json()

            for area in response:
                for country in area["areas"]:
                    if "areas" in country and country["areas"]:  # Проверяем наличие и непустой список areas
                        for region in country["areas"]:
                            if region["name"] == city:
                                return region["id"]
                    elif country["name"] == city:  # Если список пустой, сравниваем имя страны с городом
                        return country["id"]

    @staticmethod
    def order_by(param: str):
        """
        Возвращает параметр сортировки для запроса.
        :param param: Строковое значение, определяющее параметр сортировки.
        :type param: str
        :return: Параметр сортировки для запроса.
        :rtype: str or None
        """

        if param == "1":
            return "publication_time"
        elif param == "2":
            return "salary_desc"
        else:
            return None
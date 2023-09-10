import requests

from API_hh_sjob.jobapi import JobApi
from vacancy import Vacancy


class HeadHunterAPI(JobApi):
    def get_vacancies(self, search_term: str, city: str = None, experience: str = None, count=None, order_by=None):

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

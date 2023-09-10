import os

import requests

from API_hh_sjob.jobapi import JobApi
from vacancy import Vacancy


class SuperJobAPI(JobApi):
    def get_vacancies(self, search_term: str, city: str = None, experience: str = None, count=None, order_by=None):

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

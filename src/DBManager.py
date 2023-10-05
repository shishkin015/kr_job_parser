import psycopg2

from src.vacancy import Vacancy


class DBManager:
    """
    Класс DBManager предоставляет методы для работы с базой данных PostgreSQL и таблицей 'vacancies'.
    """

    def __init__(self):
        """
        Инициализирует объект класса DBManager и устанавливает соединение с базой данных PostgreSQL.
        """
        self.connection = psycopg2.connect(
            host="Localhost",
            database="postgres",
            user="postgres",
            password="admin@123",
        )

    def checking_for_emptiness(self) -> bool:
        """
        Проверяет, пуста ли таблица 'vacancies' в базе данных.
        :return:
        """
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM vacancies")
                row_count = cursor.fetchone()[0]

                if row_count == 0:
                    print("Ваша БД пуста!")
                    return False
                else:
                    return True

    def get_companies_and_vacancies_count(self):
        """
        Получает список компаний и количество вакансий у каждой компании, выводя результаты на экран.
        :return:
        """
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT company_name, COUNT(*) AS vacancy_count
                    FROM public.vacancies
                    GROUP BY company_name
                    ORDER BY vacancy_count DESC;
                """)
                results = cursor.fetchall()

                for row in results:
                    company_name, vacancy_count = row
                    print(f"Компания: {company_name}, Количество вакансий: {vacancy_count}")

    def get_all_vacancies(self) -> list[Vacancy]:
        """
        Получает все вакансии из таблицы 'vacancies' и возвращает их в виде списка объектов класса Vacancy.
        :return:
        """

        rows = None
        list_vacancies = []
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM vacancies")
                rows = cursor.fetchall()

        for row in rows:
            (_, id_num, vacancy_name, company_name, description, salary_from, salary_to, salary_currency, area,
             url) = row
            vacancy = Vacancy(id_num, vacancy_name, company_name, description, float(salary_from), float(salary_to),
                              salary_currency,
                              area, url)
            list_vacancies.append(vacancy)
        return list_vacancies

    def get_avg_salary(self):
        """
        Вычисляет и выводит среднюю зарплату по всем вакансиям в таблице 'vacancies'.
        :return:
        """
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT AVG(salary_from) AS average_salary
                    FROM public.vacancies;
                """)
                average_salary = cursor.fetchone()[0]
                print(f"Средняя зарплата по вакансиям: {average_salary}")

    def get_vacancies_with_higher_salary(self):
        """
         Получает список вакансий, у которых зарплата выше средней, и возвращает их в виде списка объектов класса Vacancy.
        :return:
        """
        rows = None
        list_vacancies = []

        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT *
                    FROM public.vacancies
                    WHERE salary_from > (SELECT AVG(salary_from) FROM public.vacancies);
                """)
                results = cursor.fetchall()
                for row in results:
                    (_, id_num, vacancy_name, company_name, description, salary_from, salary_to, salary_currency, area,
                     url) = row
                    vacancy = Vacancy(id_num, vacancy_name, company_name, description, float(salary_from),
                                      float(salary_to),
                                      salary_currency,
                                      area, url)
                    list_vacancies.append(vacancy)
        return list_vacancies

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список вакансий, в названии которых содержится переданное ключевое слово 'keyword',
        и возвращает их в виде списка объектов класса Vacancy.
        :param keyword:
        :return:
        """
        result = None
        list_vacancies = []

        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                        SELECT *
                        FROM public.vacancies
                        WHERE vacancy_name LIKE %s;
                    """, ('%' + keyword + '%',))
                results = cursor.fetchall()

        for row in results:
            (_, id_num, vacancy_name, company_name, description, salary_from, salary_to, salary_currency, area,
             url) = row
            vacancy = Vacancy(id_num, vacancy_name, company_name, description, float(salary_from),
                              float(salary_to),
                              salary_currency,
                              area, url)
            list_vacancies.append(vacancy)

        return list_vacancies

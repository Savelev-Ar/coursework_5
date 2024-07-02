import psycopg2


class DBManager:
    """
    Класс для работы с базой данных
    """
    def __init__(self, database_name: str, connect_params: dict):
        self.database_name = database_name
        self.connect_params = connect_params

    def __sql_query(self, query, params=None):

        conn = psycopg2.connect(dbname=self.database_name, **self.connect_params)

        with conn.cursor() as cur:
            cur.execute(query, params)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def add_vacancy(self, name, salary_from, salary_to, requirements, url, employer_id):
        query = """
                INSERT INTO vacancy (name, salary_from, salary_to, requirements, url, employer_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING vacancy_id
                """
        self.__sql_query(query, (name, salary_from, salary_to, requirements, url, employer_id))

    def add_employer(self, employer_id, name):
        query = """
                INSERT INTO employer (employer_id, name)
                VALUES (%s, %s)
                RETURNING key
                """
        self.__sql_query(query, (employer_id, name))

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        query = """
                SELECT employer.name, COUNT(vacancy.employer_id)
                FROM employer INNER JOIN vacancy USING (employer_id)
                GROUP BY employer.name
                """
        return self.__sql_query(query)

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        query = """
                SELECT employer.name, vacancy.name, vacancy.salary_from, vacancy.salary_to, vacancy.url
                FROM vacancy INNER JOIN employer USING (employer_id)
                WHERE employer.employer_id = vacancy.employer_id
                """
        return self.__sql_query(query)

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        """
        query = """
                SELECT AVG((salary_from + salary_to)/2)
                FROM vacancy
                """
        return self.__sql_query(query)

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        query = """
                SELECT employer.name, vacancy.name, vacancy.salary_from, vacancy.salary_to, vacancy.url
                FROM vacancy INNER JOIN employer USING (employer_id)
                WHERE (employer.employer_id = vacancy.employer_id)
                    AND (((salary_from + salary_to)/2) > (SELECT AVG((salary_from + salary_to)/2)
                                                          FROM vacancy))
                """
        return self.__sql_query(query)

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        query = f"""
                SELECT employer.name, vacancy.name, vacancy.salary_from, vacancy.salary_to, vacancy.url
                FROM vacancy INNER JOIN employer USING (employer_id)
                WHERE (employer.employer_id = vacancy.employer_id) AND (vacancy.name LIKE '%{keyword}%')
                """
        return self.__sql_query(query)

    def create_db(self):
        """
        Создание базы данных и таблиц для сохранения данных о вакансиях.
        """
        conn = psycopg2.connect(dbname='postgres', **self.connect_params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        conn.close()

        conn = psycopg2.connect(dbname=self.database_name, **self.connect_params)

        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE employer (
                        key SERIAL PRIMARY KEY,
                        employer_id INT UNIQUE NOT NULL,
                        name VARCHAR
                        )
                        """)

        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE vacancy (
                        vacancy_id SERIAL PRIMARY KEY,
                        name VARCHAR,
                        salary_from INT,
                        salary_to INT,
                        requirements text,
                        url VARCHAR,
                        employer_id INT REFERENCES employer(employer_id)
                        )
                        """)

        conn.commit()
        conn.close()

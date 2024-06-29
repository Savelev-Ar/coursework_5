import psycopg2

class DBManager:
    """
    Класс для работы с базой данных
    """
    def __init__(self, database_name: str,  connect_params: dict):
        self.database_name = database_name
        self.connect_params = connect_params

    def __sql_query(self, query, params=None):

        conn = psycopg2.connect(dbname=self.database_name, **self.connect_params)

        with conn.cursor() as cur:
            cur.execute(query, params)
            result = cur.fetchone()[0]
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
        получает список всех компаний и количество вакансий у каждой компании.
        """
        query = """
                SELECT employer.name, COUNT(vacancy.employer_id)
                FROM employer INNER JOIN vacancy USING (employer_id)
                """

        return self.__sql_query(query)

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        pass

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        pass

    def get_vacancies_with_keyword(self):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        pass

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


import psycopg2

class DBManager:
    """
    Класс для работы с базой данных
    """
    def __init__(self, database_name: str,  connect_params: dict):
        self.database_name = database_name
        self.connect_params = connect_params
    def get_companies_and_vacancies_count():
        """
        получает список всех компаний и количество вакансий у каждой компании.
        """
        pass

    def get_all_vacancies():
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        pass

    def get_avg_salary():
        """
        получает среднюю зарплату по вакансиям
        """
        pass

    def get_vacancies_with_higher_salary():
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        pass

    def get_vacancies_with_keyword():
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

        cur.execute(f"DROP DATABASE IS EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")

        conn.close()

        conn = psycopg2.connect(dbname=self.database_name, **self.connect_params)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE channels (
                        channel_id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        views INTEGER,
                        subscribers INTEGER,
                        videos INTEGER,
                        channel_url TEXT
                    )
                """)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE videos (
                        video_id SERIAL PRIMARY KEY,
                        channel_id INT REFERENCES channels(channel_id),
                        title VARCHAR NOT NULL,
                        publish_date DATE,
                        video_url TEXT
                    )
                """)

        conn.commit()
        conn.close()


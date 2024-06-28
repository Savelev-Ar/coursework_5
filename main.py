from src.utils import top_vacancies, filtered_vacancies
from src.vacancy import Vacancies
from src.hh import HHAPI
from config import read_config_db
from src.dbmanager import DBManager as dbman


def main():
    params_db = read_config_db()

    data_base = dbman('vacancy',params_db)
    data_base.create_db



def user_interaction():
    """
    Функция для взаимодействия с пользователем
    """
    search_query = input("Введите поисковый запрос: ")

    # Получение вакансий  по запросу от пользователя
    hh_api = HHAPI()
    hh_api.load_employer_info(search_query)
    for employer in hh_api.employers:
        print(employer)


if __name__ == "__main__":
    main()

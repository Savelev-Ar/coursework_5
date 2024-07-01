from src.utils import top_vacancies, filtered_vacancies
from src.vacancy import Vacancies
from src.hh import HHAPI
from config import read_config_db
from src.dbmanager import DBManager as dbman


def main():
    params_db = read_config_db()

    data_base = dbman('vacancy', params_db)
    data_base.create_db()



    for emp_id in [{'employer_id': '1905607', 'employer_name': 'Завод металлических изделий'},
                   {'employer_id': '1480111', 'employer_name': 'Соликамскбумпром'},
                   {'employer_id': '2639424', 'employer_name': 'Соликамский завод Урал'},
                   {'employer_id': '9029510', 'employer_name': 'Телекомпания Соль-ТВ'},
                   {'employer_id': '3796539', 'employer_name': 'Уральский завод ОСБ'},
                   {'employer_id': '104628',  'employer_name': 'Газпром'},
                   {'employer_id': '80',  'employer_name': 'Альфа-Банк'},
                   {'employer_id': '3529',  'employer_name': 'СБЕР'},
                   {'employer_id': '565840',  'employer_name': 'Сбербанк АСТ'},
                   {'employer_id': '4827957',  'employer_name': 'ФКУ СИЗО-6 ГУФСИН России по Пермскому краю'},
                   {'employer_id': '3734593',  'employer_name': 'ФКУ Центр инженерно-технического обеспечения и вооружения ГУФСИН России по Пермскому краю'}
                   ]:
        hh_api = HHAPI()
        hh_api.load_vacancies_from_employer(emp_id['employer_id'])
        vacancies_list = Vacancies.add_vacancies(hh_api.vacancies)
        data_base.add_employer(emp_id['employer_id'], emp_id['employer_name'])
        for vacancy in vacancies_list:
            data_base.add_vacancy(vacancy.name, vacancy.salary_from, vacancy.salary_to, vacancy.requirements, vacancy.url, emp_id['employer_id'])

    print(data_base.get_companies_and_vacancies_count())
    print_list = data_base.get_all_vacancies()
    for line in print_list:
        print(line)



if __name__ == "__main__":
    main()

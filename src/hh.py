from abc import ABC, abstractmethod
import requests


class JobsParser(ABC):

    @abstractmethod
    def load_vacancies(self, keyword):
        pass


class HHAPI(JobsParser):
    """
    Класс для работы с API HeadHunter
    """
    def __init__(self):
            self.url_vacancies = 'https://api.hh.ru/vacancies'
            self.url_employers = 'https://api.hh.ru/employers'
            self.headers = {'User-Agent': 'HH-User-Agent'}
            self.params = {'text': '', 'page': 0,
                           'per_page': 100,
                           }
            self.vacancies = []
            self.employers = []

    def load_vacancies(self, keyword):
        self.params['schedule'] = 'remote'
        self.params['only_with_salary'] = True
        self.params['currency'] = 'RUR'
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url_vacancies, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1

    def load_employer_info(self, keyword):
        self.params['text'] = keyword
        self.params['locale'] = 'RU'
        self.params['area'] = '113'  # "113" - Россия, "1317" - Пермский край ,  "1335" - Соликамск Пермского края
        self.params['only_with_vacancies'] = True
        while self.params.get('page') != 50:
            response = requests.get(self.url_employers, headers=self.headers, params=self.params)
            employers = response.json()['items']
            self.employers.extend(employers)
            self.params['page'] += 1

    def load_vacancies_from_employer(self, id_employer):
        self.params['only_with_salary'] = True
        self.params['currency'] = 'RUR'
        self.params['employer_id'] = id_employer
        while self.params.get('page') != 20:
            response = requests.get(self.url_vacancies, headers=self.headers, params=self.params)
            try:
                vacancies = response.json()['items']
                self.vacancies.extend(vacancies)
            except:
                pass
            self.params['page'] += 1

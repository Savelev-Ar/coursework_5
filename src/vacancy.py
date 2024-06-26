class Vacancies:

    def __init__(self, name, salary_from, salary_to, requirements, url):
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.requirements = requirements
        self.url = url

    @classmethod
    def add_vacancies(cls, vacancies_list):
        result = []
        for vacancy in vacancies_list:
            if vacancy.get('salary')['from'] is not None:
                salary_from = int(vacancy.get('salary')['from'])
            else:
                salary_from = 0
            if vacancy.get('salary')['to'] is not None:
                salary_to = int(vacancy.get('salary')['to'])
            else:
                salary_to = 0
            if vacancy.get('snippet').get('requirement') is not None:
                requirement = vacancy.get('snippet').get('requirement').replace('<highlighttext>','').replace('</highlighttext>','')
            result.append(Vacancies(vacancy.get('name'), salary_from, salary_to,
                                    requirement,
                                    vacancy.get('alternate_url')))
        return result

    def __lt__(self, other):
        if self.salary_from != 0 or other.salary_from != 0:
            return self.salary_from < other.salary_from
        else:
            return self.salary_to < other.salary_to
    def __repr__(self):
        return (f'Вакансия : {self.name} ,'
                f' зарплата: от {self.salary_from} до {self.salary_to},'
                f' ссылка : {self.url} ,'
                f' требования : {self.requirements} \n')

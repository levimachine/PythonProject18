from requests import get
from abc import ABC, abstractmethod


class API(ABC):
    @abstractmethod
    def get_vacancies(self, text: str):
        pass


class HeadHunterAPI(API):
    """Класс по работе с HH API"""

    def get_vacancies(self, text: str):
        """Метод get_vacancies позволяет получить все вакансии(не больше 2000) по заданному тексту.
        :param text: Текст для поиска."""
        vacancies_list = []
        vacancies_quantity = get(f"https://api.hh.ru/vacancies?text={text}&only_with_salary=true&area=113").json()[
            'found']  # Общее количество вакансий
        for page_number in range(vacancies_quantity // 100 + 1):
            # Ставим стоппер, иначе программа "упадёт", потому что можем получить только 2000 вакансий.
            if len(vacancies_list) == 2000:
                break
            # Обходим каждую страницу по 100 вакансий, per_page не может быть больше 100, page начинается с 0.
            vacancies = get(
                f"https://api.hh.ru/vacancies?text={text}&only_with_salary=true&area=113&page={page_number}&per_page=100").json()[
                'items']
            for vacancy in vacancies:
                salary = None
                average_salary = None  # Средняя между "от" и "до", для сортировки.
                if vacancy['salary'] is None:
                    continue
                if vacancy['salary']['from'] and vacancy['salary']['to']:
                    salary = f'от {vacancy['salary']['from']} до {vacancy['salary']['to']} руб.'
                    average_salary = int((vacancy['salary']['from'] + vacancy['salary']['to']) / 2)
                elif vacancy['salary']['to'] is None:
                    salary = f"{vacancy['salary']['from']} руб."
                    average_salary = vacancy['salary']['from']
                elif vacancy['salary']['from'] is None:
                    salary = f"{vacancy['salary']['to']} руб."
                    average_salary = vacancy['salary']['to']
                vacancies_list.append({
                    'name': vacancy['name'],
                    'url': vacancy['alternate_url'],
                    'city': vacancy['area']['name'],
                    'created_date': f'{vacancy['created_at'][8:10]}.{vacancy['created_at'][5:7]}.{vacancy['created_at'][0:4]}',
                    'employer_url': vacancy['employer'].get('alternate_url'),
                    'salary': salary,
                    'average_salary': average_salary
                })

        return vacancies_list

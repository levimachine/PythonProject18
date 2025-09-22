from requests import get
from abc import ABC, abstractmethod
from vacancy_class import Vacancy
from datetime import datetime



class API(ABC):
    """
    Абстрактный класс API.

    Определяет интерфейс для работы с API сервисов поиска вакансий.
    Классы-наследники обязаны реализовать метод `get_vacancies`.
    """
    @abstractmethod
    def get_vacancies(self, text: str):
        """
        Метод для получения вакансий по ключевому слову.

        :param text: Строка поиска (ключевое слово или фраза).
        :return: Список вакансий или иной результат, определённый в реализации.
        """
        pass


class HeadHunterAPI(API):
    """
    Класс для работы с API HeadHunter (https://api.hh.ru).

    Позволяет выполнять поиск вакансий по ключевым словам, парсит результат
    и возвращает список объектов класса Vacancy.
    """

    @classmethod
    def _get_salary(cls, vacancy_salary: dict) -> tuple:
        """
        Приватный метод для извлечения зарплаты и расчёта средней зарплаты из данных вакансии.

        :param vacancy_salary: Словарь с ключами "from" и "to", содержащий диапазон зарплаты.
        :return: Кортеж (salary, average_salary):
            - salary (str): Читабельная строка с зарплатой (например, "от 100000 до 150000 руб.").
            - average_salary (int | list[int, int]): Средняя зарплата или диапазон зарплаты для сортировки.
         """
        salary = None
        average_salary = None
        salary_from = vacancy_salary['from']
        salary_to = vacancy_salary['to']

        if salary_from and salary_to:
            salary = f'от {salary_from} до {salary_to} руб.'
            average_salary = [salary_from, salary_to]
        elif salary_from:
            salary = f"{salary_from} руб."
            average_salary = salary_from
        elif salary_to:
            salary = f"{salary_to} руб."
            average_salary = salary_to

        return salary, average_salary

    @classmethod
    def _get_api_info(cls, text: str, page_number: int = None):
        """
       Приватный метод для выполнения запроса к HH API.

       :param text: Строка поиска (ключевое слово или фраза).
       :param page_number: Номер страницы для пагинации (начиная с 0).
       :return: Кортеж (vacancies_quantity, response_information):
           - vacancies_quantity (int): Общее количество вакансий, найденных по запросу.
           - response_information (list[dict]): Список словарей с информацией о вакансиях на текущей странице.
       :raises RuntimeError: Если ответ API не равен 200 (ошибка подключения или некорректный запрос).
       """
        response = get(
            f"https://api.hh.ru/vacancies?text={text}&only_with_salary=true&area=113&page={page_number}&per_page=100")
        if response.status_code != 200:
            raise RuntimeError('Не удаётся подключиться к HH API!')
        else:
            vacancies_quantity = response.json()['found']
            response_information = response.json()['items']

        return vacancies_quantity, response_information

    def get_vacancies(self, text: str):
        """
        Основной метод для получения вакансий по заданному ключевому слову.

        Метод обходит страницы API (максимум 2000 вакансий, по 100 на страницу),
        извлекает данные, преобразует их в объекты Vacancy и возвращает список.

        :param text: Строка поиска (ключевое слово или фраза).
        :return: Список экземпляров класса Vacancy.
        """
        vacancies_list = []
        vacancies_quantity = self._get_api_info(text, 0)  # Общее количество вакансий
        for page_number in range(vacancies_quantity[0] // 100 + 1):
            # Ставим стоппер, иначе программа "упадёт", потому что можем получить только 2000 вакансий.
            if len(vacancies_list) == 2000:
                break
            # Обходим каждую страницу по 100 вакансий, per_page не может быть больше 100, page начинается с 0.
            vacancies = self._get_api_info(text, page_number)[1]
            for vacancy in vacancies:
                date = datetime.strptime(vacancy['created_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y')
                if vacancy['salary'] is None:
                    continue

                salary, average_salary = self._get_salary(vacancy['salary'])

                vacancies_list.append(Vacancy(name=vacancy['name'],
                                              url=vacancy['alternate_url'],
                                              salary=salary,
                                              average_salary=average_salary,
                                              created_date=date,
                                              city=vacancy['area']['name'],
                                              employer_url=vacancy['employer'].get('alternate_url')))
        return vacancies_list

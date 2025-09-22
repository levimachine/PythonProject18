from abc import abstractmethod, ABC
from vacancy_class import Vacancy
from json import dump, load


class Saver(ABC):
    """
    Класс Saver - абстрактный класс, который задаёт шаблон для создания новых классов.
    Обязательные методы для реализации:
    - add_vacancy
    - get_vacancy_by_salary
    -delete_vacancy
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Метод добавляет вакансию в json-файл в формате url:{info}.
        :param vacancy: Экземпляр класса Vacancy.
        :return:  None.
        """
        pass

    @abstractmethod
    def get_vacancy_by_salary(self, salary: int | float) -> dict | str:
        """
        Метод получает словарь вакансий, сортировка происходит по заданному значению salary(нижняя граница).
        :param salary: Нижняя граница зарплаты, по которой будет проходить сортировка.
        :return: Возвращает словарь с вакансиями, если подходящих вакансий нет - вернёт строку "Вакансий с зп от {salary} не найдено".
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Метод удаляет вакансию из json-файла.
        :param vacancy: Экземпляр класса Vacancy, который будет удалять.
        :return: None.
        """
        pass


class JSONSaver(Saver):
    """
    Класс JSONSaver - класс для получения, удаления и поиска вакансий по заданной зарплате.
    Наследуется от класса шаблона Saver.
    """
    _FILE_NAME = 'vacancies.json'

    @classmethod
    def _read_json(cls) -> dict:
        """
        Класс метод считывает файл vacancies.json и возвращает словарь с вакансиями.
        Файл vacancies.json храним локально, в нём уже есть словарь.
        :return: Словарь с вакансиями.
        """
        with open(cls._FILE_NAME, mode='r', encoding='utf-8') as f:
            data = load(f)
        return data

    @classmethod
    def _write_json(cls, data: dict) -> None:
        """
        Класс метод записывает словарь в json файл.
        :param data: Словарь с вакансиями.
        :return: None.
        """
        with open(cls._FILE_NAME, mode='w', encoding='utf-8') as f:
            dump(data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Метод добавляет вакансию в json-файл в формате url:{info}.
        :param vacancy: Экземпляр класса Vacancy.
        :return:  None.
        """
        json_dict_with_vacancies: dict = self._read_json()
        json_dict_with_vacancies.update({str(vacancy.url): vacancy.model_dump(exclude={'url'}, mode='json')})
        self._write_json(json_dict_with_vacancies)

    def add_list_with_vacancies(self, vacancies_list: list[Vacancy]) -> None:
        """
        Метод добавляет список вакансий в json-файл в формате url:{info}.
        :param vacancies_list: Список экземпляров класса Vacancy.
        :return: None.
        """
        json_dict_with_vacancies: dict = self._read_json()
        for vacancy in vacancies_list:
            json_dict_with_vacancies.update({str(vacancy.url): vacancy.model_dump(exclude={'url'}, mode='json')})
        self._write_json(json_dict_with_vacancies)

    def get_vacancy_by_salary(self, salary: int | float) -> list | str:
        """
        Метод получает словарь вакансий, сортировка происходит по заданному значению salary(нижняя граница).
        :param salary: Нижняя граница зарплаты, по которой будет проходить сортировка.
        :return: Возвращает словарь с вакансиями, если подходящих вакансий нет - вернёт строку "Вакансий с зп от {salary} не найдено".
        """
        list_with_vacancies: list = []
        json_dict_with_vacancies: dict = self._read_json()
        for url, information in json_dict_with_vacancies.items():
            if isinstance(information['average_salary'], list) and salary <= information['average_salary'][1]:
                list_with_vacancies.append(Vacancy(name=information['name'],
                                                   url=url,
                                                   employer_url=information['employer_url'],
                                                   salary=information['salary'],
                                                   average_salary=information['average_salary'],
                                                   created_date=information['created_date'],
                                                   city=information['city']
                                                   ))
            elif isinstance(information['average_salary'], (int, float)) and salary <= information['average_salary']:
                list_with_vacancies.append(Vacancy(name=information['name'],
                                                   url=url,
                                                   employer_url=information['employer_url'],
                                                   salary=information['salary'],
                                                   average_salary=information['average_salary'],
                                                   created_date=information['created_date'],
                                                   city=information['city']
                                                   ))
        if list_with_vacancies:
            return list_with_vacancies
        return f'Вакансий с зп от {salary} не найдено.'

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Метод удаляет вакансию из json-файла.
        :param vacancy: Экземпляр класса Vacancy, который будет удалять.
        :return: None.
        """
        json_dict_with_vacancies: dict = self._read_json()
        try:
            json_dict_with_vacancies[str(vacancy.url)]
        except KeyError:
            print('Такой вакансии не существует!')
        else:
            del json_dict_with_vacancies[str(vacancy.url)]
        self._write_json(json_dict_with_vacancies)

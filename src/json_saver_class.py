from abc import abstractmethod, ABC
from vacancy_class import Vacancy
from json import dump, load


class Saver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancy_by_salary(self, salary: str) -> dict | str:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass


class JSONSaver:
    _FILE_NAME = 'vacancies.json'

    @classmethod
    def _read_json(cls) -> dict:
        with open(cls._FILE_NAME, mode='r', encoding='utf-8') as f:
            data = load(f)
        return data

    @classmethod
    def _write_json(cls, data: dict) -> None:
        with open(cls._FILE_NAME, mode='w', encoding='utf-8') as f:
            dump(data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        json_dict_with_vacancies: dict = self._read_json()
        json_dict_with_vacancies.update(vacancy.get_class_by_dict())
        self._write_json(json_dict_with_vacancies)

    def get_vacancy_by_salary(self, salary: int | float) -> dict | str:
        dict_with_vacancies: dict = {}
        json_dict_with_vacancies: dict = self._read_json()
        for name, information in json_dict_with_vacancies.items():
            if isinstance(information['average_salary'], list) and salary <= information['average_salary'][1]:
                dict_with_vacancies.setdefault(name, information)
            elif salary <= information['average_salary']:
                dict_with_vacancies.setdefault(name, information)
        if dict_with_vacancies:
            return dict_with_vacancies
        return f'Вакансий с зп от {salary} не найдено.'

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        json_dict_with_vacancies: dict = self._read_json()
        try:
            json_dict_with_vacancies[vacancy.url]
        except KeyError:
            print('Такой вакансии не существует!')
        else:
            del json_dict_with_vacancies[vacancy.url]
        self._write_json(json_dict_with_vacancies)

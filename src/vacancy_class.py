from pydantic import BaseModel, HttpUrl


class Vacancy(BaseModel):
    """
    Класс Vacancy — модель данных вакансии с валидацией полей на основе pydantic.

    Атрибуты:
        name (str): Название вакансии.
        salary (str): Читаемая строка с зарплатой (в формате "от 100000 до 150000 руб.").
        average_salary (int | list[int]): Средняя зарплата или диапазон зарплат для сравнения.
        city (str): Город, в котором размещена вакансия.
        url (HttpUrl): Ссылка на вакансию.
        created_date (str): Дата создания вакансии (в формате "16.09.2025").
        employer_url (str | None): Ссылка на страницу работодателя (может быть None).

    Возможности:
    - Поддерживает сравнение (`==`, `!=`, `<`, `<=`, `>`, `>=`) на основе поля average_salary.
    - Предоставляет читаемое строковое представление вакансии.
    - Умеет красиво выводить данные для пользователя с помощью метода show_vacancy_for_user().
    """
    name: str
    salary: str
    average_salary: int | list[int]
    city: str
    url: HttpUrl
    created_date: str
    employer_url: str | None

    def __str__(self):
        return f"{self.name}, {self.salary}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.created_date}, {self.city}, {self.salary}, {self.average_salary}, {self.url}, {self.employer_url})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError('Класс Vacancy можно сравнивать только с его экземплярами!')
        return self.average_salary == other.average_salary

    def __gt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError('Класс Vacancy можно сравнивать только с его экземплярами!')
        return self.average_salary > other.average_salary

    def __ge__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError('Класс Vacancy можно сравнивать только с его экземплярами!')
        return self.average_salary >= other.average_salary

    def __lt__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError('Класс Vacancy можно сравнивать только с его экземплярами!')
        return self.average_salary < other.average_salary

    def __le__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError('Класс Vacancy можно сравнивать только с его экземплярами!')
        return self.average_salary <= other.average_salary

    def __ne__(self, other) -> bool:
        if not isinstance(other, Vacancy):
            raise TypeError('Класс Vacancy можно сравнивать только с его экземплярами!')
        return self.average_salary != other.average_salary

    def show_vacancy_for_user(self):
        """
        Форматирует информацию о вакансии в удобный для пользователя вид.

        :return: Многострочная строка с подробной информацией о вакансии:
            - название
            - дата создания
            - ссылка на вакансию
            - город
            - зарплата
            - ссылка на работодателя
        """
        return f"""{self.name}
Дата создания: {self.created_date}
Ссылка на вакансию: {self.url}
Город: {self.city}
Зарплата: {self.salary}
Ссылка на работодателя: {self.employer_url}
"""

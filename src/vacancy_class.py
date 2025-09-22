from pydantic import BaseModel, HttpUrl
from datetime import datetime


class Vacancy(BaseModel):
    name: str
    salary: str
    average_salary: int | list[int]
    city: str
    url: HttpUrl
    created_date: datetime
    employer_url: HttpUrl

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

from pydantic import BaseModel, HttpUrl


class VacancySchema(BaseModel):
    name: str
    salary: str
    average_salary: int | tuple[int, int]
    city: str
    url: HttpUrl
    created_date: str
    employer_url: HttpUrl


class Vacancy:
    def __init__(self, name: str, salary: str, average_salary: int | tuple[int, int], city: str, url: HttpUrl,
                 created_date: str,
                 employer_url: HttpUrl):
        VacancySchema(name=name, salary=salary, average_salary=average_salary, city=city, url=url,
                      created_date=created_date, employer_url=employer_url)
        self.__name = name
        self.__salary = salary
        self.__average_salary = average_salary
        self.__city = city
        self.__url = url
        self.__created_date = created_date
        self.__employer_url = employer_url

    def __str__(self):
        return f"{self.__name}, {self.__salary}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__name}, {self.__created_date}, {self.__city}, {self.__salary}, {self.__average_salary}, {self.__url}, {self.__employer_url})"

    def __eq__(self, other):
        return self.__average_salary == other.__average_salary

    def __gt__(self, other):
        return self.__average_salary > other.__average_salary

    def __ge__(self, other):
        return self.__average_salary >= other.__average_salary

    def __lt__(self, other):
        return self.__average_salary < other.__average_salary

    def __le__(self, other):
        return self.__average_salary <= other.__average_salary

    def __ne__(self, other):
        return self.__average_salary != other.__average_salary

    @property
    def url(self):
        return self.__url

    def get_class_by_dict(self):
        """Метод возвращает словарь, key которого является название вакансии, а value - все данные о ней"""
        return {
            f'{self.__url}': {
                'salary': self.__salary,
                'average_salary': self.__average_salary,
                'city': self.__city,
                'name': self.__name,
                'created_date': self.__created_date,
                'employer_url': self.__employer_url
            }
        }

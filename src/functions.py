from api_class import HeadHunterAPI
from json_saver_class import JSONSaver
from pprint import  pprint
def start_program():
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()
    name = input('Введите ваше имя: ')
    message_1 = input(f'{name.capitalize()}, добро пожаловать в приложения для поиска работы!\n'
                            f'Здесь я помогу найти тебе работу на платформе HH.ru\n'
                            f'Введи свой запрос а я попытаюсь что-то для тебя найти: ')
    list_with_vacancies = hh_api.get_vacancies(message_1)
    vacancies_quantity = len(list_with_vacancies)
    json_saver.add_list_with_vacancies(list_with_vacancies)
    message_2 = int(input(f'По вашему запросу найдено {vacancies_quantity} вакансий!\n'
                      f'Введите ожидаемую зарплату: '))
    pprint(json_saver.get_vacancy_by_salary(message_2))

start_program()


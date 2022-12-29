from prettytable import PrettyTable
from prettytable import ALL
import csv
import re
import os

invert_dic = lambda dic: {v: k for k, v in dic.items()}

# Словарь перевода английских названий заголовков в русские
dic_naming = {
    'name': 'Название',
    'description': 'Описание',
    'key_skills': 'Навыки',
    'experience_id': 'Опыт работы',
    'premium': 'Премиум-вакансия',
    'employer_name': 'Компания',
    'salary': 'Оклад',
    'salary_from': 'Нижняя граница вилки оклада',
    'salary_to': 'Верхняя граница вилки оклада',
    'salary_gross': 'Оклад указан до вычета налогов',
    'salary_currency': 'Идентификатор валюты оклада',
    'area_name': 'Название региона',
    'published_at': 'Дата публикации вакансии'
}

# Словарь перевода английских логических значений в русские
dic_bool = {
    'True': 'Да',
    'TRUE': 'Да',
    'False': 'Нет',
    'FALSE': 'Нет'
}

# Словарь перевода английских указателей опыта работы в русские
dic_work_experience = {
    'noExperience': 'Нет опыта',
    'between1And3': 'От 1 года до 3 лет',
    'between3And6': 'От 3 до 6 лет',
    'moreThan6': 'Более 6 лет'
}

# Словарь сортировки указателей опыта работы
work_experience_sort = {
    'Нет опыта': 0,
    'От 1 года до 3 лет': 1,
    'От 3 до 6 лет': 2,
    'Более 6 лет': 3
}

# Словарь перевода кода валюты в полное название
dic_currency = {
    'AZN': 'Манаты',
    'BYR': 'Белорусские рубли',
    'EUR': 'Евро',
    'GEL': 'Грузинский лари',
    'KGS': 'Киргизский сом',
    'KZT': 'Тенге',
    'RUR': 'Рубли',
    'UAH': 'Гривны',
    'USD': 'Доллары',
    'UZS': 'Узбекский сум'
}

# Cловарь коэффицентов конвертации валют в рубли
currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055
}

# Словарь функций фильтрации для парметров вакансии
dic_filters = {
    'Название': lambda x, y: x == y,
    'Описание': lambda x, y: x == y,
    'Навыки': lambda x, y: all(t in x for t in y),
    'Опыт работы': lambda x, y: x == y,
    'Премиум-вакансия': lambda x, y: x == y,
    'Компания': lambda x, y: x == y,
    'Оклад': lambda salary_from, salary_to, x: salary_from <= x <= salary_to,
    'Оклад указан до вычета налогов': lambda x, y: x == y,
    'Идентификатор валюты оклада': lambda x, y: x == y,
    'Название региона': lambda x, y: x == y,
    'Дата публикации вакансии': lambda yi, mi, di, dt, mt, yt: di == dt and mi == mt and yi == yt
}

# Словарь функций сортировки для параметров вакансии
dic_sorters = {
    'Навыки': lambda x: len(x.full_dict['key_skills'].split('\n')),
    'Опыт работы': lambda x: work_experience_sort[dic_work_experience[x.full_dict['experience_id']]],
    'Оклад': lambda x: x.full_dict['salary'].converter(),
    'Дата публикации вакансии': lambda x: int(
       x.full_dict['published_at'][:4] + x.full_dict['published_at'][5:7] +
       x.full_dict['published_at'][8:10] + x.full_dict['published_at'][11:13] +
       x.full_dict['published_at'][14:16] + x.full_dict['published_at'][17:19])
}


def check_filter_value(filter_opt):
    """
    Проверяет значение параметра фильтрации на соответствие требованиям
    Args:
        filter_opt (str): Значение параматра фильтрации

    Returns:
        str or bool: Найденная ошибка или False, если введенный параметр выполняет требования

    >>> check_filter_value('Название')
    'Формат ввода некорректен'
    >>> check_filter_value('НеверныйЗаголовок')
    'Формат ввода некорректен'
    >>> check_filter_value('Название: 1С-программист')
    False
    >>> check_filter_value('Неверный заголовок: 1С-программист')
    'Параметр поиска некорректен'
    >>> check_filter_value('Опыт работы: Без опыта')
    False
    """
    if filter_opt != '':
        if ':' not in filter_opt:
            return "Формат ввода некорректен"
        elif filter_opt.split(': ')[0] not in dic_naming.values():
            return "Параметр поиска некорректен"
    return False


def check_sorter_value(sorter):
    """
    Проверяет значение параметра сортировки на соответствие требованиям
    Args:
        sorter (str): Значение параматра сортировки

    Returns:
        str or bool: Найденная ошибка или False, если введенный параметр выполняет требования

    >>> check_sorter_value('Название')
    False
    >>> check_sorter_value('')
    False
    >>> check_sorter_value('НеверныйЗаголовок')
    'Параметр сортировки некорректен'
    """
    if sorter != '' and sorter not in dic_naming.values():
        return "Параметр сортировки некорректен"
    return False


def check_reverse_value(reverse_sort):
    """
    Проверяет значение параметра обратной сортировки на соответствие требованиям
    Args:
        reverse_sort (str): Значение параматра обратной сортировки

    Returns:
        str or bool: Найденная ошибка или False, если введенный параметр выполняет требования

    >>> check_reverse_value('Да')
    False
    >>> check_reverse_value('')
    False
    >>> check_reverse_value('НеверноеЗначение')
    'Порядок сортировки задан некорректно'
    """
    if reverse_sort != '' and reverse_sort not in ['Да', 'Нет']:
        return "Порядок сортировки задан некорректно"
    return False


def formatter(row, key):
    """
    Форматирует строковое значение параметра вакансии в соответствии с правилами для каждого столбца
    Args:
        row(str): Строковое значение параметра вакансии
        key(str): Указатель названия столбца, к которому относится строковое значение

    Returns:
        str: Отформатированное строковое значение параметра вакансии
        
    >>> formatter('  Программист 1С'   , 'name')
    'Программист 1С'
    >>> formatter('<p>Описание Вакансии</p>', 'description')
    'Описание Вакансии'
    >>> formatter('between1And3', 'experience_id')
    'От 1 года до 3 лет'
    >>> formatter('FALSE', 'premium')
    'Нет'
    >>> formatter('2022-07-05T18:31:44+0300', 'published_at')
    '05.07.2022'
    """

    shrink_long_row = lambda string: string[:100] + '...' if len(string) > 100 else string
    if key == 'name':
        row.strip()
        row = ' '.join(row.split())
    elif key == 'description':
        regex = re.compile(r'<[^>]+>')
        row = regex.sub('', row)
        row.strip()
        row = ' '.join(row.split())
    elif key == 'key_skills':
        skills_list = row.split('\n')
        row = '\n'.join(skills_list)
    elif key == 'experience_id':
        row.strip()
        row = dic_work_experience[row]
    elif key == 'premium':
        row.strip()
        row = dic_bool[row]
    elif key == 'salary':
        salary_from = str(round(float(row.salary_from)))[::-1]
        salary_from = ' '.join(salary_from[i:i + 3] for i in range(0, len(salary_from), 3))[::-1]
        salary_to = str(round(float(row.salary_to)))[::-1]
        salary_to = ' '.join(salary_to[i:i + 3] for i in range(0, len(salary_to), 3))[::-1]
        salary_gross = '(Без вычета налогов)' if dic_bool[row.salary_gross] == 'Да' else '(С вычетом налогов)'
        row = f"{salary_from} - {salary_to} ({dic_currency[row.salary_currency]}) {salary_gross}"
    elif key == 'published_at':
        day = row[8:10]
        month = row[5:7]
        year = row[:4]
        row = day + "." + month + "." + year

    row = shrink_long_row(row)
    return row


class Salary(object):
    """
    Класс для представления зарплаты
    Attributes:
        salary_from (int or float): Нижняя граница вилки оклада
        salary_to (int or float): Верхняя граница вилки оклада
        salary_gross (str): Указатель размера оклада с учетом налогов
        salary_currency (str): Валюта оклада
        salary_to_print (str): Отформатированная строка зарплаты для печати
    """
    def __init__(self, salary_f, salary_t, salary_g, salary_c):
        """
        Инициализирует объект Salary
        Args:
            salary_f (int or float): Нижняя граница вилки оклада
            salary_t (int or float): Верхняя граница вилки оклада
            salary_g (str): Указатель размера оклада с учетом налогов
            salary_c (str): Валюта оклада

        >>> type(Salary(10.0, 20.4, 'False', 'RUR')).__name__
        'Salary'
        >>> type(Salary(100, 200, 'False', 'EUR')).__name__
        'Salary'
        >>> Salary(10.0, 20.4, 'False', 'RUR').salary_from
        10.0
        >>> Salary(10.0, 20.4, 'False', 'RUR').salary_to
        20.4
        >>> Salary(10.0, 20.4, 'False', 'RUR').salary_currency
        'RUR'
        >>> Salary(10.0, 20.4, 'False', 'RUR').salary_gross
        'False'
        """
        self.salary_from = salary_f
        self.salary_to = salary_t
        self.salary_gross = salary_g
        self.salary_currency = salary_c
        self.salary_to_print = formatter(self, 'salary')

    def converter(self):
        """
        Конвертирует значение зарплаты в валюте в рубли
        Returns: int: Конвертированное значение зарплаты в рублях

        >>> Salary(10, 20, 'False', 'RUR').converter()
        15
        >>> Salary(10, 20, 'False', 'EUR').converter()
        898
        >>> Salary(10, 20, 'False', 'RUR').converter()
        15
        >>> Salary(10.0, 20.0, 'False', 'RUR').converter()
        15
        >>> Salary(10.0, 20.0, 'False', 'EUR').converter()
        898
        >>> Salary(10.0, 20.0, 'False', 'RUR').converter()
        15
        """
        return int(round(currency_to_rub[self.salary_currency] *
                         (int(float(self.salary_from) + (int(float(self.salary_to))))) / 2))


class Vacancy(object):
    """
    Класс для представления вакансии

    Attributes:
        full_dict (dict): Полный словарь из названий парметров и значений параметров
        name (str): Название вакансии
        salary (Salary object): Зарплата
        area_name (str): Название региона
        published_at (str): Дата публикации вакансии
        description (str): Описание вакансии
        key_skills (list of str): Список необходимых навыков
        premium (str): Указатель премиум-вакансии
        employer_name (str): Название компании работодателя
        experience_id (str): Опыт работы
    """
    def __init__(self, vacancy_row):
        r"""
        Инициализирует объект Vacancy
        Args:
            vacancy_row(list of str or int): Список параметров вакансии

        >>> type(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300'])).__name__
        'Vacancy'
        >>> Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'True', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).name
        'Оператор сервисного центра'
        >>> Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).description
        'Необходимо отвечать на звонки клиентов и решать их проблемы'
        >>> Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).key_skills
        'Ответственность\nКоммуникабельность'
        >>> Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'True', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).experience_id
        'Нет опыта'
        >>> Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).premium
        'Нет'
        >>> Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).employer_name
        'ОАО "Информационные технологии"'
        >>> type(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).salary)
        <class 'str'>
        >>> Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).area_name
        'Екатеринбург'
        >>> Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).published_at
        '15.07.2022'
        """
        self.full_dict = dict({
            'name': vacancy_row[0],
            'description': vacancy_row[1],
            'key_skills': vacancy_row[2],
            'experience_id': vacancy_row[3],
            'premium': vacancy_row[4],
            'employer_name': vacancy_row[5],
            'salary': Salary(vacancy_row[6], vacancy_row[7], vacancy_row[8], vacancy_row[9]),
            'salary_from': vacancy_row[6],
            'salary_to': vacancy_row[7],
            'salary_gross': vacancy_row[8],
            'salary_currency': vacancy_row[9],
            'area_name': vacancy_row[10],
            'published_at': vacancy_row[11]})

        self.name = formatter(vacancy_row[0], 'name')
        self.description = formatter(vacancy_row[1], 'description')
        self.key_skills = formatter(vacancy_row[2], 'key_skills')
        self.experience_id = formatter(vacancy_row[3], 'experience_id')
        self.premium = formatter(vacancy_row[4], 'premium')
        self.employer_name = formatter(vacancy_row[5], 'employer_name')
        self.salary = Salary(vacancy_row[6], vacancy_row[7], vacancy_row[8], vacancy_row[9]).salary_to_print
        self.area_name = formatter(vacancy_row[10], 'area_name')
        self.published_at = formatter(vacancy_row[11], 'published_at')


class DataSet(object):
    """
    Класс для представления датасета

    Attributes:
        vacancies (list of Vacancy objects): Список вакансий датасета
    """
    def __init__(self, file_path):
        """
        Инициализирует объект датасета
        Args:
            file_path (str): Путь к csv-файлу с данными о вакансиях

        >>> type(DataSet('vacancies.csv')).__name__
        'DataSet'
        """
        vacancies = []
        vacancies_objs = []
        with open(file_path, encoding="utf-8-sig") as File:
            if os.stat(file_path).st_size == 0:
                self.vacancies = 'Пустой файл'
            else:
                reader = csv.reader(File, delimiter=',', quotechar='"')
                for vacancy in reader:
                    if all(vacancy):
                        vacancies.append(vacancy)
                        if len(vacancy) < len(vacancies[0]):
                            vacancies.remove(vacancy)

            if len(vacancies) == 1:
                self.vacancies = 'Нет данных'
            elif len(vacancies) != 0:
                columns_names.extend([dic_naming[x] for x in vacancies[0]])
                for vacancy in vacancies[1::]:
                    vacancies_objs.append(Vacancy(vacancy))
                self.vacancies = vacancies_objs

    def filter_data(self, filter_opt):
        """
        Фильтрует список вакансий по заданному условию
        Args:
            filter_opt(str): Значение параметра фильтрации
        """
        filter_key = filter_opt.split(': ')[0]
        filter_value = filter_opt.split(': ')[1]
        if filter_key == 'Оклад':
            self.vacancies = list(
                filter(lambda x:
                       dic_filters[filter_key]
                       (int(x.full_dict['salary_from']),
                        int(x.full_dict['salary_to']),
                        int(filter_value)),
                       self.vacancies))
        elif filter_key == 'Дата публикации вакансии':
            self.vacancies = list(
                filter(lambda x:
                       dic_filters[filter_key]
                       (x.full_dict['published_at'][:4],
                        x.full_dict['published_at'][5:7],
                        x.full_dict['published_at'][8:10],
                        filter_value[:2],
                        filter_value[3:5],
                        filter_value[6:10]),
                       self.vacancies))
        elif filter_key == 'Опыт работы':
            self.vacancies = list(
                filter(lambda x:
                       dic_filters[filter_key]
                       (dic_work_experience[x.full_dict[invert_dic(dic_naming)[filter_key]]].split('\n'),
                        filter_value.split(', ')),
                       self.vacancies))
        elif filter_key in ['Опыт работы', 'Премиум-вакансия']:
            self.vacancies = list(
                filter(lambda x:
                       dic_filters[filter_key]
                       (dic_bool[x.full_dict[invert_dic(dic_naming)[filter_key]]].split('\n'),
                        filter_value.split(', ')),
                       self.vacancies))
        elif filter_key in ['Идентификатор валюты оклада']:
            self.vacancies = list(
                filter(lambda x:
                       dic_filters[filter_key]
                       (dic_currency[x.full_dict[invert_dic(dic_naming)[filter_key]]].split('\n'),
                        filter_value.split(', ')),
                       self.vacancies))
        else:
            self.vacancies = list(
                filter(lambda x:
                       dic_filters[filter_key]
                       (x.full_dict[invert_dic(dic_naming)[filter_key]].split('\n'),
                        filter_value.split(', ')),
                       self.vacancies))
        if len(self.vacancies) == 0:
            self.vacancies = 'Ничего не найдено'

    def sorter_data(self, sorter_opt, is_reverse):
        """
        Сортирует список вакансий по заданному условию
        Args:
            sorter_opt (str): Значение параметра сортировки
            is_reverse (str): Значение параметра обратной сортировки
        """
        is_reverse_sorter = is_reverse == 'Да'

        if sorter_opt in ['Название', 'Описание', 'Компания', 'Название региона',
                           'Премиум-вакансия', 'Оклад указан до вычета налогов', 'Идентификатор валюты оклада']:
            self.vacancies = sorted(self.vacancies, reverse=is_reverse_sorter,
                                    key=lambda d: d.full_dict[invert_dic(dic_naming)[sorter_opt]])
        else:
            self.vacancies = sorted(self.vacancies, reverse=is_reverse_sorter, key=dic_sorters[sorter_opt])


class InputConect(object):
    """
    Класс для вывода полученного списка вакансий в виде таблицы
    """
    def __init__(self, file_path, filter_opt, sorter_opt, is_reverse, split_r, columns_r):
        """
        Инициализирует объект InputConect
        Args:
            file_path (str): Путь к csv-файлу с данными о вакансиях
            filter_opt (str): Значение параметра фильтрации
            sorter_opt (str): Значение параметра сортировки
            is_reverse (str): Значение параметра обратной сортировки
            split_r (list of two int): Нумерованные границы строк, которые должны быть выведены
            columns_r: Список названий столбцов, которые должны быть выведены
        """
        if check_filter_value(filter_opt):
            print(check_filter_value(filter_opt))
        elif check_sorter_value(sorter_opt):
            print(check_sorter_value(sorter_opt))
        elif check_reverse_value(is_reverse):
            print(check_reverse_value(is_reverse))
        else:
            data = DataSet(file_path)
            if data.vacancies in ['Нет данных', 'Пустой файл']:
                print(data.vacancies)
            else:
                # FILTER
                if filter_opt != '':
                    data.filter_data(filter_opt)

                # SORTER
                if sorter_opt != '':
                    data.sorter_data(sorter_opt, is_reverse)

                if data.vacancies == 'Ничего не найдено':
                    print('Ничего не найдено')
                else:
                    for index, vacancy in enumerate(data.vacancies):
                        table.add_row([index + 1] + [vacancy.name, vacancy.description, vacancy.key_skills,
                                                     vacancy.experience_id, vacancy.premium, vacancy.employer_name,
                                                     vacancy.salary, vacancy.area_name, vacancy.published_at])

                    columns_names.insert(0, '№')
                    columns_names.insert(7, 'salary')
                    columns_names.remove('Нижняя граница вилки оклада')
                    columns_names.remove('Верхняя граница вилки оклада')
                    columns_names.remove('Оклад указан до вычета налогов')
                    columns_names.remove('Идентификатор валюты оклада')
                    for (index, field) in enumerate(columns_names):
                        if field in dic_naming:
                            columns_names[index] = dic_naming[field]

                    table.field_names = columns_names
                    table._max_width = {'№': 20, 'Название': 20, 'Описание': 20, 'Навыки': 20, 'Опыт работы': 20,
                                        'Премиум-вакансия': 20, 'Компания': 20, 'Оклад': 20, 'Название региона': 20,
                                        'Дата публикации вакансии': 20}

                    output_range = [columns_names[0]] + columns_r
                    if columns_r[0] == '':
                        output_range = columns_names

                    if len(split_r) == 2:
                        print(table.get_string(start=int(split_r[0]) - 1, end=int(split_r[1]) - 1, fields=output_range))
                    elif split_r[0] != '':
                        print(table.get_string(start=int(split_r[0]) - 1, fields=output_range))
                    else:
                        print(table.get_string(fields=output_range))


columns_names = []
table = PrettyTable()
table.align = "l"
table.border = True
table.hrules = ALL
vacancies = []

def PrintTable():
    """
    Выводит данные о вакансиях в виде таблицы в соответствии с заданными параметрами фильтрации,
    сортировки и обратной сортировки
    """
    file = input('Введите название файла: ')
    filter_option = input('Введите параметр фильтрации: ')
    sorter_option = input('Введите параметр сортировки: ')
    is_reverse_sort = input('Обратный порядок сортировки (Да / Нет): ')
    split_range = input('Введите диапазон вывода: ').split(' ')
    columns_range = input('Введите требуемые столбцы: ').split(', ')

    inputConnect = InputConect(file, filter_option, sorter_option, is_reverse_sort, split_range, columns_range)

# Код из задачи 5.2
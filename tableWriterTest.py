import unittest
from tableWriter import *


class TableWriterTests(unittest.TestCase):
    def test_check_filter_value(self):
        self.assertEqual(check_filter_value('Название'), 'Формат ввода некорректен')
        self.assertEqual(check_filter_value('НеверныйЗаголовок'), 'Формат ввода некорректен')
        self.assertEqual(check_filter_value('Название: 1С-программист'), False)
        self.assertEqual(check_filter_value('Неверный заголовок: 1С-программист'), 'Параметр поиска некорректен')
        self.assertEqual(check_filter_value('Опыт работы: Без опыта'), False)

    def test_check_sorter_value(self):
        self.assertEqual(check_sorter_value('Название'), False)
        self.assertEqual(check_sorter_value(''), False)
        self.assertEqual(check_sorter_value('НеверныйЗаголовок'), 'Параметр сортировки некорректен')

    def test_check_reverse_value(self):
        self.assertEqual(check_reverse_value('Да'), False)
        self.assertEqual(check_reverse_value(''), False)
        self.assertEqual(check_reverse_value('НеверноеЗначение'), 'Порядок сортировки задан некорректно')

    def test_formatter(self):
        self.assertEqual(formatter('  Программист 1С'   , 'name'), 'Программист 1С')
        self.assertEqual(formatter('<p>Описание Вакансии</p>', 'description'), 'Описание Вакансии')
        self.assertEqual(formatter('between1And3', 'experience_id'), 'От 1 года до 3 лет')
        self.assertEqual(formatter('FALSE', 'premium'), 'Нет')
        self.assertEqual(formatter('2022-07-05T18:31:44+0300', 'published_at'), '05.07.2022')

    def test_salary(self):
        self.assertEqual(type(Salary(10.0, 20.4, 'False', 'RUR')).__name__, 'Salary')
        self.assertEqual(type(Salary(100, 200, 'False', 'EUR')).__name__, 'Salary')
        self.assertEqual(Salary(10.0, 20.4, 'False', 'RUR').salary_from, 10.0)
        self.assertEqual(Salary(10.0, 20.4, 'False', 'RUR').salary_to, 20.4)
        self.assertEqual(Salary(10.0, 20.4, 'False', 'RUR').salary_currency, 'RUR')
        self.assertEqual(Salary(10.0, 20.4, 'False', 'RUR').salary_gross, 'False')

    def test_converter(self):
        self.assertEqual(Salary(10, 20, 'False', 'RUR').converter(), 15)
        self.assertEqual(Salary(10, 20, 'False', 'EUR').converter(), 898)
        self.assertEqual(Salary(10, 20, 'False', 'RUR').converter(), 15)
        self.assertEqual(Salary(10.0, 20.0, 'False', 'RUR').converter(), 15)
        self.assertEqual(Salary(10.0, 20.0, 'False', 'EUR').converter(), 898)
        self.assertEqual(Salary(10.0, 20.0, 'False', 'RUR').converter(), 15)

    def test_vacancy(self):
        self.assertEqual(type(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300'])).__name__,
                         'Vacancy')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'True', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).name,
                         'Оператор сервисного центра')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).description,
                         'Необходимо отвечать на звонки клиентов и решать их проблемы')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).key_skills,
                         'Ответственность\nКоммуникабельность')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'True', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).experience_id,
                         'Нет опыта')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).premium,
                         'Нет')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).employer_name,
                         'ОАО "Информационные технологии"')
        self.assertEqual(str(type(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).salary)),
                         "<class 'str'>")
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).area_name,
                         'Екатеринбург')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', 'Ответственность\nКоммуникабельность', 'noExperience', 'False', 'ОАО "Информационные технологии"', 20000, 30000, 'False', 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).published_at,
                         '15.07.2022')

    def test_dataset(self):
        self.assertEqual(type(DataSet('vacancies.csv')).__name__, 'DataSet')

if __name__ == '__main__':
    unittest.main()

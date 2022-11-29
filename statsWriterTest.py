import unittest
from statsWriter import *


class StatsWriterTests(unittest.TestCase):
    def test_report_type(self):
        self.assertEqual(str(type(Report(['First_Worksheet', 'Second_Worksheet', 'Third_Worksheet'],
                         Side(style='thin', color="000000")))), "<class 'statsWriter.Report'>")

    def test_report_title_headers(self):
        self.assertEqual((Report(['First_Worksheet', 'Second_Worksheet', 'Third_Worksheet'],
                         Side(style='thin', color="000000")).ws_titles_headers),
                         ["First_Worksheet", "Second_Worksheet", "Third_Worksheet"])

    def test_salary_type(self):
        self.assertEqual(str(type(Salary(10.0, 20.4, 'RUR')).__name__), 'Salary')
        self.assertEqual(str(type(Salary(100, 200, 'EUR', 'Да')).__name__), 'Salary')

    def test_salary_from(self):
        self.assertEqual(Salary(10.0, 20.4, 'RUR').salary_from, 10.0)

    def test_salary_to(self):
        self.assertEqual(Salary(10.0, 20.4, 'RUR').salary_to, 20.4)

    def test_salary_currency(self):
        self.assertEqual(Salary(10.0, 20.4, 'RUR').salary_currency, 'RUR')
        self.assertEqual(Salary(100, 200, 'EUR', 'Да').salary_currency, 'EUR')

    def test_salary_gross(self):
        self.assertEqual(Salary(100, 200, 'EUR', 'Да').salary_gross, 'Да')
        self.assertEqual(Salary(10.0, 20.4, 'RUR').salary_gross, 'Нет')

    def test_salary_convert(self):
        self.assertEqual(Salary(10, 20, 'RUR').convert(), 15.0)
        self.assertEqual(Salary(10, 20, 'EUR').convert(), 898.5)
        self.assertEqual(Salary(10, 20, 'RUR', 'Да').convert(), 15.0)
        self.assertEqual(Salary(10.0, 20.0, 'RUR').convert(), 15.0)
        self.assertEqual(Salary(10.0, 20.0, 'EUR').convert(), 898.5)
        self.assertEqual(Salary(10.0, 20.0, 'RUR', 'Да').convert(), 15.0)

    def test_vacancy(self):
        self.assertEqual(type(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', ['Ответственность', 'Коммуникабельность'], 'Без опыта', 'Нет', 'ОАО "Информационные технологии"', 20000, 30000, 'RUR', 'Да', 'Екатеринбург', '2022-07-15T09:56:52+0300'])).__name__,
                         'Vacancy')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', ['Ответственность', 'Коммуникабельность'], 'Без опыта', 'Нет', 'ОАО "Информационные технологии"', 20000, 30000, 'RUR', 'Да', 'Екатеринбург', '2022-07-15T09:56:52+0300']).name,
                         'Оператор сервисного центра')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', ['Ответственность', 'Коммуникабельность'], 'Без опыта', 'Нет', 'ОАО "Информационные технологии"', 20000, 30000, 'RUR', 'Да', 'Екатеринбург', '2022-07-15T09:56:52+0300']).description,
                         'Необходимо отвечать на звонки клиентов и решать их проблемы')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', ['Ответственность', 'Коммуникабельность'], 'Без опыта', 'Нет', 'ОАО "Информационные технологии"', 20000, 30000, 'RUR', 'Да', 'Екатеринбург', '2022-07-15T09:56:52+0300']).key_skills,
                         ['Ответственность', 'Коммуникабельность'])
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', ['Ответственность', 'Коммуникабельность'], 'Без опыта', 'Нет', 'ОАО "Информационные технологии"', 20000, 30000, 'RUR', 'Да', 'Екатеринбург', '2022-07-15T09:56:52+0300']).experience_id,
                         'Без опыта')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', ['Ответственность', 'Коммуникабельность'], 'Без опыта', 'Нет', 'ОАО "Информационные технологии"', 20000, 30000, 'RUR', 'Да', 'Екатеринбург', '2022-07-15T09:56:52+0300']).premium,
                         'Нет')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', ['Ответственность', 'Коммуникабельность'], 'Без опыта', 'Нет', 'ОАО "Информационные технологии"', 20000, 30000, 'RUR', 'Да', 'Екатеринбург', '2022-07-15T09:56:52+0300']).employer_name,
                         'ОАО "Информационные технологии"')
        self.assertEqual(str(type(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', ['Ответственность', 'Коммуникабельность'], 'Без опыта', 'Нет', 'ОАО "Информационные технологии"', 20000, 30000, 'RUR', 'Да', 'Екатеринбург', '2022-07-15T09:56:52+0300']).salary)),
                         "<class 'statsWriter.Salary'>")
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', ['Ответственность', 'Коммуникабельность'], 'Без опыта', 'Нет', 'ОАО "Информационные технологии"', 20000, 30000, 'RUR', 'Да', 'Екатеринбург', '2022-07-15T09:56:52+0300']).area_name,
                         'Екатеринбург')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 'Необходимо отвечать на звонки клиентов и решать их проблемы', ['Ответственность', 'Коммуникабельность'], 'Без опыта', 'Нет', 'ОАО "Информационные технологии"', 20000, 30000, 'RUR', 'Да', 'Екатеринбург', '2022-07-15T09:56:52+0300']).published_at,
                         '2022-07-15T09:56:52+0300')

    def test_short_vacancy(self):
        self.assertEqual(str(type(Vacancy(['Оператор сервисного центра', 20000, 30000, 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300'])).__name__),
                         'Vacancy')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 20000, 30000, 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).name,
                         'Оператор сервисного центра')
        self.assertEqual(str(type(Vacancy(['Оператор сервисного центра', 20000, 30000, 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).salary)),
                         "<class 'statsWriter.Salary'>")
        self.assertEqual(Vacancy(['Оператор сервисного центра', 20000, 30000, 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).area_name,
                         'Екатеринбург')
        self.assertEqual(Vacancy(['Оператор сервисного центра', 20000, 30000, 'RUR', 'Екатеринбург', '2022-07-15T09:56:52+0300']).published_at,
                         '2022-07-15T09:56:52+0300')

    def test_dataset(self):
        self.assertEqual(type(DataSet('vacancies.csv')).__name__, 'DataSet')


if __name__ == '__main__':
    unittest.main()

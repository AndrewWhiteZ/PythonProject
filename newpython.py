import statsWriter
import tableWriter

output_type = input('Выберите формат представления выходных данных (Вакансии/Статистика): ')
if output_type == 'Вакансии':
    tableWriter.PrintTable()
elif output_type == 'Статистика':
    statsWriter.PrintStats()

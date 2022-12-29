import statsWriter
import tableWriter
import cProfile


output_type = input('Выберите формат представления выходных данных (Вакансии/Статистика): ')
if output_type == 'Вакансии':
    tableWriter.PrintTable()
    #cProfile.run('tableWriter.PrintTable()')
elif output_type == 'Статистика':
    statsWriter.PrintStats()
    #cProfile.run('statsWriter.PrintStats()')

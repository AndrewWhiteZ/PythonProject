import statsWriter
import tableWriter

<<<<<<< HEAD
output_type = input('Выберите возможность представления выходных данных (Вакансии/Статистика): ')
||||||| 8b91be6
output_type = input('Выберите способ представления выходных данных (Вакансии/Статистика): ')
=======
output_type = input('Выберите формат представления выходных данных (Вакансии/Статистика): ')
>>>>>>> newBranch1
if output_type == 'Вакансии':
    tableWriter.PrintTable()
elif output_type == 'Статистика':
    statsWriter.PrintStats()

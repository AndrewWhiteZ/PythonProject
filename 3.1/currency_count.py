import pandas as pd
df = pd.read_csv("../vacancies_dif_currencies.csv")
print(df.value_counts("salary_currency"))


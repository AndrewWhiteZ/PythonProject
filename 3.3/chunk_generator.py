import pandas as pd

vacancies = pd.read_csv("../vacancies_dif_currencies.csv")


def split_years(vacancies):
    return [vacancies[vacancies['published_at'].str[:4] == x] for x in vacancies['published_at'].str[:4].unique()]


res = split_years(vacancies)
for df in res:
    df.to_csv("../new_chunks/" + df['published_at'].iat[0][:4] + ".csv", encoding='utf-8', index=False)

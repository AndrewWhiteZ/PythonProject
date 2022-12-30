import pandas as pd
import numpy as np

currency_data = pd.read_csv("currency_data.csv")
currency_list = list(currency_data.head())
currency_list.remove('date')
currency_list.append('RUR')
currencies = set(currency_list)
df = pd.read_csv("../vacancies_dif_currencies.csv", encoding='utf-8', header=0)
df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
df['salary'] = np.floor(df.apply(
    lambda x: x['salary'] if (x['salary_currency'] == 'RUR'
                              or pd.isna(x['salary'])
                              or x['salary_currency'] not in currencies)
    else (x['salary'] * currency_data[currency_data['date'] == x['published_at'][:7]][x['salary_currency']].values[0]),
    axis=1))
df.drop(['salary_from', 'salary_to', 'salary_currency'], axis=1, inplace=True)
df = df[['name', 'salary', 'area_name', 'published_at']]
df.head(100).to_csv('vacancies_with_converted_salary.csv', encoding='utf-8', index=False)

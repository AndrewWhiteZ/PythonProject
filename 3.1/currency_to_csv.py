import requests
import pandas as pd

response = requests.get("http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req=01/01/2017")
currencies = ["BYR", "USD", "EUR", "KZT", "UAH"]
df = pd.DataFrame(currencies)
data = []
for year in range(2003, 2023):
    for month in range(1, 13):
        if year == 2016 and month == 7:
            currencies[0] = "BYN"
        response = requests.get(f"http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={f'01/{month:02d}/{year}'}")
        monthly_data = [f"{year}-{month:02d}"]
        if response.status_code == 200:
            xml = pd.read_xml(response.text)

            for currency in currencies:
                monthly_data.append(round(
                    xml[xml["CharCode"] == currency]["Value"].apply(
                        lambda x: float(x.split()[0].replace(',', '.'))).values[0]
                    / xml[xml["CharCode"] == currency]["Nominal"]
                    .apply(lambda x: float(x)).values[0], 4))
            data.append(monthly_data)
        else:
            break
df = pd.DataFrame(data, columns=["date"] + currencies)
df.to_csv("currency_data.csv", index=False, encoding="utf-8")

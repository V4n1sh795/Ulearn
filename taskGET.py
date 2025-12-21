import pandas as pd
import sqlite3
import math

df_currency = pd.read_csv('valutes.csv')
csv_merged = pd.read_csv('vacancies_dif_currencies.csv')

# Список для результатов
results = []
i=1
# Обрабатываем вакансии
for _, row in csv_merged.iterrows():
    # Рассчитываем зарплату
    if math.isnan(row['salary_from']) and math.isnan(row['salary_to']):
        salary = None
    elif math.isnan(row['salary_from']):
        salary = row['salary_to']
    elif math.isnan(row['salary_to']):
        salary = row['salary_from']
    else:
        salary = (row['salary_from'] + row['salary_to']) / 2

    # Конвертируем в рубли если нужно
    currency = row['salary_currency']
    if currency != 'RUR' and not(salary is None):
        date = pd.to_datetime(row['published_at'])
        month = date.strftime('%Y-%m')

        # Проверяем, есть ли такой месяц в курсах валют
        if month in df_currency['date'].values:
            # Проверяем, есть ли такая валюта в столбцах
            if currency in df_currency:
                rate = df_currency.loc[df_currency['date'] == month, currency].item()
                if not pd.isna(rate):
                    salary = salary * rate
                else:
                    salary = None
            else:
                salary = None
        else:
            # Если нет курса для этого месяца - пропускаем
            salary = None

    # Сохраняем результат
    results.append([i, row['name'], salary, row['area_name'], row['published_at']])
    i+=1

# Создаем DataFrame
df_result = pd.DataFrame(results, columns=['id', 'name', 'salary', 'area_name', 'published_at'])

# Сохраняем в SQLite
conn = sqlite3.connect('student_works/vacancies.db')
df_result.to_sql('vacancies', conn, if_exists='replace', index=False)
conn.close()
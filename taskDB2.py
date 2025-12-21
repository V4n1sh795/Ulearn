import sys
import sqlite3
import csv
from datetime import datetime

database_name = input()
csv_file = input()
table_name = input()
currency_table = input()

conn = sqlite3.connect(database_name)
cursor = conn.cursor()

cursor.execute(f"SELECT * FROM {currency_table}")
columns = [desc[0] for desc in cursor.description]
rates = {}

for row in cursor.fetchall():
    row_dict = {}
    for col, val in zip(columns, row):
        if col == 'date':
            date_key = val
        else:
            row_dict[col] = val 
    rates[date_key] = row_dict

cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        name TEXT,
        salary INTEGER,
        area_name TEXT,
        published_at TEXT
    )
""")

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['name']
        area_name = row['area_name']
        published_at = row['published_at']

        try:
            dt_str = published_at
            if dt_str.endswith('Z'):
                dt_str = dt_str[:-1] + '+00:00'
            dt = datetime.fromisoformat(dt_str)
            date_key = dt.isoformat()
        except Exception:
            final_salary = None
            cursor.execute(f"""
                INSERT INTO {table_name} (name, salary, area_name, published_at)
                VALUES (?, ?, ?, ?)
            """, (name, final_salary, area_name, published_at))
            continue

        def parse_float(val):
            if val == '' or val is None:
                return None
            try:
                return float(val)
            except ValueError:
                return None

        salary_from = parse_float(row['salary_from'])
        salary_to = parse_float(row['salary_to'])
        currency = row['salary_currency']

        if salary_from is None and salary_to is None:
            final_salary = None
        else:
            if salary_from is None:
                avg_salary = salary_to
            elif salary_to is None:
                avg_salary = salary_from
            else:
                avg_salary = (salary_from + salary_to) / 2.0

            rub_salary = None
            if currency == 'RUR':
                rub_salary = avg_salary
            else:
                if date_key in rates:
                    rate = rates[date_key].get(currency)
                    if rate is not None:
                        rub_salary = avg_salary * rate

            if rub_salary is None:
                final_salary = None
            else:
                final_salary = int(rub_salary)

        cursor.execute(f"""
            INSERT INTO {table_name} (name, salary, area_name, published_at)
            VALUES (?, ?, ?, ?)
        """, (name, final_salary, area_name, published_at))

conn.commit()
conn.close()
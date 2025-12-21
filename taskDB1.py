import pandas as pd
import sqlite3
import sys

def test(name, csv_file, table_name):
    conn = sqlite3.connect(name)
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, conn, index=False)
    conn.close()


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'test':
            test('db_name', 'test/vacancies.csv', 'tb_name')
    except IndexError:
        database_name = input()
        csv_file = input()
        table_name = input()
        test(database_name, csv_file, table_name)
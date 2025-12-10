from xmlrpc.server import SimpleXMLRPCServer
import pandas as pd
import threading
import sys

data = None
server = None 


def get_vacancy_by_id(vacancy_id):
    row = data[data['id'] == vacancy_id]
    if row.empty:
        return {}
    rec = row.iloc[0]
    return {
        'Название вакансии': str(rec['name']),
        'Зарплата от': float(rec['salary_from']),
        'Зарплата до': float(rec['salary_to']),
        'Город': str(rec['area_name'])
    }


def get_vacancies_by_city(city):
    filtered = data[data['area_name'] == city]
    result = {}
    for _, rec in filtered.iterrows():
        result[str(int(rec['id']))] = {
            'Название вакансии': str(rec['name']),
            'Зарплата от': float(rec['salary_from']),
            'Зарплата до': float(rec['salary_to']),
            'Город': str(rec['area_name'])
        }
    return result


def get_vacancies_by_min_salary(salary):
    filtered = data[data['salary_from'] >= salary]
    result = {}
    for _, rec in filtered.iterrows():
        result[str(int(rec['id']))] = {
            'Название вакансии': str(rec['name']),
            'Зарплата от': float(rec['salary_from']),
            'Зарплата до': float(rec['salary_to']),
            'Город': str(rec['area_name'])
        }
    return result


def exit_server():
    
    def stop():
        server.shutdown()
    threading.Thread(target=stop).start()
    return "Server shutting down"


def start_server():
    global data, server

    df = pd.read_csv(
        'vacancies.csv',
        header=None,
        names=['name', 'salary_from', 'salary_to', 'currency', 'area_name', 'published_at']
    )
    df['id'] = range(0, len(df))
    df['id'] = df['id'].astype(int)
    df['salary_from'] = pd.to_numeric(df['salary_from'], errors='coerce')
    df['salary_to'] = pd.to_numeric(df['salary_to'], errors='coerce')
    df['name'] = df['name'].astype(str)
    df['area_name'] = df['area_name'].astype(str)
    data = df

    server = SimpleXMLRPCServer(("localhost", 8000))
    server.register_function(get_vacancy_by_id, "get_vacancy_by_id")
    server.register_function(get_vacancies_by_city, "get_vacancies_by_city")
    server.register_function(get_vacancies_by_min_salary, "get_vacancies_by_min_salary")
    server.register_function(exit_server, "exit")

    server.serve_forever()


if __name__ == '__main__':
    start_server()
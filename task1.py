def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Данные некорректны, повторите ввод")


def get_int_input(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Данные некорректны, повторите ввод")


def get_bool_input(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in ("да", "нет"):
            return value == "да"
        else:
            print("Данные некорректны, повторите ввод")


def get_salary_bounds():
    while True:
        lower = get_int_input("Введите нижнюю границу оклада вакансии: ")
        upper = get_int_input("Введите верхнюю границу оклада вакансии: ")
        if lower <= upper:
            return lower, upper
        else:
            print("Нижняя граница оклада должна быть не больше верхней границы. Повторите ввод.")


def format_experience(years):
    if 11 <= years % 100 <= 14:
        return f"{years} лет"
    elif years % 10 == 1:
        return f"{years} год"
    elif 2 <= years % 10 <= 4:
        return f"{years} года"
    else:
        return f"{years} лет"

def sklon(n, n1, n2_4, n5_0):
    n = abs(n) % 100
    if 11 <= n <= 19:
        return n5_0
    last_digit = n % 10
    if last_digit == 1:
        return n1
    elif last_digit in (2, 3, 4):
        return n2_4
    else:
        return n5_0


title = get_non_empty_input("Введите название вакансии: ")
description = get_non_empty_input("Введите описание вакансии: ")
city = get_non_empty_input("Введите город для вакансии: ")
experience = get_int_input("Введите требуемый опыт работы (лет): ")
lower_salary, upper_salary = get_salary_bounds()
flexible_schedule = get_bool_input("Нужен свободный график (да / нет): ")
premium = get_bool_input("Является ли данная вакансия премиум-вакансией (да / нет): ")

avg_salary = (lower_salary + upper_salary) // 2

print(title)
print(f"Описание: {description}")
print(f"Город: {city}")
print(f"Требуемый опыт работы: {format_experience(experience)}")
print(f"Средний оклад: {avg_salary} {sklon(avg_salary, 'рубль', 'рубля', 'рублей')}")
print(f"Свободный график: {'да' if flexible_schedule else 'нет'}")
print(f"Премиум-вакансия: {'да' if premium else 'нет'}")


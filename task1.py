# let's get started!!!
ask = {
    'vac': "Введите название вакансии: ",
    'desc': "Введите описание вакансии: ",
    'city': "Введите город для вакансии: ",
    'exp': "Введите требуемый опыт работы (лет): ",
    'minsal': "Введите нижнюю границу оклада вакансии: ",
    'maxsal': "Введите верхнюю границу оклада вакансии: ",
    'graf': "Нужен свободный график (да / нет): ",
    'prem': "Является ли данная вакансия премиум-вакансией (да / нет): "
}

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

answers = {}
for key, prompt in ask.items():
    while True:
        try:
            inp = input(prompt)
        except EOFError:
            exit(1)
        if key in ['vac', 'desc', 'city']:
            if inp:
                answers[key] = inp
                break
            else:
                print("Данные некорректны, повторите ввод")

        elif key in ['exp', 'minsal', 'maxsal']:
            try:
                num = int(inp)
                if key == 'maxsal' and answers['minsal'] >= num:
                    print("Нижняя граница оклада должна быть не больше верхней границы. Повторите ввод.")
                    continue
                answers[key] = num
                break
            except ValueError:
                print("Данные некорректны, повторите ввод")

        elif key in ['graf', 'prem']:
            if inp == "да":
                answers[key] = inp
                break
            elif inp == "нет":
                answers[key] = inp
                break
            else:
                print("Данные некорректны, повторите ввод")
try:
    avg_sal = (answers['minsal'] + answers['maxsal']) // 2  
except Exception as e:
    avg_sal = answers['minsal']

print(answers['vac'])
print(f"Описание: {answers['desc']}")
print(f"Город: {answers['city']}")
print(f"Требуемый опыт работы: {answers['exp']} {sklon(answers['exp'], 'год', 'года', 'лет')}")
print(f"Средний оклад: {avg_sal} {sklon(avg_sal, 'рубль', 'рубля', 'рублей')}")
print(f"Свободный график: {answers['graf']}")
print(f"Премиум-вакансия: {answers['prem']}")


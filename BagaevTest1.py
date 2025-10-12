import prettytable

file = input()
shear = input().split(' ')

if len(shear) > 1:
    for i in range(len(shear)):
        shear[i] = int(shear[i])

if len(shear) == 1:
    shear.append(False)
headings_shear = [x for x in input().split(', ')]

if headings_shear[0] != '':
    headings_shear.insert(0, '№')

def csv_reader(file_name):
    text_list = []
    file = open(file_name, 'r', encoding='utf_8_sig')
    text = file.read()

    start = 0
    count = 0
    for i in range(len(text)):
        if text[i] == '\"':
            count += 1
        if count%2 == 0 and text[i] == '\n':
            text_list.append(text[start:i])
            start = i + 1
        if i == len(text) - 1:
            text_list.append(text[start:i+1])
    heading = text_list[0].split(',')
    text_list.pop(0)

    vacancies_list = []
    for vacancy in text_list:
        vacancy_list = []
        start = 0
        count = 0
        for j in range(len(vacancy)):
            if vacancy[j] == '"':
                count += 1
            if count % 2 == 0 and vacancy[j] == ',':
                vac = vacancy[start:j]
                if vac[0] == '\"':
                    vac = vac[1:]
                if vac[-1] == '\"':
                    vac = vac[:-1]
                vacancy_list.append(vac.replace('\"\"', '\"'))
                start = j + 1
            if j == len(vacancy) - 1:
                vac = vacancy[start:j + 1]
                if vac[0] == '\"':
                    vac = vac[1:]
                if vac[-1] == '\"':
                    vac = vac[:-1]
                vacancy_list.append(vac.replace('\"\"', '\"'))
        for i in range(len(vacancy_list)):
            if vacancy_list[i] == '':
                vacancy_list[i] = 'Нет данных'
            if len(vacancy_list[i]) > 100:
                vacancy_list[i] = vacancy_list[i][:100] + '...'
        vacancies_list.append(vacancy_list)



    vacancies_list = [element for element in vacancies_list if element]
    final = [vacancies_list, heading]
    return final

def print_vacancies(vacancies, titles):

    headings = titles
    headings.insert(0, '№')
    table = prettytable.PrettyTable()
    table.field_names = headings
    for vacancy_id in range(len(vacancies)):
        vacancies[vacancy_id].insert(0, vacancy_id+1)
        table.add_row(vacancies[vacancy_id])
    table.hrules = prettytable.ALL
    table.max_width = 20
    table.align = "l"
    if len(vacancies) == 0:
        return ['Нет данных', False]
    else:
        return [table, True]

ph = csv_reader(file)
table = print_vacancies(ph[0], ph[1])
if table[1]:
    tb = table[0]
    if shear[0] != '' and headings_shear[0] != '':
        if shear[1] == False:
            tb = tb.get_string(start=int(shear[0])-1, fields=headings_shear)
        else:
            tb = tb.get_string(start=int(shear[0])-1, end=int(shear[1]), fields=headings_shear)
    elif shear[0] == '' and headings_shear[0] != '':
        tb = tb.get_string(fields=headings_shear)
    elif shear[0] != '' and headings_shear[0] == '':
        if shear[1] == False:
            tb = tb.get_string(start=int(shear[0])-1)
        else:
            tb = tb.get_string(start=int(shear[0])-1, end=int(shear[1]))
    print(tb)
else:
    print(table[0])
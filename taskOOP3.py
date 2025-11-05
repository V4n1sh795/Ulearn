from datetime import datetime

class Vacancy:
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name,
                 published_at):
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class Salary:
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


class DataSet:
    def __init__(self, file_name):
        raw_lines = []
        with open(file_name, 'r', encoding='utf_8_sig') as f:
            content = f.read()

        start_pos = 0
        quote_count = 0
        n = len(content)
        for idx in range(n):
            if content[idx] == '"':
                quote_count += 1
            if quote_count % 2 == 0 and content[idx] == '\n':
                raw_lines.append(content[start_pos:idx])
                start_pos = idx + 1
            if idx == n - 1:
                raw_lines.append(content[start_pos:idx + 1])

        parsed_data = []
        headers = raw_lines[0].split(',')
        parsed_data.append(headers)
        raw_lines = raw_lines[1:]

        for row in raw_lines:
            fields = []
            pos = 0
            quotes = 0
            row_len = len(row)
            for j in range(row_len):
                if row[j] == '"':
                    quotes += 1
                if quotes % 2 == 0 and row[j] == ',':
                    if j == pos:
                        fields.append('')
                        pos = j + 1
                    else:
                        cell = row[pos:j]
                        if cell.startswith('"'):
                            cell = cell[1:]
                        if cell.endswith('"'):
                            cell = cell[:-1]
                        fields.append(cell.replace('""', '"'))
                        pos = j + 1
                if j == row_len - 1:
                    cell = row[pos:j + 1]
                    if cell.startswith('"'):
                        cell = cell[1:]
                    if cell.endswith('"'):
                        cell = cell[:-1]
                    fields.append(cell.replace('""', '"'))
            parsed_data.append(fields)

        self.data = [entry for entry in parsed_data if entry]


class Statistics:
    def __init__(self, dataset):
        self.raw_data = dataset.data

    def get_salary_stat(self, target_role):
        exchange_rates = {
            "Манаты": 35.68,
            "Белорусские рубли": 23.91,
            "Евро": 59.90,
            "Грузинский лари": 21.74,
            "Киргизский сом": 0.76,
            "Тенге": 0.13,
            "Рубли": 1,
            "Гривны": 1.64,
            "Доллары": 60.66,
            "Узбекский сум": 0.0055,
        }

        avg_sal_by_year = {}
        avg_sal_by_year_job = {}
        vac_count_by_year = {}
        avg_sal_by_city = {}
        share_vac_by_city = {}
        job_vac_count_by_year = {}

        all_entries = self.raw_data
        header_line = all_entries[0]
        city_col = header_line.index('area_name')
        date_col = header_line.index('published_at')
        sal_from_col = header_line.index('salary_from')
        sal_to_col = header_line.index('salary_to')
        currency_col = header_line.index('salary_currency')
        title_col = header_line.index('name')
        all_entries = all_entries[1:]
        total_vacancies = len(all_entries)

        for yr in range(2003, 2025):
            avg_sal_by_year[yr] = [0, 0]
            avg_sal_by_year_job[yr] = [0, 0]
            job_vac_count_by_year[yr] = 0

        for record in all_entries:
            year_val = int(record[date_col].split('/')[-1])
            if year_val not in vac_count_by_year:
                vac_count_by_year[year_val] = 0

            city_name = record[city_col]
            if city_name not in avg_sal_by_city:
                avg_sal_by_city[city_name] = [0, 0]
            if city_name not in share_vac_by_city:
                share_vac_by_city[city_name] = 0

            mid_salary = ((float(record[sal_from_col]) + float(record[sal_to_col])) / 2.0) * exchange_rates[record[currency_col]]

            avg_sal_by_year[year_val][0] += mid_salary
            avg_sal_by_year[year_val][1] += 1

            avg_sal_by_city[city_name][0] += mid_salary
            avg_sal_by_city[city_name][1] += 1

            share_vac_by_city[city_name] += 1
            vac_count_by_year[year_val] += 1

            if target_role in record[title_col].lower():
                avg_sal_by_year_job[year_val][0] += mid_salary
                avg_sal_by_year_job[year_val][1] += 1
                job_vac_count_by_year[year_val] += 1

        to_remove_avg_year = []
        to_remove_avg_job = []
        to_remove_city_avg = []
        to_remove_job_count = []

        for yr_key in avg_sal_by_year:
            if avg_sal_by_year[yr_key][1] > 0:
                avg_sal_by_year[yr_key] = round(avg_sal_by_year[yr_key][0] / avg_sal_by_year[yr_key][1])
            else:
                to_remove_avg_year.append(yr_key)

        for yr_key in avg_sal_by_year_job:
            if avg_sal_by_year_job[yr_key][1] > 0:
                avg_sal_by_year_job[yr_key] = round(avg_sal_by_year_job[yr_key][0] / avg_sal_by_year_job[yr_key][1])
            else:
                to_remove_avg_job.append(yr_key)

        for city in avg_sal_by_city:
            if avg_sal_by_city[city][1] > 0:
                avg_sal_by_city[city] = round(avg_sal_by_city[city][0] / avg_sal_by_city[city][1])
            else:
                to_remove_city_avg.append(city)
            share_vac_by_city[city] = round(share_vac_by_city[city] / total_vacancies, 4)

        for yr_key in job_vac_count_by_year:
            if job_vac_count_by_year[yr_key] == 0:
                to_remove_job_count.append(yr_key)

        for k in to_remove_city_avg:
            del avg_sal_by_city[k]
        for k in to_remove_avg_job:
            del avg_sal_by_year_job[k]
        for k in to_remove_avg_year:
            del avg_sal_by_year[k]
        for k in to_remove_job_count:
            del job_vac_count_by_year[k]

        avg_sal_by_year = dict(sorted(avg_sal_by_year.items()))
        vac_count_by_year = dict(sorted(vac_count_by_year.items()))
        avg_sal_by_year_job = dict(sorted(avg_sal_by_year_job.items()))
        job_vac_count_by_year = dict(sorted(job_vac_count_by_year.items()))
        avg_sal_by_city = dict(sorted(avg_sal_by_city.items(), key=lambda x: x[1], reverse=True)[:10])
        share_vac_by_city = dict(sorted(share_vac_by_city.items(), key=lambda x: x[1], reverse=True)[:10])

        print(f"Средняя зарплата по годам: {avg_sal_by_year}")
        print(f"Количество вакансий по годам: {vac_count_by_year}")
        print(f"Средняя зарплата по годам для профессии '{target_role}': {avg_sal_by_year_job}")
        print(f"Количество вакансий по годам для профессии '{target_role}': {job_vac_count_by_year}")
        print(f"Средняя зарплата по городам: {avg_sal_by_city}")
        print(f"Доля вакансий по городам: {share_vac_by_city}")


def main():
    inp_file = input()
    job_title = input()
    dataset_obj = DataSet(inp_file)
    stats_processor = Statistics(dataset_obj)
    stats_processor.get_salary_stat(job_title)


if __name__ == '__main__':
    main()
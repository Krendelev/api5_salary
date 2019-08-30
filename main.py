import itertools
import statistics
import requests
from terminaltables import AsciiTable

from settings import HeadHunter, SuperJob, languages


def predict_rub_salary(salary_from, salary_to):
    if not salary_from:
        return salary_to * 0.8
    elif not salary_to:
        return salary_from * 1.2
    else:
        return (salary_to + salary_from) / 2


def get_vacancies(url, headers, payload, records):
    for page in itertools.count():
        payload.update({"page": page})
        response = requests.get(url, headers=headers, params=payload)
        if not (response.ok and response.json()[records]):
            break
        yield from response.json()[records]


def get_salary_info(site):
    salary_info = {}
    for language in languages:
        payload = site.make_payload(language)
        vacancies_count = requests.get(
            site.url, headers=site.headers, params=payload
        ).json()[site.total]

        records = site.record_name
        vacancies = get_vacancies(site.url, site.headers, payload, records)
        salaries = (site.extract_salary(vacancy) for vacancy in vacancies)

        salaries_proccessed = []
        for salary in salaries:
            salary_from, salary_to, currency = salary
            if currency != site.currency_abbr:
                continue
            proccessed = predict_rub_salary(salary_from, salary_to)
            if proccessed:
                salaries_proccessed.append(proccessed)

        if salaries_proccessed:
            average_salary = int(statistics.mean(salaries_proccessed))
        else:
            average_salary = 0

        salary_info.update(
            {
                language: {
                    "vacancies_found": vacancies_count,
                    "vacancies_processed": len(salaries_proccessed),
                    "average_salary": average_salary,
                }
            }
        )
    return salary_info


def make_table(data):
    table_data = []
    table_data.append(
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    )
    for key, value in data.items():
        table_data.append([key] + [values for values in value.values()])
    return table_data


if __name__ == "__main__":
    sites = [HeadHunter(), SuperJob()]
    for site in sites:
        salary_info = get_salary_info(site)
        table = AsciiTable(make_table(salary_info))
        table.title = site.title
        print(table.table)

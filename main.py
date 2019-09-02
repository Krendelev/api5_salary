import itertools
import logging
import statistics
import sys
import requests
from terminaltables import AsciiTable

import settings
from data_providers import HeadHunter, SuperJob


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
        # HeadHunter responses 400 to attempt to get more than 2000 records
        if not response.ok and response.status_code != 400:
            response.raise_for_status()
        current_records = response.json()[records] if response.ok else None
        if not current_records:
            break
        yield from current_records


def get_salary_info(site, languages):
    salary_info = {}
    for language in languages:
        payload = site.make_payload(language)
        response = requests.get(site.url, headers=site.headers, params=payload)
        response.raise_for_status()
        vacancies_count = response.json()[site.total]

        records = site.record_name
        vacancies = get_vacancies(site.url, site.headers, payload, records)
        salaries = (site.extract_salary(vacancy) for vacancy in vacancies)

        predicted_salaries = (
            predict_rub_salary(salary_from, salary_to)
            for salary_from, salary_to, salary_currency in salaries
            if salary_currency == site.ruble_abbr
        )
        filtered_salaries = list(filter(None, predicted_salaries))

        average_salary = (
            int(statistics.mean(filtered_salaries)) if filtered_salaries else 0
        )
        salary_info[language] = {
            "vacancies_found": vacancies_count,
            "vacancies_processed": len(filtered_salaries),
            "average_salary": average_salary,
        }

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
        table_data.append(
            [
                key,
                value["vacancies_found"],
                value["vacancies_processed"],
                value["average_salary"],
            ]
        )
    return table_data


if __name__ == "__main__":
    logging.basicConfig(filename="main.log", format="%(asctime)s - %(message)s")
    sites = [HeadHunter(), SuperJob()]
    for site in sites:
        try:
            salary_info = get_salary_info(site, settings.LANGUAGES)
        except requests.exceptions.RequestException as e:
            logging.exception("Exception occurred")
            sys.exit(1)
        table = AsciiTable(make_table(salary_info))
        table.title = site.title
        print(table.table)

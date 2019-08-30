import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class HeadHunter:
    title: str = "HeadHunter"
    url: str = "https://api.hh.ru/vacancies"
    headers: dict = field(default_factory=lambda: {})
    record_name: str = "items"
    total: str = "found"
    currency_abbr: str = "RUR"

    def make_payload(self, language):
        return {
            "text": f"программист {language}",
            "area": 1,
            "period": 30,
            "per_page": 100,
        }

    def extract_salary(self, vacancy):
        salary = vacancy["salary"]
        if not salary:
            return (None, None, None)
        return salary["from"], salary["to"], salary["currency"]


@dataclass
class SuperJob:
    title: str = "SuperJob"
    url: str = "https://api.superjob.ru/2.0/vacancies/"
    headers: dict = field(
        default_factory=lambda: {
            "X-Api-App-Id": os.environ["SJ_TOKEN"],
            "Authorization": "Bearer r.000000010000001.example.access_token",
        }
    )
    record_name: str = "objects"
    total: str = "total"
    per_page: str = "count"
    currency_abbr: str = "rub"

    def make_payload(self, language):
        return {
            "keywords[0][keys]": "",
            "keywords[1][srws]": 1,
            "keywords[1][keys]": language,
            "town": 4,
            "catalogues": 48,
            "period": 30,
            "count": 100,
        }

    def extract_salary(self, vacancy):
        return vacancy["payment_from"], vacancy["payment_to"], vacancy["currency"]


languages = [
    "javascript",
    "java",
    "python",
    "php",
    "c++",
    "c#",
    "typescript",
    "c",
    "ruby",
    "1с",
]

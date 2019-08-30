# Programming vacancies compare

Script to fetch salary offerings to developers from [HeadHunter](https://hh.ru) and [SuperJob](https://www.superjob.ru).

### How to install

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

### Usage

There's no need to register with HeadHunter, but you have to create account on SuperJob in order to obtain `Secret key` to their API. Put it into the `.env` file.

```bash
$ python main.py
+HeadHunter-------------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| javascript            | 2662             | 768                 | 134464           |
| java                  | 1846             | 393                 | 167263           |
| python                | 1420             | 346                 | 158219           |
| php                   | 1183             | 566                 | 122148           |
| c++                   | 152              | 65                  | 128069           |
| c#                    | 1126             | 322                 | 149825           |
| typescript            | 465              | 161                 | 164413           |
| c                     | 341              | 169                 | 133283           |
| ruby                  | 204              | 70                  | 154867           |
| 1с                    | 848              | 432                 | 131081           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob---------------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| javascript            | 4                | 4                   | 119250           |
| java                  | 8                | 6                   | 115333           |
| python                | 2                | 1                   | 84000            |
| php                   | 16               | 7                   | 117457           |
| c++                   | 10               | 7                   | 111917           |
| c#                    | 11               | 6                   | 171333           |
| typescript            | 0                | 0                   | 0                |
| c                     | 2                | 2                   | 105000           |
| ruby                  | 0                | 0                   | 0                |
| 1с                    | 107              | 65                  | 120050           |
+-----------------------+------------------+---------------------+------------------+
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

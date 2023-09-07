class Vacancy:
    def __init__(self, name, description, company, salary, currency):
        self.name = name
        self.description = description
        self.company = company
        self.salary = salary
        self.currency = currency

    def __repr__(self):
        return f'Vacancy({self.name}, {self.description}, {self.company}, {self.salary}, {self.currency})'



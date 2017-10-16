import json

from production import PRODUCTION
from research import RESEARCH
from base import Base
from utils import calculate_next_base_price


class Game:
    def __init__(self, area, solar, fertility, metal, gas, crystals, location):
        self.time = 0
        self.eco = 100
        self.log = []

        self.products = {p: 0 for p in PRODUCTION.keys()}
        self.technologies = {r: 0 for r in RESEARCH.keys()}

        self.bases = [
            Base(area, solar, fertility, metal, gas, crystals, location, energy=2, construction=40, game=self),
        ]

    def product_finished(self, product):
        self.log.append('{}\tFinished product:\t'.format(self.time, product))

        if product['Goods']:
            self.eco += 21
        elif product['Outpost Ship']:
            next_base_price = calculate_next_base_price(len(self.bases))
            if self.eco >= next_base_price:
                self.eco -= next_base_price
                self.bases.append(Base(85, 3, 5, 3, 1, 0, 'X14:54:16:41', energy=2, construction=20, game=self))
        else:
            self.products[product] += 1

    def remove_product(self, product):
        self.products[product] -= 1

    def research_finished(self, technology):
        self.log.append('{}\tFinished research:\t'.format(self.time, technology))
        self.technologies[technology] += 1

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def save(self, name):
        with open('{}_{}.txt'.format(name, self.time), 'w') as outfile:
            outfile.write(self.json())

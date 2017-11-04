import json

from Game.base import Base
from Game.base.utils import calculate_price, calculate_next_base_price
from Game.production import PRODUCTION
from Game.research import RESEARCH


class Game:
    def __init__(self, area, solar, fertility, metal, gas, crystals, location):
        self.time = 0
        self.eco = 100

        self.products = {p: 0 for p in PRODUCTION.keys()}
        self.technologies = {r: 0 for r in RESEARCH.keys()}

        self.bases = [
            Base(area, solar, fertility, metal, gas, crystals, location,
                 basic_energy_production=2, basic_construction=40,
                 fleet=self.products, technologies=self.technologies),
        ]

    def exchange_products(self):
        if self.products['Goods']:
            self.products['Goods'] -= 1
            self.eco += 21

        if self.products['Outpost Ship']:
            next_base_price = calculate_next_base_price(len(self.bases))
            if self.eco >= next_base_price:
                self.eco -= next_base_price
                self.products['Outpost Ship'] -= 1
                self.bases.append(Base(85, 3, 5, 3, 1, 0, 'X14:54:16:41',
                                       basic_energy_production=2, basic_construction=20,
                                       fleet=self.products, technologies=self.technologies))

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def save(self, name):
        with open('{}_{}.txt'.format(name, self.time), 'w') as outfile:
            outfile.write(self.json())

    # FIXME: somehow
    def start_research(self, base, technology, game):
        research_cost = calculate_price(price=RESEARCH[technology].eco, level=game.technologies[technology])

        if technology not in [b.q_research.performing for b in game.bases if b.q_research.performing] and \
            base.structures['Research Labs'] >= RESEARCH[technology].lab_req and \
            game.eco >= research_cost:
            game.eco -= research_cost
            base.q_research.start()   # FIXME:performing, cost, time_now, resources):
            return True
        else:
            return False


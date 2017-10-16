from math import sqrt


class BaseTradeRoutes:
    def __init__(self, base):
        self.trade_routes_self = []
        self.trade_routes_foreign = 0

        self.__base = base
        self.__dict__.pop('_' + self.__class__.__name__ + '__base')  # avoid circular reference when serialising

    def calculate_income(self):
        self_income = sum(1.2 * sqrt(min(self.__base.eco, b.eco)) for b in self.trade_routes_self)
        foreign_income = 1.2*sqrt(self.__base.eco) * self.trade_routes_foreign
        return self_income + foreign_income

    def create_self_route(self, bases):
        if not self.free_routes_slots():
            return False

        hosts = [b for b in bases if b != self and b.free_routes_slots()]
        if not hosts:
            return False

        base_best = min(bases, key=lambda x: abs(x.eco - self.__base.eco))
        base_best.trade_routes.trade_routes_self.append(self.__base)
        self.trade_routes_self.append(base_best)
        return True

    def create_foreign_route(self):
        if not self.free_routes_slots():
            return False

        self.trade_routes_foreign += 1
        return True

    def free_routes_slots(self):
        spaceports = self.__base.structures['Spaceports']
        routes_slots_used = len(self.trade_routes_self) + self.trade_routes_foreign
        routes_slots_max = (1 if spaceports else 0) + spaceports/5
        return routes_slots_max - routes_slots_used

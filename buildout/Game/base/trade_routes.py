class BaseTradeRoutes:
    def __init__(self):
        self.trade_routes_self = []
        self.trade_routes_foreign = 0

    def create_self_route(self, base):
        self.trade_routes_self.append(base)
        base.trade_routes_self.append(self)

    def create_foreign_route(self):
        self.trade_routes_foreign += 1

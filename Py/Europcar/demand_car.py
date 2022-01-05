import numpy as np

from parameters import *


class DemandCar:

    def __init__(self, low=10, high=30):
        self.low = low
        self.high = high

    def get_demands(self, prices, d1) -> []:
        demands = np.zeros((0, 2), dtype=int)
        p1, p2, p3 = prices
        for delay in range(min(MAX_DELAY_TO_BOOK, DAYS_IN_YEAR-d1)):
            p = p1 if delay == 0 else p2 if delay <= 10 else p3
            demands = self.get_demands_at_d2(p, d1, d1+delay, demands)
        return demands

    def get_demands_at_d2(self, p, d1, d2, demands) -> []:
        '''

        :param p:
        :param d1:
        :param d2:
        :param demands:
        :return:
        '''
        demand_multiplier_d2 = (1 + (self.high/self.low - 1) * np.sin(d2 / DAYS_IN_YEAR * np.pi) ** 2)
        demand_multiplier_d1d2 = self.get_demand_multiplier_d1d2(d1, d2)
        wtp_multiplier_d2 = np.sqrt((1 + (self.high/self.low - 1) * np.sin(d2 / DAYS_IN_YEAR * np.pi) ** 2))
        wtp_multiplier_d1d2 = np.sqrt(1 + (self.high/self.low - 1) * np.exp(d1 - d2))

        d0 = NOMINAL_DEMAND * demand_multiplier_d2 * demand_multiplier_d1d2
        avg_price = NOMINAL_PRICE * wtp_multiplier_d2 * wtp_multiplier_d1d2
        avg_demand = self.get_average_demand(d0=d0, avg_price=avg_price, p=p)

        demands_nb = np.random.poisson(avg_demand)
        for _ in range(demands_nb):
            duration = np.random.poisson(AVG_DURATION-1)+1
            demand = (d2, d2+duration)
            demands = np.vstack((demands, demand))
        return demands

    def get_demand_multiplier_d1d2(self, d1, d2):

        if d2 < d1:
            dm = 0
        else:
            dm = 1/3 if d1 == d2 else 1/30 if d2-10 <= d1 else 1/3 * 1/90
        return dm

    def get_average_demand(self, d0=100, avg_price=30, b=3, p=30):
        a = avg_price * b
        aa = d0 * (1 + np.exp(a)) / np.exp(a)
        avg_demand = aa * np.exp(a -b * p) / (1 + np.exp(a - b * p))
        return avg_demand
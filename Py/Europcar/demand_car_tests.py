import unittest
import demand_car as dc
import numpy as np


class MyTestCase(unittest.TestCase):

    def test_demand_multiplier_d1d2(self):

        year = 355
        low = 1
        high = 3
        d2 = 110
        cumulated_mul = 0
        demand = dc.DemandCar(low=low, high=high, days_in_years=year)
        for d1 in range(d2+1):
            cumulated_mul += demand.get_demand_multiplier_d1d2(d1, d2)
            #print(d1, demand.get_demand_multiplier_d1d2(d1, d2), cumulated_mul)
        self.assertAlmostEqual(cumulated_mul, 1)  # sum should be 1 if d2>100

    def test_get_average_demand(self):
        demand = dc.DemandCar()
        dem = demand.get_average_demand(d0=100, avg_price=30, b=3, p=30)
        self.assertAlmostEqual(dem, 0.5*100)

        dem = demand.get_average_demand(d0=100, avg_price=30, b=3, p=0)
        self.assertAlmostEqual(dem, 100)

        dem = demand.get_average_demand(d0=100, avg_price=30, b=3, p=300)
        self.assertAlmostEqual(dem, 0)

    def test_get_demands(self):
        demand = dc.DemandCar()
        dem = demand.get_demands(30, 85, 188)
        print(dem)



if __name__ == '__main__':
    unittest.main()

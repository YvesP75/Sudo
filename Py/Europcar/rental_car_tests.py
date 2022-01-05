import unittest
import rental_car as rc
import numpy as np

from parameters import *


class RentalCarTestsCase(unittest.TestCase):

    def test_financials_of_the_day(self):
        car0 = rc.RentalCar(max_cars=30, start_cars=0)
        rev, cost, _ = car0.get_financials(t=0, day_prices=0, starting_bookings=0, new_orders=0)
        await_rev, await_costs = 0, 0*car0.car_cost_per_day_in_carpark
        self.assertEqual((rev, cost), (await_rev, await_costs))

        car10 = rc.RentalCar(max_cars=30, start_cars=10)
        rev, cost, _ = car10.get_financials(t=0, day_prices=10, starting_bookings=0, new_orders=0)
        await_rev, await_costs = 0, 10*car0.car_cost_per_day_in_carpark
        self.assertEqual((rev, cost), (await_rev, await_costs))

        car10 = rc.RentalCar(max_cars=30, start_cars=10)
        car10.cars_booked[:12, :] = True
        rev, cost, _ = car10.get_financials(t=0, day_prices=10, starting_bookings=0, new_orders=0)
        await_rev, await_costs = 12*10, 10*car10.car_cost_per_day_in_carpark
        self.assertEqual((rev, cost), (await_rev, await_costs))


    def test_update_carpark(self):
        car10 = rc.RentalCar(max_cars=30, start_cars=10)

        car_variation = 0
        day_cars_before = np.count_nonzero(car10.cars_in_carpark)
        car10.update_carpark(car_variation, t=0)
        day_cars_after = np.count_nonzero(car10.cars_in_carpark)
        self.assertEqual(day_cars_before, day_cars_after)  # nothing should occur

        car_variation = 10
        day_cars_before = np.count_nonzero(car10.cars_in_carpark)
        car10.update_carpark(car_variation=car_variation, t=0)
        day_cars_after = np.count_nonzero(car10.cars_in_carpark)
        self.assertEqual(day_cars_after - day_cars_before, car_variation * (DAYS_IN_YEAR-car10.days_to_get_a_car))

        car_variation = 11
        day_cars_before = np.count_nonzero(car10.cars_in_carpark)
        car10.update_carpark(car_variation=car_variation, t=0)
        day_cars_after = np.count_nonzero(car10.cars_in_carpark)
        self.assertEqual(day_cars_after - day_cars_before, 10 * (DAYS_IN_YEAR-car10.days_to_get_a_car))

        car_variation = -10
        day_cars_before = np.count_nonzero(car10.cars_in_carpark)
        car10.update_carpark(car_variation=car_variation, t=0)
        day_cars_after = np.count_nonzero(car10.cars_in_carpark)
        self.assertEqual(day_cars_after - day_cars_before, car_variation * (DAYS_IN_YEAR-car10.days_to_return_a_car))

        car_variation = -21
        day_cars_before = np.count_nonzero(car10.cars_in_carpark)
        car10.update_carpark(car_variation=car_variation, t=0)
        day_cars_after = np.count_nonzero(car10.cars_in_carpark)
        self.assertEqual(day_cars_after - day_cars_before, -20 * (DAYS_IN_YEAR-car10.days_to_return_a_car))

    def test_update_bookings(self):

        def internal_update_bookings(self, car10, demands, t, given_lost_days=0):
            demand_days = 0
            for demand in demands:
                start, end = demand
                demand_days += (end - start)
            day_cars_before = np.count_nonzero(car10.cars_booked)
            car10.update_booking(demands, t=t)
            #print(car10.cars_booked)
            day_cars_after = np.count_nonzero(car10.cars_booked)
            lost_days = 0
            for demand in car10.lost_demands:
                _, start, end = demand
                lost_days += (end - start)
            self.assertEqual(day_cars_after-day_cars_before+lost_days, demand_days)
            self.assertEqual(lost_days, 0)

        car = rc.RentalCar(max_cars=8, start_cars=3)
        demands = [(2, 7)]

        '''
        internal_update_bookings(self, car, demands, t)

        demands = [(2, 7), (3, 8), (4, 9)]
        internal_update_bookings(self, car, demands, t)
        '''

        car = rc.RentalCar(max_cars=5, start_cars=5)
        demands = [(2, 3), (3, 8), (1, 3)]
        t = 0
        print(car.cars_booked)
        internal_update_bookings(self, car, demands, t, given_lost_days=0)
        print(car.cars_booked)



if __name__ == '__main__':
    unittest.main()

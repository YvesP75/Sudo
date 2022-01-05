import numpy as np

from parameters import *


class RentalCar:

    def __init__(self, max_cars=MAX_CARS, start_cars=START_CARS):
        self.max_cars = max_cars

        # car costs
        self.car_cost_per_day = CAR_COST_PER_DAY
        self.car_cost_per_booking = CAR_COST_PER_DAY_BOOKING
        self.car_cost_one_off = CAR_COST_PER_ONE_OFF
        self.car_cost_per_day_in_carpark = CAR_COST_PER_DAY_IN_CARPARK

        # time to get or return a car, e.g. to VW
        self.days_to_get_a_car = DAYS_TO_GET_A_CAR
        self.days_to_return_a_car = DAYS_TO_RETURN_A_CAR

        # start with no car booked
        self.cars_booked = np.zeros((self.max_cars, DAYS_IN_YEAR), dtype=bool)
        self.bookings_of_the_day = 0  # booking of the day

        # start with baseline demand in carpark
        self.cars_in_carpark = np.zeros((self.max_cars, DAYS_IN_YEAR), dtype=bool)
        self.cars_in_carpark[:start_cars, :] = True
        self.car_added_to_carpark = 0

        # financial KPIs
        self.revenues = np.zeros(DAYS_IN_YEAR, dtype=np.float32)
        self.costs = np.zeros(DAYS_IN_YEAR, dtype=np.float32)
        self.benefits = np.zeros(DAYS_IN_YEAR, dtype=np.float32)

        self.day_revenue = np.zeros((DAYS_IN_YEAR, DAYS_IN_YEAR), dtype=np.float32)  # revenue in d2 created in d1
        self.day_revenue_loss = np.zeros((DAYS_IN_YEAR, DAYS_IN_YEAR), dtype=np.float32)  # idem for lost revenue
        self.day_cost = np.zeros((DAYS_IN_YEAR, DAYS_IN_YEAR), dtype=np.float32)  # idem for costs

        # lost demands
        self.lost_demands = np.zeros((0, 3), dtype=int)

    def update_carpark(self, car_variation: int, t: int):
        if t == DAYS_IN_YEAR or car_variation == 0:
            pass
        else:
            if car_variation < 0:
                self.carpark_return(-1 * car_variation, t)
            else:
                self.carpark_add(car_variation, t)

    def carpark_add(self, car_variation: int, t: int):

        horizon = min(t+self.days_to_get_a_car, DAYS_IN_YEAR)
        non_active_cars = 1 - np.sum(self.cars_in_carpark[:, horizon:], axis=1, dtype=bool)
        if np.count_nonzero(non_active_cars) < car_variation:
            # print('hum, sorry, impossible to get new cars, we have reached the limit')
            car_variation = np.count_nonzero(non_active_cars)

        self.cars_in_carpark[np.nonzero(non_active_cars)[0][:car_variation], horizon:] = True
        self.car_added_to_carpark = car_variation
        self.day_cost[t, horizon:] += self.car_cost_per_day_in_carpark
        self.day_cost[t, t] += self.car_cost_one_off

    def carpark_return(self, car_variation: int, t: int):

        cars_returnable = np.product(((1 - self.cars_booked) * self.cars_in_carpark)[:, t+self.days_to_return_a_car:],
                                     axis=1, dtype=bool)
        if np.count_nonzero(cars_returnable) < car_variation:
            # print('hum, sorry, impossible to return all required cars, we have reached the limit')
            car_variation = np.count_nonzero(cars_returnable)
        self.cars_in_carpark[np.nonzero(cars_returnable)[0][-car_variation:], t+self.days_to_return_a_car:] = False

    def update_booking(self, demands, prices, t: int = 0):
        self.bookings_of_the_day = 0
        p1, p2, p3 = prices
        for demand in demands:
            start, end = demand
            end = min(end, DAYS_IN_YEAR)
            start = min(start, end-1)
            assert 0 <= t <= start, "start should come after t ... and after 0"
            assert start < end, "start should come before end and respect boundaries"
            p = p1 if start == t else p2 if start - t < 10 else p3
            car_bookable = ((1 - self.cars_booked) * self.cars_in_carpark)[:, start:end]
            cars = np.nonzero(np.sum(car_bookable, axis=1) == (end - start))[0]
            if 0 < len(cars):
                self.cars_booked[cars[0], start:end] = True
                self.bookings_of_the_day += 1

                # update revenues and costs
                self.day_revenue[t, start:end] += p
                self.day_cost[t, start:end] += self.car_cost_per_day
                self.day_cost[t, start] += self.car_cost_per_booking

            else:  # no car is available
                lost_demand = t, start, end
                self.lost_demands = np.vstack((self.lost_demands, lost_demand))
                self.day_revenue_loss[t, start:end] += p

    def get_financials(self, t: int = 0):

        day_revenues = np.sum(self.day_revenue[t, :])
        day_costs = np.sum(self.day_cost[t, :])
        day_benefits = day_revenues - day_costs

        return day_revenues, day_costs, day_benefits

    def get_observations(self, t: int = 0):

        periods = np.insert(2**np.arange(8), 0, 0)

        obs_carpark = np.zeros(8)
        obs_booking = np.zeros(8)

        for i in range(8):
            start = min(t+periods[i], DAYS_IN_YEAR)
            end = min(t + periods[i+1], DAYS_IN_YEAR)
            obs_carpark[i] = np.sum(self.cars_in_carpark[:, start:end])
            if 0 < obs_carpark[i]:
                obs_booking[i] = np.sum(self.cars_booked[:, start:end]) / obs_carpark[i]
            else:
                obs_booking[i] = 0
            obs_carpark[i] /= ((DAYS_IN_YEAR - t) * self.max_cars)
        obs = np.hstack((obs_carpark * 2 - 1, obs_booking * 2 - 1))

        return obs

    def get_reward(self, t: int = 0, p=0.):
        _, _, reward = self.get_financials(t=t)
        return reward

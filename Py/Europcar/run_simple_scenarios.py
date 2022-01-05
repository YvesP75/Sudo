import numpy as np
from stable_baselines3 import SAC

from rental_env import RentalEnv
from parameters import *



day_carpark = np.zeros((DAYS_IN_YEAR, MAX_CARS, DAYS_IN_YEAR), dtype=int)
day_booking = np.zeros((DAYS_IN_YEAR, MAX_CARS, DAYS_IN_YEAR), dtype=int)



env = RentalEnv()


# Test the trained agent
obs = env.reset()
total_reward = 0

car_variation = 0
p1 = 1
p2 = 1
p3 = 1
prices = p1, p2, p3

done = False
step = 0

while not done:
    car_variation = 10 if step == 5 else 0
    car_variation = -5 if step == 8 else car_variation
    car_variation = 5 if step == 9 else car_variation

    if step == 6:
        env.greens.update_booking(demands=[(9, 16)], prices=prices, t=step)

    if step == 10:
        env.greens.update_booking(demands=[(12, 18), (15, 17), (15, 17), (15, 18), (17, 18),], prices=prices, t=step)

    action = car_variation, p1, p2, p3
    _, _, done, _ = env.step(action)
    day_carpark[step, :, :] = env.greens.cars_in_carpark
    day_booking[step, :, :] = env.greens.cars_booked
    step += 1

rev = env.greens.day_revenue
rev_nonzero = np.nonzero(rev)
revenue_matrix = np.vstack((rev_nonzero, rev[rev_nonzero])).T

zed = day_carpark.astype(int) + 2 * day_booking.astype(int)

np.save('zzed', zed)
np.save('rev_matrix', revenue_matrix)

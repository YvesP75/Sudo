
import numpy as np
from stable_baselines3 import SAC

from rental_env import RentalEnv
from parameters import *

env = RentalEnv()

model = SAC.load("SAC5000")


# Test the trained agent
obs = env.reset()
total_reward = 0



day_carpark = np.zeros((DAYS_IN_YEAR, MAX_CARS, DAYS_IN_YEAR), dtype=bool)
day_booking = np.zeros((DAYS_IN_YEAR, MAX_CARS, DAYS_IN_YEAR), dtype=bool)

for step in range(DAYS_IN_YEAR):

  action, _ = model.predict(obs, deterministic=True)
  print("Step {}".format(step + 1))
  car_variation = int(round((action[0] + 1 / 2) * MAX_CARS))
  p1 = round((1 + (action[1] + 1)) * NOMINAL_PRICE)
  p2 = round((1 + (action[2] + 1)) * NOMINAL_PRICE)
  p3 = round((1 + (action[3] + 1)) * NOMINAL_PRICE)
  #print("Action: ", car_variation, p1, p2, p3)
  obs, reward, done, info = env.step(action)
  total_reward += reward
  obs = 2 * obs + 1
  # print('carpark=', np.round(obs[:8]*100))
  # print('booking=', np.round(obs[8:]*100))
  # print('reward=', reward)
  day_carpark[step, :, :] = env.greens.cars_in_carpark
  day_booking[step, :, :] = env.greens.cars_booked
  if done:
      if total_reward < 0:
          print("hum, we lost money, reward=", total_reward)
      else:
          print("yeah, reward=", total_reward)
      break

mesh = np.meshgrid(range(MAX_CARS), range(DAYS_IN_YEAR))
x, y = mesh
zed = 1. * day_carpark[:, x, y] + 2. * day_booking[:, x, y]

np.save('mesh', mesh)
for day in range(DAYS_IN_YEAR):
    np.save(f'zed{day}', zed[day, :, :])





from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3 import SAC
from stable_baselines3.sac.policies import MlpPolicy
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_checker import check_env
import os

import numpy as np

from parameters import *
from rental_env import RentalEnv

# Instantiate the env
env = RentalEnv()

model = SAC('MlpPolicy', env, verbose=1).learn(LEARNING_DAYS)



model.save("SAC5000")

# Test the trained agent
obs = env.reset()
for step in range(DAYS_IN_YEAR):
  action, _ = model.predict(obs, deterministic=True)
  print("Step {}".format(step + 1))
  car_variation = int(round((action[0] + 1 / 2) * MAX_CARS))
  p1 = (1 + (action[1] + 1)) * NOMINAL_PRICE
  p2 = (1 + (action[2] + 1)) * NOMINAL_PRICE
  p3 = (1 + (action[3] + 1)) * NOMINAL_PRICE
  print("Action: ", car_variation, p1, p2, p3)
  obs, reward, done, info = env.step(action)
  obs = 2 * obs + 1
  print('carpark=', np.round(obs[:8]*100))
  print('booking=', np.round(obs[8:]*100))
  print('reward=', reward)
  if done:
      if reward < 0:
          print("hum, we lost money, reward=", reward)
      else:
          print("yeah, reward=", reward)
      break
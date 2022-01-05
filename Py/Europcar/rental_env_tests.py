from stable_baselines3.common.env_checker import check_env
from rental_env import RentalEnv

env = RentalEnv()
obs = env.reset()

# If the environment don't follow the interface, an error will be thrown
check_env(env, warn=True)

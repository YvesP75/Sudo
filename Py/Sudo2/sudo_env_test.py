from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO, A2C
import numpy as np

from sudo_env import SudoEnv

env = SudoEnv()
# check_env(env)

#model = PPO.load("sudo_model_test")
model = False

# Test the trained agent
obs = env.reset()

n_steps = 30
cumul_reward = 0
for step in range(n_steps):
    if model:
        action, _ = model.predict(obs, deterministic=False)
    else:
        action = np.random.randint(18)
    obs, reward, done, info = env.step(action)
    print("Step {}".format(step + 1))
    block, line = divmod(action, 2)
    raw_ll, raw_cc = divmod(block, 3)
    ll = env.sudo.line_permutation[raw_ll]
    cc = env.sudo.column_permutation[raw_cc]
    raw_numbers_found = info['numbers_found']
    numbers_found = env.sudo.number_permutation[np.arange(9)[raw_numbers_found] + 1]
    if 0 < np.count_nonzero(numbers_found):
        print("numéros trouvés : ", numbers_found)
        if (line == 0):
            print("Action: inférence sur la colonne  sur le bloc: ", ll, cc)
        else:
            print("Action: inférence sur la ligne sur le bloc: ", ll, cc)
        env.sudo.print()
        print(f"cumulated reward {cumul_reward:.1f}")
    else:
        print("...")
        if (line == 0):
            print("Action: inférence sur la colonne  sur le bloc: ", ll, cc)
        else:
            print("Action: inférence sur la ligne sur le bloc: ", ll, cc)


    cumul_reward += reward
    print(f" reward {reward:.1f}")

    if done:
        # Note that the VecEnv resets automatically
        # when a done signal is encountered
        sudogrid = env.sudo
        env.sudo.print()
        print(f"cumulated reward {cumul_reward:.1f}")
        break




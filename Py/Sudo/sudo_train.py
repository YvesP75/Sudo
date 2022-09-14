from stable_baselines3 import A2C, PPO


from sudo_env import SudoEnv

env = SudoEnv()

model = PPO('MlpPolicy', env, verbose=1).learn(500000)
model.save('sudo_model_n')

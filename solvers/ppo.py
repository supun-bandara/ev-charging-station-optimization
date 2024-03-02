import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from stable_baselines3 import PPO
import os
from charging_station.environment.env import ChargingEnv
import time

models_dir = f"models/{int(time.time())}/"
logdir = f"logs/{int(time.time())}/"

if not os.path.exists(models_dir):
	os.makedirs(models_dir)

if not os.path.exists(logdir):
	os.makedirs(logdir)

env = ChargingEnv()
env.reset()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir, n_steps=64000)

TIMESTEPS = 20000
iters = 0
while True:		
	iters += 1
	model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
	model.save(f"{models_dir}/{TIMESTEPS*iters}")
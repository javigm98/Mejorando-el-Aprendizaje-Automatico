import training
import ray
import ray.rllib.agents.ppo as ppo
import json, os, shutil, sys
import gym
import pprint
import time
import shelve
from tensorflow import keras
from ray import tune

shutil.rmtree('~/ray_results', ignore_errors = True, onerror = False)
ray.shutdown()
ray.init()
config = ppo.DEFAULT_CONFIG.copy()
config['num_workers'] = 8 
agent = ppo.PPOTrainer(env='Pong-v0')
policy=agent.get_policy()
print(policy.model.model_config)
print(policy.model.base_model.summary())

print("Configuración del agente:\n\n" + str(config))
print("\nConfiguración del modelo del agente:\n\n" + str(config["model"]))

t0 = time.time()
checkpoint_root='./checkpoints/model1'
n_iter = int(sys.argv[1])
save_file = sys.argv[2]
training.full_train(checkpoint_root, agent, n_iter)
t1 = time.time()-t0
print("Total time for the " + str(n_iter) + " training iterations: " + str(t1))
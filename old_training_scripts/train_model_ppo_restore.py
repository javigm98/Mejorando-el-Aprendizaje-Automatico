import training_ppo as training
import ray
import ray.rllib.agents.ppo as ppo
import json, os, shutil, sys
import gym
import pprint
import time
import shelve
from tensorflow import keras
from ray import tune

#shutil.rmtree('~/ray_results', ignore_errors = True, onerror = False)
ray.shutdown()
ray.init()
model = sys.argv[1]
config = ppo.DEFAULT_CONFIG.copy()
num_workers = int(sys.argv[2])
config['num_workers'] = num_workers

if model == 'model1':
    save_file = './training_results/ppo/model1/model1_results'
    checkpoint_root='./checkpoints/ppo/model1'
elif model == 'model2':
    config['model']['dim'] = 168
    config['model']['conv_filters'] = [[16, [16, 16], 8],[32, [4, 4], 2],[256, [11, 11], 1]]
    save_file = './training_results/ppo/model2/model2_results'
    checkpoint_root='./checkpoints/ppo/model2'
elif model == 'model3':
    config['model']['dim'] = 252
    config['model']['conv_filters'] = [[16, [8, 8], 4],[16, [8, 8], 4], [32, [4, 4], 2], [256, [8, 8], 1]]
    save_file = './training_results/ppo/model3/model3_results'
    checkpoint_root='./checkpoints/ppo/model3'
elif model == 'model4':
    config['model']['dim'] = 168
    config['model']['conv_filters'] = [[16, [8, 8], 4],[32, [4, 4], 2],[32, [4, 4], 2], [256, [11, 11], 1]]
    save_file = './training_results/ppo/model4/model4_results'
    checkpoint_root='./checkpoints/ppo/model4'
elif model == 'model5':
    config['model']['dim'] = 252
    config['model']['conv_filters'] = [[16, [8, 8], 4],[32, [4, 4], 2], [32, [4, 4], 2], [256, [16, 16], 1]]
    save_file = './training_results/ppo/model5/model5_results'
    checkpoint_root='./checkpoints/ppo/model5'
elif model == 'model6':
    config['model']['dim'] = 168
    config['model']['conv_filters'] = [[16, [8, 8], 4],[32, [4, 4], 2],[256, [21, 21], 1]]
    save_file = './training_results/ppo/model6/model6_results'
    checkpoint_root='./checkpoints/ppo/model6'

agent = ppo.PPOTrainer(config, env='Pong-v0')
policy=agent.get_policy()
print(policy.model.model_config)
print(policy.model.base_model.summary())

print("Configuración del agente:\n\n" + str(config))
print("\nConfiguración del modelo del agente:\n\n" + str(config["model"]))

t0 = time.time()
n_iter = int(sys.argv[3])
restore_file = sys.argv[4]
n_ini=int(sys.argv[5])
training.full_train(checkpoint_root, agent, n_iter, save_file, n_ini = n_ini, header = False, restore = True, restore_dir = restore_file)
t1 = time.time()-t0
print("Total time for the " + str(n_iter) + " training iterations: " + str(t1))
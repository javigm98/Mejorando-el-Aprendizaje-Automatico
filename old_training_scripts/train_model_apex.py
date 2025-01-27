import training_apex as training
import ray
import ray.rllib.agents.dqn.apex as apex
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
model = sys.argv[1]
config = apex.APEX_DEFAULT_CONFIG.copy()
num_workers = int(sys.argv[2])
config['num_workers'] = num_workers
config['num_gpus'] = 1
config['buffer_size'] = 2000

if model == 'model1':
    save_file = './training_results/apex/model1/model1_results_gpu'
    checkpoint_root='./checkpoints/apex/model1_gpu'
elif model == 'model2':
    config['model']['dim'] = 168
    config['model']['conv_filters'] = [[16, [16, 16], 8],[32, [4, 4], 2],[256, [11, 11], 1]]
    save_file = './training_results/apex/model2/model2_results_gpu'
    checkpoint_root='./checkpoints/apex/model2_gpu'
elif model == 'model3':
    config['model']['dim'] = 252
    config['model']['conv_filters'] = [[16, [8, 8], 4],[16, [8, 8], 4], [32, [4, 4], 2], [256, [8, 8], 1]]
    save_file = './training_results/apex/model3/model3_results_gpu'
    checkpoint_root='./checkpoints/apex/model3_gpu'
elif model == 'model4':
    config['model']['dim'] = 168
    config['model']['conv_filters'] = [[16, [8, 8], 4],[32, [4, 4], 2],[32, [4, 4], 2], [256, [11, 11], 1]]
    save_file = './training_results/apex/model4/model4_results_gpu'
    checkpoint_root='./checkpoints/apex/model4_gpu'
elif model == 'model5':
    config['model']['dim'] = 252
    config['model']['conv_filters'] = [[16, [8, 8], 4],[32, [4, 4], 2], [32, [4, 4], 2], [256, [16, 16], 1]]
    save_file = './training_results/apex/model5/model5_results_gpu'
    checkpoint_root='./checkpoints/apex/model5_gpu'
elif model == 'model6':
    config['model']['dim'] = 168
    config['model']['conv_filters'] = [[16, [8, 8], 4],[32, [4, 4], 2],[256, [21, 21], 1]]
    save_file = './training_results/apex/model6/model6_results_gpu'
    checkpoint_root='./checkpoints/apex/model6_gpu'

agent = apex.ApexTrainer(config, env='Pong-v0')
policy=agent.get_policy()
print(policy.model.model_config)
print(policy.model.base_model.summary())

print("Configuración del agente:\n\n" + str(config))
print("\nConfiguración del modelo del agente:\n\n" + str(config["model"]))

t0 = time.time()
n_iter = int(sys.argv[3])
training.full_train(checkpoint_root, agent, n_iter, save_file)
t1 = time.time()-t0
print("Total time for the " + str(n_iter) + " training iterations: " + str(t1))
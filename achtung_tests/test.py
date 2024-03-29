import time
import numpy as np
import pickle
import matplotlib.pyplot as plt
from stable_baselines3.common.evaluation import evaluate_policy


ITERATIONS = 150
LEARN_STEP = 100
EVALUATE_POLICY_EPISODES = 100

def test_and_save(paramas):
    start_time = time.time()
    (model, model_name) = paramas
    rewards = []
    reward_stds = []
    lengths = []
    length_stds = []
    for i in range(ITERATIONS):
        print("iteration: ", i+1)
        model.learn(total_timesteps=LEARN_STEP)
        # mean_reward, std_reward = evaluate_policy(model, model.env, n_eval_episodes=EVALUATE_POLICY_EPISODES)
        episode_rewards, episode_lengths = evaluate_policy(model, model.env, n_eval_episodes=EVALUATE_POLICY_EPISODES, return_episode_rewards= True)

        mean_reward = np.mean(episode_rewards)
        std_reward = np.std(episode_rewards)
        mean_length = np.mean(episode_lengths)
        std_length = np.std(episode_lengths)
        
        print(f"   mean_reward :{mean_reward:.2f} +/- {std_reward:.2f}")
        print(f"   mean_length :{mean_length:.2f} +/- {std_length:.2f}")
        
        rewards.append(mean_reward)
        reward_stds.append(std_reward)
        lengths.append(mean_length)
        length_stds.append(std_length)
        
    print("   saving...")

    with open(f"./achtung_tests/results/test_{model_name}_reward", "wb") as f:   
        pickle.dump(rewards, f)
    with open(f"./achtung_tests/results/test_{model_name}_reward_std", "wb") as f:   
        pickle.dump(reward_stds, f)
    with open(f"./achtung_tests/results/test_{model_name}_length", "wb") as f:   
        pickle.dump(lengths, f)
    with open(f"./achtung_tests/results/test_{model_name}_length_std", "wb") as f:   
        pickle.dump(length_stds, f)

    model.save(f"./achtung_tests/models/{model_name}")
    
    print("   saved")
    print("--- %s seconds ---" % (time.time() - start_time))

    
def read_and_show_graph(model_name):
    with open(f"./achtung_tests/results/test_{model_name}_reward", "rb") as f:   
        rewards = np.array(pickle.load(f))
    with open(f"./achtung_tests/results/test_{model_name}_reward_std", "rb") as f:   
        rewards_stds = np.array(pickle.load(f))

    with open(f"./achtung_tests/results/test_{model_name}_length", "rb") as f:   
        lengths = np.array(pickle.load(f))
    with open(f"./achtung_tests/results/test_{model_name}_length_std", "rb") as f:   
        length_stds = np.array(pickle.load(f))

    range_x = list(range(LEARN_STEP,(ITERATIONS+1)*LEARN_STEP,LEARN_STEP))

    my_dpi= 100
    plt.figure(figsize=(1000/my_dpi, 600/my_dpi), dpi=my_dpi)
    plt.plot(range_x, rewards)
    plt.xlabel('epoch')
    plt.ylabel('episode reward')
    plt.title(model_name)

    plt.fill_between(range_x,rewards-rewards_stds,rewards+rewards_stds,alpha=.3)
    plt.savefig(f'./achtung_tests/plots/{model_name}_rewards.png')
    plt.close()
    
    my_dpi= 100
    plt.figure(figsize=(1000/my_dpi, 600/my_dpi), dpi=my_dpi)
    plt.plot(range_x,lengths)
    plt.xlabel('epoch')
    plt.ylabel('episode length')
    plt.title(model_name)

    plt.fill_between(range_x,lengths-length_stds,lengths+length_stds,alpha=.3)
    plt.savefig(f'./achtung_tests/plots/{model_name}_lengths.png')


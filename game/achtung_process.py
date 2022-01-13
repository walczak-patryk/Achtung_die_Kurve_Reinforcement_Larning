import gym
import numpy as np
import matplotlib.pyplot as plt
from game.achtung import Achtung
from game.common import prepro

class AchtungProcess(gym.Env):
    def __init__(self, n=1, frame_skip=4, obs_len=4, _id = 0, height = 80, width= 80):
      self.env = Achtung(n,_id,speed=0,render_game=False, height=height, width=width)
      self.frame_skip = frame_skip
      self.obs_len = obs_len
      self.state = np.zeros((self.obs_len, self.env.window_width, self.env.window_height))
      self.action_space = gym.spaces.Discrete(3)
      self.observation_space = gym.spaces.Box(low=0, high=255,
        shape=(3, self.env.window_width, self.env.window_height), dtype=np.uint8)

    def step(self, action):
      _obs = []
      _reward = []
      done = False
      for t in range(self.frame_skip):
          obs, reward, done, info = self.env.step(action)
          # print("   r = ",reward)
          _obs.append(obs)
          _reward.append(reward)

          if done:
            break

      obs_new = np.maximum(_obs[-1], _obs[-2] if len(_obs) > 1 else _obs[-1])
      self.state = np.roll(self.state, shift=-1,axis=0)
      self.state[-1] = obs_new

      return self.state, np.sum(_reward), done, {}   

    def reset(self):
      self.state = np.zeros((self.obs_len, self.env.window_width, self.env.window_height))
      obs = self.env.reset()
      self.state[-1] = obs[:,:,0]

      return self.state

    def render(self):
      self.env.render()


# env = AchtungProcess(1)
# env.env.render_game = True
# env.env.speed = 0
# obs = env.reset()

# n_games = 0
# running_reward = []
# rewards = []

# while n_games < 100:
#     # Random action
#     action = env.action_space.sample() + 1
#     print("action: ", action)
#     obs, reward, done, info = env.step(action)
#     running_reward.append(reward)

#     if done:
#         rewards.append(sum(running_reward))
#         running_reward = []
#         # filename = "images/game_{}".format(env.games-1)
#         # os.rename(filename, filename + "_{}".format(int(rewards[-1])))
#         obs = env.reset()
#         n_games += 1

# print("test complete")
# print("   reward (avg): ", np.mean(rewards))
# print("   reward (std): ", np.std(rewards))



import numpy as np

from tensorforce.environments import Environment
from tensorforce.agents import Agent
from tensorforce.execution import Runner


class BasicEnv(Environment):
    """
    A basic environment implementing
    --------------------------------------------------------------------------------------------------------------------
        State: 4 arbitrary components
        Actions: 2 possible actions ('buy' or 'sell')
        Reward: The balance at step t (computed with simple addition of buy and subtraction of sell actions at each step)
        Terminal: A random boolean determining whether the episode has terminated or not
    --------------------------------------------------------------------------------------------------------------------
    N.B When initialising the environment it is recommended to utilize the create functionality of the Environment class
    e.g.
    env = Environment.create(
        environment=BasicEnv
    )
    and not
    env = BasicEnv()
    """

    def __init__(self):
        super().__init__()
        self.balance = 0

    def states(self):
        return dict(type='float', shape=(4,))

    def actions(self):
        return {
            'buy': dict(type='float', min_value=0.0, max_value=1.0),
            'sell': dict(type='float', min_value=0.0, max_value=1.0)
        }

    def reset(self, num_parallel=None):
        self.balance = 0
        state = np.ones((4,))
        return state

    def execute(self, actions):
        next_state = self.compute_timestep(actions)
        terminal = self.terminal()
        reward = self.reward()
        return next_state, terminal, reward

    # OPTIONAL
    def max_episode_timesteps(self):
        return 50

    def close(self):
        super().close()

    # HELPER FUNCTIONS
    def terminal(self):
        return np.random.uniform() < 0.05

    def reward(self):
        return self.balance

    def compute_timestep(self, actions):
        self.balance += actions['buy']
        self.balance -= actions['sell']
        return np.ones((4,))


# ----------------------------------------------------------------------------------------------------------------------
# EXAMPLE RUN
# ----------------------------------------------------------------------------------------------------------------------
env = Environment.create(
    environment=BasicEnv
)

agent = Agent.create(
    agent='tensorforce',
    environment=env,
    update=64,
    optimizer=dict(optimizer='adam', learning_rate=1e-3),
    objective='policy_gradient',
    reward_estimation=dict(horizon=20),
    summarizer=dict(
        directory='results/CustomEnv/logs/summaries',
        summaries='all'
    )
)

runner = Runner(
    agent=agent,
    environment=env
)

runner.run(num_episodes=300)

runner.run(num_episodes=100, evaluation=True)

runner.close()
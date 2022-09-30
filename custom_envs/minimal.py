from tensorforce.environments import Environment


class MinimalEnv(Environment):
    """
    A minimal tensorforce environment, that could be used as a template environment.
    --------------------------------------------------------------------------------------------------------------------
    This environment has two property methods (states and actions), which enable a RL agent to be
    agnostic to inputs and outputs as long as the agent is initialised with the environment.

    The environment also has two interaction methods (reset and execute), which is the expected interface
    for the RL agent to interact with the custom environment and thus execution can be performed with a runner utility.
    """
    def __init__(self):
        super().__init__()

    def states(self):
        return

    def actions(self):
        return

    def reset(self, num_parallel=None):
        return

    def execute(self, actions):
        next_state = ...
        terminal = ...
        reward = ...
        return next_state, terminal, reward

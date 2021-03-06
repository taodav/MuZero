from typing import List

import gym

from game.game import Action, AbstractGame
from game.gym_wrappers import ScalingObservationWrapper

class Acrobot(AbstractGame):
    """
    Gym Acrobot environment
    """

    def __init__(self, discount: float, **kwargs):
        super(Acrobot, self).__init__(discount)
        id = 'AcrobotModified-v1'
        entry_point = 'deer.helper.gym_env:ContinuableAcrobotEnv'

        max_steps = kwargs.get('max_steps', 200)
        gym.envs.register(
            id=id,
            entry_point=entry_point,
            max_episode_steps=max_steps,
        )
        self.env = gym.make(id)

        self.env = ScalingObservationWrapper(self.env, low=[-2.4, -2.0, -0.42, -3.5], high=[2.4, 2.0, 0.42, 3.5])
        self.actions = list(map(lambda i: Action(i), range(self.env.action_space.n)))
        self.observations = [self.env.reset()]
        self.done = False

    @property
    def action_space_size(self) -> int:
        """Return the size of the action space."""
        return len(self.actions)

    def step(self, action) -> int:
        """Execute one step of the game conditioned by the given action."""
        observation, reward, done, _ = self.env.step(action.index)
        self.observations += [observation]
        self.done = done
        return reward

    def terminal(self) -> bool:
        """Is the game is finished?"""
        return self.done

    def legal_actions(self) -> List[Action]:
        """Return the legal actions available at this instant."""
        return self.actions

    def make_image(self, state_index: int):
        """Compute the state of the game."""
        return self.observations[state_index]



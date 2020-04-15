import utility
import random

# 1 Stroke Reward For Each Action
reward = 1


def model_based_rl():
    counter = 0

    for state in utility.states.values():
        while counter < 1001:
            for action in state.avail_actions:
                sel_action_result(state,action)
            counter += 1

    establish_transition_prob(state, counter)

    # Determine Policy


def sel_action_result(state, action):
    rand_val = random.random()
    accum = 0
    for result in state.avail_actions[action]:
        accum += state.avail_actions[action][result]
        if rand_val <= accum:
            state.transition_track[action][result] += 1
            state.reward_track[action] += utility.rewards[result]
            return


def establish_transition_prob(ste, count):
    for act in ste.avail_actions:
        for result in ste.avail_actions[act]:
            # Need to be a float
            ste.transition_track[act][result] /= count

import utility
import random


def model_based_rl():

    for state in utility.states.values():
        counter = 0

        while counter < 1001:

            for action in state.avail_actions:
                sel_action_result(state, action)

            counter += 1

        establish_transition_prob(state, counter)

        # Determine Policy
        policy = determine_policy(state)

        print_stats(state)
        print('Recommended Action', end=': ')
        print(policy)


def sel_action_result(ste, action):
    rand_val = random.random()
    accum = 0
    for result in ste.avail_actions[action]:
        accum += ste.avail_actions[action][result]
        if rand_val <= accum:
            ste.transition_track[action][result] += 1
            ste.reward_track[action] += utility.rewards[result]
            return


def establish_transition_prob(ste, count):
    for act in ste.avail_actions:
        ste.reward_track[act] /= count

        for result in ste.avail_actions[act]:
            # Need to be a float
            ste.transition_track[act][result] /= count


def determine_policy(ste):
    best_action = ''
    comparator = 1000000000
    for act in ste.reward_track:
        if ste.reward_track[act] < comparator:
            comparator = ste.reward_track[act]
            best_action = act

    return best_action


def print_stats(ste):
    print(ste)
    print('Available Actions', end=': ')
    print(ste.avail_actions)
    print('Transition Probabilities', end=': ')
    print(ste.transition_track)
    print('Rewards Proposition For Each Action', end=': ')
    print(ste.reward_track)

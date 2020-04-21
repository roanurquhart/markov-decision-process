import utility
import random
import math


def model_based_rl():
    discount = 0.9
    reward = 1

    for state in utility.states.values():
        counter = 0
        # Establish transition probabilities
        while counter < 1001:
            for action in state.avail_actions:
                sel_action_result(state, action)
            counter += 1
        establish_transition_prob(state, counter)

        # Calculate Utility Values
        baseline = dict(utility.based_rewards)
        converged = False
        while not converged:
            utility.calc_utility(state, discount, reward)
            converged = check_for_convergence(baseline, utility.based_rewards)
            baseline = dict(utility.based_rewards)

        # Determine Policy
        policy = determine_policy(state)

        print_stats(state)
        print('Recommended Policy', end=': ')
        print(policy)


def sel_action_result(ste, action):
    rand_val = random.random()
    accum = 0
    for result in ste.avail_actions[action]:
        accum += ste.avail_actions[action][result]
        if rand_val <= accum:
            ste.transition_track[action][result] += 1
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


# Returns True if converged
def check_for_convergence(baseline, new_baseline):
    for ste in baseline:
        if not math.isclose(baseline[ste], new_baseline[ste]):
            return False
    return True


def print_stats(ste):
    print(ste)
    # print('Available Actions', end=': ')
    # print(ste.avail_actions)
    # print('Transition Probabilities', end=': ')
    # print(ste.transition_track)
    print('Rewards Proposition For Each Action', end=': ')
    print(ste.reward_track)

import utility
import random


model_based_states = {}


def model_based_rl():
    discount = 0.9
    reward = 1
    explore = 0.2
    # Create a copy of states dict for local use
    global model_based_states
    model_based_states = utility.set_up_local_states()

    for state in model_based_states.values():
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
            utility.calc_utility(state, discount, reward, explore)
            converged = utility.check_for_convergence(baseline, utility.based_rewards)
            baseline = dict(utility.based_rewards)


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






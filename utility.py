import math
import random
import model_free
import model_based

states = {}
actions = []
based_rewards = {'Fairway': 1, 'Ravine': 1, 'Close': 1, 'Same': 1, 'Left': 1, 'Over': 1, 'In': 0}
free_rewards = {'Fairway': 1, 'Ravine': 1, 'Close': 1, 'Same': 1, 'Left': 1, 'Over': 1, 'In': 0}


class State:
    def __init__(self, name):
        self.name = name
        self.avail_actions = {}
        self.transition_track = {}
        self.reward_track = {}

    def __repr__(self):
        return "<State: %s>" % self.name

    def __str__(self):
        return "State: %s" % self.name


def parse_input(data):
    counter = 0
    state = State('init')

    while counter < len(data):

        temp = data[counter]
        segmented = temp.split('/')

        if segmented[0] not in states:
            state = State(segmented[0])
            states[segmented[0]] = state

        if segmented[1] not in state.avail_actions:
            # Nested dictionary - {Action: {newState: probability}}
            state.avail_actions[segmented[1]] = {}
            state.transition_track[segmented[1]] = {}
            state.reward_track[segmented[1]] = 0

        state.avail_actions[segmented[1]][segmented[2]] = float(segmented[3].rstrip())
        state.transition_track[segmented[1]][segmented[2]] = 0

        counter += 1


def print_solution(data):
    counter = 0
    # for state in states.values():
    #     print_stats(state)

    while counter < len(data):

        temp = data[counter]
        segmented = temp.split('/')

        m_based_state = model_based.model_based_states[segmented[0]]
        m_based_trans = m_based_state.transition_track[segmented[1]][segmented[2]]

        m_free_state = model_free.model_free_states[segmented[0]]
        m_free_utility = m_free_state.reward_track[segmented[1]]

        print(temp)
        print('Model Based', end=': ')
        print('Transition Probability: ' + str(m_based_trans), end=', ')
        if not segmented[2] == 'In':
            print('Recommended Policy: ' + determine_policy(model_based.model_based_states[segmented[2]]))
        else:
            print('Recommended Policy: ' + 'You have successfully completed the hole')
        print('Model Free', end=': ')
        print('Utility Value: ' + str(m_free_utility), end=', ')
        if not segmented[2] == 'In':
            print('Recommended Policy: ' + determine_policy(model_free.model_free_states[segmented[2]]))
        else:
            print('Recommended Policy: ' + 'You have successfully completed the hole')
        print('')

        counter += 1


# Calculate utility values for a state's available actions and assign overall utility
def calc_utility(state, discount, reward, explore_val):
    val = 0
    min_util = 99999999999
    all_vals = []
    # Available actions
    for action in state.avail_actions:

        # Possible outcome states of action
        for ste in state.avail_actions[action]:

            # Calculate weighted utility value for given state
            val += state.transition_track[action][ste] * based_rewards[ste]

        # Track utility of given action
        state.reward_track[action] = (val * discount + reward)
        all_vals.append((val * discount + reward))

        # Store min utility value calculated as state's utility
        # Low utility is a better move
        if state.reward_track[action] < min_util:
            min_util = state.reward_track[action]

    # Explore vs Exploit Step
    # Given explore_val will determine the how often this happens
    if random.random() < explore_val:
        based_rewards[state.name] = random.sample(all_vals, 1)[0]
    else:
        based_rewards[state.name] = min_util


# Checks all actions and their associated utility values to determine policy
def determine_policy(ste):
    best_action = ''
    comparator = 1000000000
    for act in ste.reward_track:
        if ste.reward_track[act] < comparator:
            comparator = ste.reward_track[act]
            best_action = act

    return best_action


# Returns True if utility values converge
def check_for_convergence(baseline, new_baseline):
    for ste in baseline:
        if not math.isclose(baseline[ste], new_baseline[ste]):
            return False
    return True


def print_stats(ste):
    print(ste)
    print('Available Actions', end=': ')
    print(ste.avail_actions)
    print('Transition Probabilities', end=': ')
    print(ste.transition_track)
    print('Rewards Proposition For Each Action', end=': ')
    print(ste.reward_track)


def set_up_local_states():
    return dict(states)



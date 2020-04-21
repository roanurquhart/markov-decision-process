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

    states['In'] = State('In')


# Calculate utility values for a state's available actions and assign overall utility
def calc_utility(state, discount, reward):
    val = 0
    min_util = 99999999999
    # Available actions
    for action in state.avail_actions:
        # Possible outcome states of action
        for ste in state.avail_actions[action]:
            # Calculate weighted utility value for given state
            val += state.transition_track[action][ste] * based_rewards[ste]
        # Track utility of given action
        state.reward_track[action] = (val * discount + reward)
        # Store min utility value calculated as state's utility
        # Low utility is a better move
        if state.reward_track[action] < min_util:
            based_rewards[state.name] = state.reward_track[action]
            min_util = state.reward_track[action]


def check_changes_based_rewards():
    total = 0
    for val in based_rewards.values():
        total += val
    return total / len(based_rewards.values())



states = {}
actions = []
rewards = {'Fairway': 1, 'Ravine': 2, 'Close': 1, 'Same': 1, 'Left': 1, 'Over': 1, 'In': 0}


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

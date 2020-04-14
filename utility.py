states = {}
actions = []


class State:
    def __init__(self, name):
        self.name = name
        self.avail_actions = {}

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

        state.avail_actions[segmented[1]][segmented[2]] = float(segmented[3].rstrip())

        counter += 1

    states['In'] = State('In')

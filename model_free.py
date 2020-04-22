import utility


def model_free_rl():
    discount = 0.9
    reward = 1
    explore = 0.2

    for state in utility.states.values():
        state.transition_track = dict(state.avail_actions)

        # Calculate Utility Values
        baseline = dict(utility.free_rewards)
        converged = False
        while not converged:
            utility.calc_utility(state, discount, reward, explore)
            converged = utility.check_for_convergence(baseline, utility.free_rewards)
            baseline = dict(utility.free_rewards)

        # Determine Policy
        policy = utility.determine_policy(state)

        utility.print_stats(state)
        print('Recommended Policy', end=': ')
        print(policy)
from nqg_model.types import *
from functools import reduce

# Part 1. General definitions


def vote_from_quorum_delegation(user_quorum: list[UserUUID],
                                project_id: ProjectUUID,
                                action_matrix: ActionMatrix,
                                user_decisions: dict[UserUUID, Action],
                                params: NQGModelParams) -> Vote:
    """
    Compute the quorum agreement for the active participants
    """
    # Filter User quorum for actively voting users only.
    valid_delegates = [u
                       for u, d in user_decisions.items()
                       if d == Action.RoundVote
                       and u in user_quorum]

    # Select up to the max quorum selected delegates parameter
    if len(valid_delegates) > params['max_quorum_selected_delegates']:
        selected_delegates = valid_delegates[:
                                             params['max_quorum_selected_delegates']]
    else:
        selected_delegates = valid_delegates

    # Compute Quorum Agreement and Size.
    agreement = 0.0
    quorum_size = 0
    for delegate in selected_delegates:
        delegatee_actions = action_matrix.get(delegate, {})
        action = delegatee_actions.get(project_id, None)
        if action is not None:
            quorum_size += 1
            if action is Vote.Yes:
                agreement += params['quorum_agreement_weight_yes']
            elif action is Vote.No:
                agreement += params['quorum_agreement_weight_no']
            else:
                agreement += params['quorum_agreement_weight_abstain']

    # Compute Absolute and Relative agreement fractions
    absolute_agreement = agreement / params['max_quorum_selected_delegates']
    if quorum_size > 0:
        relative_agreement = agreement / quorum_size
    else:
        relative_agreement = 0.0

    # Resolve vote as per quorum consensus
    if abs(absolute_agreement) >= params['quorum_delegation_absolute_threshold']:
        if abs(relative_agreement) >= params['quorum_delegation_relative_threshold']:
            if relative_agreement > 0:
                return Vote.Yes
            else:
                return Vote.No
        else:
            return Vote.Abstain
    else:
        return Vote.Abstain


def power_from_neural_governance(uid: UserUUID,
                                 pid: ProjectUUID,
                                 neuron_layers: list[NeuronLayer],
                                 oracle_state: OracleState,
                                 initial_votes: float = 0.0,
                                 print_on_each_layer=False) -> VotingPower:
    """
    Computes a User Vote towards a Project as based on 
    a Feedforward implementation of Neural Governance for a strictly
    sequential network (no layer parallelism).
    """
    current_vote = initial_votes
    if print_on_each_layer:
        print(f"Layer {0}: {current_vote}")
    for i, layer in enumerate(neuron_layers):
        (neurons, layer_aggregator) = layer
        neuron_votes = []
        for (neuron_label, neuron) in neurons.items():
            (oracle_function, weighting_function) = neuron
            raw_neuron_vote = oracle_function(
                uid, pid, current_vote, oracle_state)
            neuron_votes.append(weighting_function(raw_neuron_vote))
        current_vote = layer_aggregator(neuron_votes)

        if print_on_each_layer:
            print(f"Layer {i+1}: {current_vote}")

    return current_vote

# Part 2. Specific definitions
# Prior Voting Bonus


def prior_voting_score(user_id: UserUUID, oracle_state: OracleState) -> VotingPower:
    """
    Oracle Module for the Prior Voting Score
    """
    bonus = 1.0
    for r in oracle_state.prior_voting_bonus_values[user_id]:
        bonus += oracle_state.prior_voting_bonus_map.get(r, 0.0)
    return bonus


# Reputation Bonus

def reputation_score(user_id: UserUUID, oracle_state: OracleState) -> VotingPower:
    """
    Oracle Module for the Reputation Score
    """
    return oracle_state.reputation_bonus_map.get(oracle_state.reputation_bonus_values[user_id], 0.0)

# Trust Bonus


def trust_score(user: User, oracle_state: OracleState) -> VotingPower:
    """
    Computes the Trust Score as based on the Canonical Page Rank.

    This is done by computing the Page Rank on the whole Trust Graph
    with default arguments and scaling the results through MinMax.

    The resulting scores will be contained between 0.0 and 1.0
    """
    pagerank_values = oracle_state.pagerank_results
    if (len(pagerank_values)) < 2 or (user.label not in pagerank_values.keys()):
        trust_score = 0.0
    else:
        value = pagerank_values[user.label]
        max_value = max(pagerank_values.values())
        min_value = min(pagerank_values.values())
        trust_score = (value - min_value) / (max_value - min_value)
    return trust_score


# Layering it together
def LAYER_1_AGGREGATOR(lst): return sum(lst)

# Take the product of the list


def LAYER_2_AGGREGATOR(lst): return reduce((lambda x, y: x * y), lst)


LAYER_1_NEURONS = {
    'trust_score': (lambda u, _1, _2, state: trust_score(u, state),
                    lambda x: x),
    'reputation_score': (lambda u, _1, _2, state: reputation_score(u, state),
                         lambda x: x)
}

LAYER_2_NEURONS = {
    'past_round': (lambda u, _2, _3, state: prior_voting_score(u, state),
                   lambda x: x),
}

DEFAULT_NG_LAYERS: list[NeuronLayer] = [(LAYER_1_NEURONS, LAYER_1_AGGREGATOR),
                                        (LAYER_2_NEURONS, LAYER_2_AGGREGATOR)]

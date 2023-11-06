from nqg_model.types import *
from math import abs

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
        selected_delegates = valid_delegates[:params['max_quorum_selected_delegates']] 
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
    relative_agreement = agreement / quorum_size

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
                            neuron_layers: tuple[dict, callable],
                            initial_votes: float=0.0,
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
            raw_neuron_vote = oracle_function(uid, pid, current_vote)
            neuron_votes.append(weighting_function(raw_neuron_vote))
        current_vote = layer_aggregator(neuron_votes)

        if print_on_each_layer:
            print(f"Layer {i+1}: {current_vote}")

    return current_vote


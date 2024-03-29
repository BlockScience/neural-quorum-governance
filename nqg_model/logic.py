from cadCAD_tools.types import Signal, VariableUpdate  # type: ignore
from nqg_model.types import *
from typing import Callable
from copy import deepcopy
from scipy.stats import poisson, bernoulli  # type: ignore
from random import choice, sample
from nqg_model.neural_quorum_governance import *
from nqg_model.helper import *
import networkx as nx # type: ignore

def generic_policy(_1, _2, _3, _4) -> dict:
    """Function to generate pass through policy

    Args:
        _1
        _2
        _3
        _4

    Returns:
        dict: Empty dictionary
    """
    return {}


def replace_suf(variable: str, default_value=0.0) -> Callable:
    """Creates replacing function for state update from string

    Args:
        variable (str): The variable name that is updated

    Returns:
        function: A function that continues the state across a substep
    """
    return lambda _1, _2, _3, state, signal: (variable, signal.get(variable, default_value))


def add_suf(variable: str, default_value=0.0) -> Callable:
    """Creates replacing function for state update from string

    Args:
        variable (str): The variable name that is updated

    Returns:
        function: A function that continues the state across a substep
    """
    return lambda _1, _2, _3, state, signal: (variable, signal.get(variable, default_value) + state[variable])



def p_evolve_time(params: NQGModelParams, _2, _3, _4) -> Signal:
    return {'delta_days': params['timestep_in_days']}

def s_days_passed(_1, _2, _3,
                  state: NQGModelState,
                  signal: Signal) -> VariableUpdate:
    return ('days_passed', state['days_passed'] + signal['delta_days'])

def s_delta_days(_1, _2, _3, _4, signal: Signal) -> VariableUpdate:
    return ('delta_days', signal['delta_days'])


def s_onboard_users(params: NQGModelParams, _2, _3, state: NQGModelState, _5) -> VariableUpdate:
    """
    Onboard N new users and their relevant properties for NQG
    through stochastic processes.

    XXX: the new user reputation is chosen from the `ReputationCategory` enum
    with every option having equal weight.
    XXX: the active past rounds for the new user is randomly sampled
    from the list of past rounds with equal weights. The amount of samples
    is based on a capped poisson sample.
    """
    new_user_list = deepcopy(state['users'])

    avg_new_users_per_ts = params['avg_new_users_per_day'] * params['timestep_in_days']
    new_users: int = poisson.rvs(avg_new_users_per_ts)

    past_round_choices = params['past_rounds']
    reputation_choices = list(ReputationCategory) # TODO: parametrize

    for i in range(new_users):
        past_voting_n = min(poisson.rvs(params['avg_user_past_votes']), 
                            len(past_round_choices))

        new_user = User(label=len(new_user_list) + i,
                        reputation=choice(reputation_choices),
                        active_past_rounds=set(sample(past_round_choices, past_voting_n)))
        
        new_user_list.append(new_user)

    return ('users', new_user_list)

def p_user_vote(params: NQGModelParams,
                 _2,
                 history: dict[int, dict[int, NQGModelState]], 
                 state: NQGModelState) -> Signal:
    """
    Make new users decide on their actions: Abstain, Vote or Delegate

    XXX: Bernoulli processes are used for all of the following:
        - determining the probability of a user participating (actively or delegating) or not.
        - determine whatever the user will actively vote or delegate
        - determine if the user will vote on a project or not
        - determine if the user will vote yes or no on a project 
    XXX: Poisson processes are used for all of the following:
        - determine how much delegatees an user will have if he opted to delegate 
    """
    delegates: DelegationGraph = deepcopy(state['delegatees'])
    action_matrix: ActionMatrix = deepcopy(state['action_matrix'])
    decisions: dict[UserUUID, Action] = deepcopy(state['user_round_decisions'])

    current_users = set(u.label 
                     for u 
                     in state['users'])
    
    previous_state_users = retrieve_prev_state_users(history)

    new_users = current_users - previous_state_users

    for user in new_users:
        action_matrix[user] = {}
        if bernoulli.rvs(params['new_user_action_probability']):
            if bernoulli.rvs(params['new_user_round_vote_probability']):
                decisions[user] = Action.RoundVote
                # Active vote
                for project in params['projects']:
                    if bernoulli.rvs(params['new_user_project_vote_probability']):
                        if bernoulli.rvs(params['new_user_project_vote_yes_probability']):
                            project_vote = Vote.Yes
                        else:
                            project_vote = Vote.No
                    else:
                        project_vote = Vote.Abstain
                    action_matrix[user][project] = project_vote
            else:
                decisions[user] = Action.Delegate
                mu = params['new_user_average_delegate_count'] - params['new_user_min_delegate_count']
                delegate_count = poisson.rvs(mu, loc=params['new_user_min_delegate_count'])
                delegate_count += params['new_user_min_delegate_count']
                if delegate_count > len(previous_state_users):
                    delegate_count = len(previous_state_users)

                if delegate_count < params['new_user_min_delegate_count']:
                    pass
                else:
                    user_delegates = sample(previous_state_users, delegate_count)
                    delegates[user] = user_delegates
        else:
            decisions[user] = Action.Abstain

    return {'delegatees': delegates,
            'action_matrix': action_matrix, 
            'user_round_decisions': decisions}



def s_trust(params: NQGModelParams, _2, history, state: NQGModelState, _5) -> VariableUpdate:
    """
    Make new users trust each other

    XXX: this is done by randomly sampling the set of previous users. The amount
    of users to be trusted is sampled from a Poisson distribution.
    """
    trustees: TrustGraph = deepcopy(state['trustees'])
    current_users = set(u.label 
                     for u 
                     in state['users'])
    
    previous_state_users = retrieve_prev_state_users(history)

    new_users = current_users - previous_state_users
    for user in new_users:
        n_user_trustees = poisson.rvs(params['new_user_average_trustees'])
        n_user_trustees = min(n_user_trustees, len(previous_state_users))
        user_trustees = set(sample(previous_state_users, n_user_trustees))
        trustees[user] = user_trustees

    return ('trustees', trustees)

def s_oracle_state(params: NQGModelParams, _2, _3, state: NQGModelState, _5) -> VariableUpdate:
    """
    Update the state of the oracles (eg. pagerank values & oracles/reputation weights)
    """
    raw_graph = state['trustees']

    # Update Page rank values
    G = nx.from_dict_of_lists(raw_graph,
                              create_using=nx.DiGraph)
    pagerank_values = nx.pagerank(G, 
                                  alpha=0.85, 
                                  personalization=None, 
                                  max_iter=100,
                                  tol=1e-6,
                                  nstart=None,
                                  weight=None,
                                  dangling=None)
    
    # Update Reputation & Prior Voting user data

    reputation_values = {u.label: u.reputation for u in state['users']}
    prior_voting_values = {u.label: list(u.active_past_rounds) for u in state['users']}

    new_state = OracleState(pagerank_results=pagerank_values,
                            reputation_bonus_values=reputation_values,
                            prior_voting_bonus_values=prior_voting_values,
                            reputation_bonus_map=state['oracle_state'].reputation_bonus_map,
                            prior_voting_bonus_map=state['oracle_state'].prior_voting_bonus_map)
    return ('oracle_state', new_state)


def p_compute_votes(params: NQGModelParams, _2, _3, state: NQGModelState) -> Signal:
    """
    Perform Neural Quorum Governance
    """
    action_vote_matrix: ActionMatrix = deepcopy(state['action_matrix'])
    per_project_voting: PerProjectVoting = deepcopy(state['per_project_voting'])

    # Compute Abstainin users action matrix
    abstaining_users = set(u for u, d in state['user_round_decisions'].items()
                        if d == Action.Abstain)
    
    for user_id in abstaining_users:
        action_vote_matrix[user_id] = {}
        for project in params['projects']:
            action_vote_matrix[user_id][project] = Vote.Abstain
    
    # Compute Delegatees action matrix with Quorum Delegation
    delegating_users = set(u for u, d in state['user_round_decisions'].items()
                        if d == Action.Delegate)
    for user_id in delegating_users:
        action_vote_matrix[user_id] = {}
        for project in params['projects']:
            vote = vote_from_quorum_delegation(state['delegatees'].get('user', []),
                                        project,
                                        state['action_matrix'],
                                        state['user_round_decisions'],
                                        params)
            action_vote_matrix[user_id][project] = vote

    # Compute vote matrix with Neural Governance
    vote_matrix: VotingMatrix = {}
    for user_id, votes in action_vote_matrix.items():
        vote_matrix[user_id] = {}
        for project, vote in votes.items():
            power = power_from_neural_governance(user_id, 
                                                 project, 
                                                 params['neuron_layers'],
                                                 state['oracle_state'], 
                                                 params['initial_power'])
            vote_matrix[user_id][project] = vote * power
            if project in per_project_voting:
                per_project_voting[project] += vote_matrix[user_id][project]
            else:
                per_project_voting[project] = vote_matrix[user_id][project]

    return {'vote_matrix': vote_matrix,
            'per_project_voting': per_project_voting}
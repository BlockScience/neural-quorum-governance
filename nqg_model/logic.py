from cadCAD_tools.types import Signal, VariableUpdate
from nqg_model.types import *
from typing import Callable
from copy import copy, deepcopy
from scipy.stats import poisson, norm
from random import choice, sample

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
    """
    new_user_list = deepcopy(state['users'])

    avg_new_users_per_ts = params['avg_new_users_per_day'] * params['timestep_in_days']
    new_users: int = poisson.rvs(avg_new_users_per_ts)

    past_round_choices = params['past_rounds']
    reputation_choices = list(ReputationCategory) # TODO: parametrize

    for i in range(new_users):
        past_voting_n = max(poisson.rvs(params['avg_user_past_votes']), 
                            len(past_round_choices))

        new_user = User(label=str(len(new_user_list) + i),
                        reputation=choice(reputation_choices),
                        active_past_rounds=set(sample(past_round_choices, past_voting_n)))
        
        new_user_list.append(new_user)

    return ('users', new_user_list)

def p_user_vote(params: NQGModelParams, _2, _3, state: NQGModelState) -> Signal:

    delegates: DelegationGraph = {}
    action_matrix: ActionMatrix = {}

    return {'delegates': delegates,
            'action_matrix': action_matrix}

def s_trust(params: NQGModelParams, _2, _3, state: NQGModelState, _5) -> VariableUpdate:
    new_trustees: TrustGraph = {}
    return ('trustees', new_trustees)

def p_compute_votes(params: NQGModelParams, _2, _3, state: NQGModelState) -> Signal:

    action_vote_matrix: VotingMatrix = {}
    vote_matrix: VotingMatrix = {}
    per_project_voting: PerProjectVoting = {}

    return {'active_vote_matrix': action_vote_matrix,
            'vote_matrix': vote_matrix,
            'per_project_voting': per_project_voting}
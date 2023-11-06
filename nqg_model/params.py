from nqg_model.types import *
from nqg_model.neural_quorum_governance import DEFAULT_NG_LAYERS
from numpy import nan

TIMESTEPS = 100
SAMPLES = 1

N_INITIAL_USERS = 6
N_PROJECTS = 15
N_PAST_ROUNDS = 5

AVERAGE_PAST_VOTES_PER_USER = 1.5
PAST_ROUNDS = set(i for i in range(N_PAST_ROUNDS))

DEFAULT_PROJECTS = set(f"proj_{i}" for i in range(N_PROJECTS))


INITIAL_ORACLE_STATE = OracleState(
    pagerank_results={},
    reputation_bonus_map={
    ReputationCategory.Tier3: 0.3,
    ReputationCategory.Tier2: 0.2,
    ReputationCategory.Tier1: 0.1,
    ReputationCategory.Uncategorized: 0.0},
    prior_voting_bonus_map={
    1: 0.0,
    2: 0.1,
    3: 0.2,
    4: 0.3
}
)

INITIAL_STATE = NQGModelState(
    days_passed=0.0,
    delta_days=nan,
    users=[],
    user_round_decisions={},
    delegatees={},
    trustees={},
    action_matrix={},
    vote_matrix={},
    per_project_voting={},
    oracle_state=INITIAL_ORACLE_STATE
)

SINGLE_RUN_PARAMS = NQGModelParams(
    label='default_run',
    timestep_in_days=1.0,
    quorum_agreement_weight_yes=1.0,
    quorum_agreement_weight_no=-1.0,
    quorum_agreement_weight_abstain=0.0,
    max_quorum_selected_delegates=5,
    max_quorum_candidate_delegates=10,
    quorum_delegation_absolute_threshold=1/2,
    quorum_delegation_relative_threshold=2/3,
    neuron_layers=DEFAULT_NG_LAYERS,
    initial_power=0.0,
    past_rounds=PAST_ROUNDS,
    projects=DEFAULT_PROJECTS,
    avg_new_users_per_day=1.0,
    avg_user_past_votes=AVERAGE_PAST_VOTES_PER_USER,
    new_user_action_probability=0.5,
    new_user_round_vote_probability=0.5,
    new_user_project_vote_probability=5/N_PROJECTS,
    new_user_project_vote_yes_probability=0.8,
    new_user_average_delegate_count=6.5,
    new_user_min_delegate_count=5,
    new_user_average_trustees=7.0

)
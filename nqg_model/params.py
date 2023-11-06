from nqg_model.types import *


N_PROJECTS = 15
DEFAULT_PROJECTS = set(f"proj_{i}" for i in range(N_PROJECTS))

INITIAL_STATE = NQGModelState(
    days_passed=0.0,
    delta_days=None,
    users=INITIAL_USERS,
    user_round_decisions=INITIAL_DECISIONS,
    delegatees=INITIAL_DELEGATEES,
    trustees=INITIAL_TRUSTEES,
    action_matrix=INITIAL_ACTIONA_MATRIX,
    vote_matrix={},
    per_project_voting=None
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
    neuron_layers=DEFAULT_NEURON_LAYERS,
    initial_power=0.0,
    past_rounds={1, 2, 3, 4},
    projects=DEFAULT_PROJECTS,
    avg_new_users_per_day=1.0,
    avg_user_past_votes=3.5,
    new_user_action_probability=0.5,
    new_user_round_vote_probability=0.5,
    new_user_project_vote_probability=5/N_PROJECTS,
    new_user_project_vote_yes_probability=0.8,
    new_user_average_delegate_count=6.5,
    new_user_min_delegate_count=5,
    new_user_average_trustees=7.0

)
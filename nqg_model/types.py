from typing import Annotated, TypedDict, Union, Callable
from dataclasses import dataclass
from enum import Enum, auto

Days = Annotated[float, 'days']  # Number of days
UserUUID = str
ProjectUUID = str
VotingPower = float
PastRoundIndex = int
TrustGraph = dict[UserUUID, set[UserUUID]]
DelegationGraph = dict[UserUUID, list[UserUUID]]
class ReputationCategory(Enum):
    Tier3 = auto()
    Tier2 = auto()
    Tier1 = auto()
    Uncategorized = auto()
class Vote(float, Enum):
    """
    The Voting Actions towards a Project that a User can take and the 
    values in terms of Voting Power.
    """
    Yes = 1.0
    No = -1.0
    Abstain = 0.0

class Action(Enum):
    """
    The Decisions that a User can make in a Round.
    """
    RoundVote = auto()
    Delegate = auto()
    Abstain = auto()

@dataclass
class User():
    label: UserUUID
    reputation: ReputationCategory
    active_past_rounds: set[PastRoundIndex]


ActionMatrix = dict[UserUUID, dict[ProjectUUID, Vote]]
VotingMatrix = dict[UserUUID, dict[ProjectUUID, VotingPower]]
PerProjectVoting = dict[ProjectUUID, VotingPower]

class NQGModelState(TypedDict):
    days_passed: Days
    delta_days: Days
    users: list[User]
    
    user_round_decisions: dict[UserUUID, Action]
    delegatees: DelegationGraph
    trustees: TrustGraph
    action_matrix: ActionMatrix
    vote_matrix: VotingMatrix
    per_project_voting: PerProjectVoting


class NQGModelParams(TypedDict):
    label: str
    timestep_in_days: Days

    # Quorum Delegation Parameters
    quorum_agreement_weight_yes: float
    quorum_agreement_weight_no: float
    quorum_agreement_weight_abstain: float
    max_quorum_selected_delegates: int
    max_quorum_candidate_delegates: int
    quorum_delegation_absolute_threshold: float
    quorum_delegation_relative_threshold: float

    # Neural Governance Parameters
    neuron_layers: tuple[dict, Callable]
    initial_power: float

    # Neuron parameters
    past_rounds: set[PastRoundIndex]

    # Exogenous parameters
    projects: set[ProjectUUID]

    # Behavioral Parameters
    avg_new_users_per_day: float
    avg_user_past_votes: float
    new_user_action_probability: float
    new_user_round_vote_probability: float
    new_user_project_vote_probability: float
    new_user_project_vote_yes_probability: float
    new_user_average_delegate_count: float
    new_user_min_delegate_count: int
    new_user_average_trustees: float



    

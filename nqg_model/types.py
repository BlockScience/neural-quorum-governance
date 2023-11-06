from typing import Annotated, TypedDict, Union
from dataclasses import dataclass
from enum import Enum, auto

Days = Annotated[float, 'days']  # Number of days
UserUUID = str
ProjectUUID = str
VotingPower = float
PastRoundIndex = int

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


ActionMatrix = dict[UserUUID, dict[ProjectUUID, Action]]
VotingMatrix = dict[UserUUID, dict[ProjectUUID, VotingPower]]
PerProjectVoting = dict[ProjectUUID, VotingPower]

class NQGModelState(TypedDict):
    days_passed: Days
    delta_days: Days
    users: list[User]
    projects: set[ProjectUUID]
    delegatees: dict[UserUUID, list[UserUUID]]
    trustees: dict[UserUUID, set[UserUUID]]
    action_matrix: ActionMatrix
    active_vote_matrix: VotingMatrix
    vote_matrix: VotingMatrix
    per_project_voting: PerProjectVoting


class NQGModelParams(TypedDict):
    label: str
    timestep_in_days: Days

    avg_new_users_per_day: float
    avg_user_past_votes: float
    past_rounds: set[PastRoundIndex]

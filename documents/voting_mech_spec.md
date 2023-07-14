
<style>
    
body {
	counter-reset: heading;
}
    
h2:before {
	content: counter(heading)". ";
	counter-increment: heading;
}
    
h2 {
	counter-reset: subheading;
}
h3:before {
	content: counter(heading)"." counter(subheading)". ";
	counter-increment: subheading;
}
    
h3 {
	counter-reset: subsubheading;
}
h4:before {
	content: counter(heading)"." counter(subheading)"." counter(subsubheading)". ";
	counter-increment: subsubheading;
}
    
h4 {
	counter-reset: subsubsubheading;
}
h5:before {
	content: counter(heading)"." counter(subheading)"." counter(subsubheading)"."counter(subsubsubheading)". ";
	counter-increment: subsubsubheading;
}
</style>

## Intro

:::success
Section status: Done
:::

This document provides an concise description along with pseudo-code examples for an script-like implementation written in Python. More detailed considerations around user stories, interfaces, general architecture for an in-production implementation can be found on the [SDF Voting Mechanism PoC Design](/HzRrf1NtQ_a7nlSvX_stXg) document. The decisions on this specification comes from an mixture of requirements-based design, conversations with the SDF Team and arbitrary ones taken by BlockScience for PoC purposes. An non-exhaustive list of them can be found at [SCF Voting Mechanisms - Decisions for the PoC](/BIh2LNprSoaSM-rRVjbAjA).

An notebook containing an example implementation for this document can be found on the [`BlockScience/scf-voting-mechanism` GitHub repository](https://github.com/BlockScience/scf-voting-mechanism).

## General Definitions

:::success
Section status: done
:::

The admissible user actions for the SDF-Voting Mechansim in each round (mutually exclusive): 

- **Vote** (yes/no/abstain) on any number of project submissions
    - A "no" vote will cancel a "yes" vote with the same voting power. In other words, if someone Voting Power is `5`, then Yes would add `+5` to the Project Votes, and No would add `-5`.
- **Delegate** full Voting Power to a **ordered** list of at least 5 other users - called a Quorum. Quorums are only valid for the current round and should be re-initialized / re-activated for each new round.
    - The Actual Quorum will consists of the first 5 users that did opt for Voting rather than Delegating. If there are less than 5 users, then any missing slot will be replaced by Abstain votes.

Voting is going to take place based on Discrete Rounds, and tallying only occurs by the end of the round.

The SDF-VM PoC can be described in terms of Inputs and Outputs as:
- Input: 
    - Structural (once per round): **set of Users** and **set of Projects**
        - Assumption: the set of Users and set of Projects are validated before.
    - Active (user discretionary): set of **User Actions**
- Output: **a map from Projects to Project Voting Power**.
    - Project Voting Power = Real Number

The generic structures that make up the Voting Mechanism are:
- User: a UUID
- Project: a UUID
- Project Votes: an map from project-UUID to an Real Number.
- User Action: Either User Quorum or (exclusive) User Vote. 
    - A User Quorum: a map from a single user-UUID (key) to multiple user-UUIDs (value)
        - Constraint: The map value should contain five distinct user-UUIDs. Cannot include the own user-UUID.
    - A User Round Vote: a map from a single user-UUID to a set of User Project Votes. Project UUIDs on the set of User Project Votes should be distinct.
    - A User Project Vote is a 2-tuple consisting of project-UUID and Vote Decision
        - Vote Decision: Yes, No and Abstain


Lastly, the procedure on which User Actions is converted into Project Votes is as follows:
1. The Voting Power associated with each User Project Vote object is computed.
    - If Voting Power is agnostic to the project being voted, then this is equivalent to computing the Voting Power for each User.
    - Note that Quorum Votes arises from the Quorum Voting Module
3. All User Project Votes are summed per project and assigned to the Project Votes map.

### Vote tallying pseudocode example

:::success
Section status: Done
:::




:::info
**Note**: this pseudo-code is decoupled from the Vote Neurons that were defined for the PoC. Different ones are used here for pedagogical purposes.
:::

:::warning
**Warning**: This code is not assured to be valid, and the output is likely to be incorrect. This is not an substitute for unit tests.
:::

```python=
# 1) Types

# Neuron Governance Types
Weight = callable[[VotingPower], VotingPower]
OracleFunction = callable[[UserUUID, ProjectUUID], VotingPower]
VoteNeuron = tuple[OracleFunction, Weight]
Aggregator = callable[[list[VotingPower]], Voting Power]
           
# User Action Types
RoundVote = dict
Delegate = dict
                      
class Vote(Enum):
    Yes = 1.0
    No = -1.0
    Abstain = 0.0

# 2) Structural Inputs
USERS = {'maria', 'fernando', 'giuseppe', 'sarah', 'tom', 'laura'}

PROJECTS = {'voting-mech-for-scf', 
            'quorum-voting'}

# 3) Active Inputs
USER_ACTIONS = {
    'maria': RoundVote({'voting-mech-for-scf': Vote.Yes, 
                        'quorum-voting': Vote.Abstain}),
    'fernando': RoundVote({'voting-mech-for-scf': Vote.Yes}),
    'giuseppe': RoundVote({'voting-mech-for-scf': Vote.Yes, 
                           'quorum-voting': Vote.Yes}),
    'sarah': RoundVote({'voting-mech-for-scf': Vote.Yes, 
                        'quorum-voting': Vote.No}),
    'tom': Delegate(Users),
    'laura': Delegate({'maria', 'fernando', 'sarah', 'tom'})
}

upload_actions(USER_ACTIONS)
    
# 4) Neural Governance Configuration

# Multiplicative Aggregation over Voting Weights
AGGREGATOR: lambda power_lst: reduce(lambda x, y: x * y)

VOTE_NEURONS = {
    'one_vote_per_user': (lambda uid, pid: 1,
                          lambda x: x),
    'quadratic_funding': (lambda uid, pid: query_user_contributions(uid),
                          lambda x: 1 + K_QF * x ** (1/2)),
    'reputation_score': (lambda uid, pid: query_user_reputation(uid),
                         lambda x: 1 + K_REP * x),
}

# 5) Compute Final Output    

## a) Compute Project Votes
project_vote_power = defaultdict(float)

for (pid, project) in PROJECTS:
    for (uid, user) in USERS:
        args = (uid, pid, VOTE_NEURONS, AGGREGATOR)
        project_vote_power[pid] += user_project_vote_power(*args)        
```

```python=
print(project_vote_power)
> {'voting-mech-for-scf': 6.5, 'quorum-voting': 4.3}
```


## Components Specification

### Neural Governance Specification

:::warning
Section status: pending review
:::

The role of the Neural Governance is to decide how much voting power should be allocated to a vote (either direct votes or quorum-delegated votes). Key primitives associated with NG are the Oracle Function (a raw input provider), a Weighting Function (which transforms the raw-input into a comparable measurement for voting power), and an Aggregator (which combines all the Vote Neuron outputs into a single number).

Some open questions include:
- ~~Only "Yes" votes are weighted and all other decisions (No or Absent) are set to a pre-defined constants (eg. 0). Should we go with that or consider something else?~~
- ~~Consideration 1: Yes vs NO/Abstain. Neglects "veto power" by higher voting power users/quorums~~
    - Consideration 2: Yes = 1, Abstain = 0, No= -1 . Final outcome must be positive (xor cross certain threshold)
- Should the Oracle Function output be a Raw Voting Power number or should it be arbitrary and leave for the Weighting to make it equivalent? The first one allows the Weights to be more intuitive (it simple scales the Oracle output). The second one allows for weighting non-numerical constructs directly (eg. Map categories A, B and C from the Oracle into 0.2, 0.4 and 0.6).

### Vote Neurons to be included on the PoC

:::warning
Section status: pending review
:::

- Module 1: SDF Assigned Reputation: "Badges"
- Module 2: ~~KYC~~ Prior Voting History
- Module 3: Trust Graph Bonus, see [SCF Trust Bonus](https://hackmd.io/RQ-okLIHRduX0SL_NSbImQ)


#### Pseudocode Example

:::warning
Section status: pending review
:::

```python=
# Types
ProjectUUID = str
UserUUID = str

VoteDecision = bool
UserProjectVote = tuple[ProjectUUID, VoteDecision]
VotingPower = float

VoteNeuron = tuple[OracleFunction, Weight]
OracleFunction = callable[[UserUUID, ProjectUUID], object]
Weight = callable[[object], VotingPower]
Aggregator = callable[[list[VotingPower]]], VotingPower]

ABSENT_VOTING_POWER: VotingPower = 0.0
NAY_VOTING_POWER_FACTOR: VotingPower = 0.0

# Attribute Voting Power to an (user, project) tuple
def user_project_vote_power(uid: UserUUID, 
                            user_project_vote: UserProjectVote, 
                            vote_neurons: set[VoteNeuron], 
                            aggregator: Aggregator) -> VotingPower:
    """
    User Voting Power to be allocated for an given project.
    """
    if user_project_vote.decision in {Yes, No}
        pid = user_project_vote.pid
        
        # Compute Oracle Raw Voting Power values for
        user_project_vote_components = [weight(oracle(uid, pid))
                                        for (oracle, weight) 
                                        in vote_neurons]
        
        # Aggregate and return User-Project Voting Power
        voting_power = aggregator(user_project_vote_components)   
    elif user_project_vote.decision == Absent:
        return ABSENT_VOTING_POWER
    else:
        raise VoteDecisionError
        
    if user_project_vote.decision == Yes:
        return voting_power
    elif user_project_vote.decision == No
        return NAY_VOTING_POWER_FACTOR * voting_power


# Example execution flow
USER_UUID = 'danlessa'
USER_PROJECT_VOTE = ('voting-mech-for-scf', VoteDecision.Yes)

EXAMPLE_NEURONS = [
    (lambda uid, pid: user_reputation_score(uid),
     lambda x: x * 0.2),
    
    (lambda uid, pid: project_reputation_score(pid),
     lambda x: x * 0.2),
    
    (lambda uid, pid: user_trust_score(uid),
     lambda x: x * 0.3), 
    
    (lambda uid, pid: coi_score(uid, pid),
     lambda x: x * 0.3)
]

EXAMPLE_AGGREGATOR = lambda power_components: sum(power_components)

# Not used
EXAMPLE_QF_AGGREGATOR = lambda power_components: sum(power_components) ** 0.5

# Compute Voting Power from USER_UUID towards Project
x = user_project_vote(USER_UUID, 
                      USER_PROJECT_VOTE, 
                      EXAMPLES_NEURONS, 
                      EXAMPLE_AGGREGATOR)
```

### Quorum Voting Specification

:::warning
Section status: pending review
@danlessa adapted the below for new choices made
:::

The role of Quorum Voting is to allow delegation of votes from individual users to groups of other users they trust. To reduce the risk of circularity and inactive Quorums, Users can indicate whether they expect to vote or to delegate and choose a total of 10 other (user-ranked) UUIDs for delegation. The top 5 UUIDs make up their specific Quorum. 
A Quorum has a treshold for active participation of 66%. For the PoC, this means that 4 out of 5 Quorum members must render some vote, otherwise the delegating user will automatically abstain. 
If the active participation threshold is reached, absolute majority is used to determine the outcome of the Quorum Vote. 
Examples: 
If all 5 Quorum members vote:
* 3 Yes, 2 No -> Delegating User automatically votes Yes
* 2 Yes, 3 No -> Delegating User automatically votes No
If 4 Quorum members vote, while one does not:
* 3 Yes, 1 No -> Delegating User automatically votes Yes
* 2 Yes, 2 No -> No absolute majority, Delegating User automatically abstains. 

QV allows for users to reduce attention cost, while limiting bribery and other risks of individual delegates.
Flow: Before a voting round starts, Users can declare whether they expect to **vote** or **delegate** in this round. 
A User declares a set of 10 distinct other users, and ranks them. If any of the users have declared to **delegate**, the system ranks these below any voters that declared to **vote**. 
Once 3 of the 5 Quorum UUIDs have voted in one direction (i.e. all Yes or No), the User Voting Power (uid_pid_power) is added. The Voting Power of Quorum UUIDs is not taken into account, only the decision they make on an absolute basis. If no three Quorum UUIDs vote for the same choice, the User abstains. 


Some open questions are: 
- Agreement of Quorum: 
    - Internal Vote: Active (Yes, No) vs. Inactive (Abstain) Quorum members, this question touches on weighting of Yes and No vs only weighting Yes
        - :checkmark : As per 06 July, we have decided that an No vote will cancel an Yes vote. Eg. Yes = +1, No = -1 and Abstain = 0.
    - Threshold: 0.66 for now
    - Quorum size: 5 for PoC, but could be arbitrary
- Formation of Quorum:
    - Anonymity: When is a Quorum chosen, and how? Users could e.g. provide their quorum through a commitment scheme that is later revealed to assign power
    - Reactivation: Should a Quorum stay intact for several rounds, or have to be reactivated after each round? If intact for several rounds without additional actions, a decay of delegated voting power could come into play.
- Assignment of delegated Voting Power:
    - Option 1: User precommits his Quorum with commitment to vote with their agreement (yes, no, abstain)
    - Option 2: Delegated Power is assigned equally to each vote of the Quorum members in agreement (making it explicit that someone delegated to them)

#### Pseudocode Example

```python=

# Types
UserUUID = str
ProjectUUID = str
VoteDecision = {Yes, No}
VotingPower = float
UserQuorum = set[UserUUID]

# List of User votes towards multiple projects.
Votes = dict[UserUUID, dict[ProjectUUID, VoteDecision]]

def quorum_voting_power(uid_pid_power: VotingPower,
                        quorum: UserQuorum,
                        direct_votes: Votes,
                        threshold: float=0.66,
                        default_vote: Vote=No,
                        reject_power_factor: VotingPower=-1.0) -> VotingPower:   
    """
    Delegator User Voting Power to be allocated for an given project.
    """
    # List of Quorum Votes, eg. [Yes, No, Absent]
    quorum_votes = [direct_votes.get(delegator_uid).get(pid, default_vote)
                    for delegator_uid in quorum]
    
    # Map Quorum Votes to numerical values, eg. Yes -> 1.0. No -> -1.0
    quorum_numerical_votes = [1.0 if vote == Yes else 0.0
                              for vote in quorum_votes]
    
    # Compute Quorum Agreement in %
    quorum_agreement_share = sum(quorum_votes) / len(quorum_votes)
    
    # Return the Delegator Voting Power 
    # if Quorum Agreement is above threshold
    if yes_share >= threshold:
        return uid_pid_power
    else:
        return reject_power_factor * uid_pid_power        
```


## Resources

- [External Notes](https://docs.google.com/document/d/12V2Z4zT-rtd_oDJ8Ra-xN25h7HQyVQJXDaWBw6BhutA/edit#heading=h.1tlh3k3l5n6q)
- [Ideation Report](https://docs.google.com/document/d/1heCWpDVLm0NkhDWKhgLhpPhSgGZTVCPc7PcMQkJrDpA/edit#heading=h.jd1juvrmxwtg)
- [Lucidchart](https://lucid.app/lucidchart/3233754a-d598-422a-9b91-38a4122d1ed7/edit?viewport_loc=20%2C-3886%2C8626%2C10225%2CnhW0MXQ7lP.Y&invitationId=inv_c6d4cbe3-0807-4c14-960a-0289f7699022)
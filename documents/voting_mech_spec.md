# SCF Voting Mechanism PoC Specification

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

> Section Status: Done ✅

This document provides an concise description along with pseudo-code examples for an script-like implementation written in Python. More detailed considerations around user stories, interfaces, general architecture for an in-production implementation can be found on the [SDF Voting Mechanism PoC Design](/HzRrf1NtQ_a7nlSvX_stXg) document. The decisions on this specification comes from an mixture of requirements-based design, conversations with the SDF Team and arbitrary ones taken by BlockScience for PoC purposes. An non-exhaustive list of them can be found at [SCF Voting Mechanisms - Decisions for the PoC](/BIh2LNprSoaSM-rRVjbAjA).

An notebook containing an example implementation for this document can be found on the [`BlockScience/scf-voting-mechanism` GitHub repository](https://github.com/BlockScience/scf-voting-mechanism).

## General Definitions

> Section Status: Done ✅

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
2. All User Project Votes are summed per project and assigned to the Project Votes map.

### Vote tallying pseudocode example

> Section Status: Done ✅

> :information_source: Note: this pseudo-code is decoupled from the Vote Neurons that were defined for the PoC. Different ones are used here for pedagogical purposes.

> ⚠️ Warning: This code is not assured to be valid, and the output is likely to be incorrect. This is not an substitute for unit tests.

Below we have an demo work-flow for the PoC Voting Mechanism. An key simplification being made is the usage of an single-layer layer for Neural Governance rather than multiple layers.

Given an set of users, projects and user actions, the end output is to be an map from projects to votes. This is computed by aggregating (by taking the product) over the outputs originating from the Neural Governance Neurons, which in turn can be either simple functions (like the one user, one vote neuron), or complex functions implemented elsewhere (like the Quorum Delegation Neuron, or the Reputation Score Neuron).

```python=3.9
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

# Keys are labels for the Neurons
# Values are 2-tuples on which the first element is the Oracle Function
# and the second element is the Weighting Function
VOTE_NEURONS = {
    'one_vote_per_user': (lambda u, p: 1,
                          lambda x: x),
    'quadratic_funding': (lambda u, p: query_user_contributions(u),
                          lambda x: 1 + K_QF * x ** (1/2)),
    'reputation_score': (lambda u, p: query_user_reputation(u),
                         lambda x: 1 + K_REP * x),
    'quorum_delegation': (lambda u, p: quorum_delegate_result(u, p), 
                          lambda x: x)
}

# 5) Compute Final Output    

## a) Compute User Voting Power towards Projects

# All projects start with 0 votes.
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

> Section Status: Done ✅

*Neural Governance* is an label to an general architecture that attributes Voting Power by using paralellely and sequentially linked *Neurons*, whose input is derived from Oracle Functions, which is then weigheted and the subsequent output is aggregated across layers through custom rules (eg. take the product or sum between all Neurons an given layer)

Key primitives associated with Neural Governance are the Oracle Function (a raw input provider), a Weighting Function (which transforms the raw-input into a comparable measurement for voting power), and an Layer Aggregator (which combines all the Vote Neuron outputs into a single number). **A *Neuron*** is an pair consisting of an single *Oracle Function* and a single *Weighting Function*. **A *Layer*** is an list of *Neurons* plus a single *Layer Aggregator*.

An *Oracle Function* must take 2 or 3 arguments as an input: Voter ID (`string`), Project ID (`string`) and Previous Layer Vote (`float`, optional). The output is the Raw Neuron Vote (`float`). 

The *Weighting Function* takes a single argument as an input - Raw Neuron Votes (`float`) and their output is a single number - the Neuron Vote (`float`).

An *Layer Aggregator* function takes a ordered list of numbers (Neuron Votes, `list[float]`) and its output should be a single number - the Layer Vote (`float`).

The Final Voting Power that is directed from an Voter ID towards an Project ID is determined by feedforwarding the sequential network made by the pre-defined *Layers*.

On the following subsections, we provide an high-level example as for how to
encode the Neurons and Layers for an 2-layer Sequential Network, and an
example implementation for computing the Voting Power for an N-layer 
Sequential Network.

#### High-Level Example

> Section Status: Done ✅

```python=3.9

# Keys are labels for the Neurons
# Values are 2-tuples on which the first element is the Oracle Function
# and the second element is the Weighting Function

LAYER_1_AGGREGATOR = lambda lst: sum(lst)
LAYER_2_AGGREGATOR = lambda lst: product(lst)

LAYER_1_NEURONS = {
    'trust_score': (lambda uid, _1, _2: trust_score(uid),
                    lambda x: x),
    'reputation_score': (lambda uid, _1, _2: user_reputation(uid),
                         lambda x: 1 + K_REP * x)
}

LAYER_2_NEURONS = {
    'power_before_delegation': (lambda _1, _2, prev_vote: prev_vote,
                                lambda x: x),
    'quorum_delegation': (lambda u, p: quorum_delegate_result(u, p), 
                          lambda x: x) # Either 0.0 or 1.0
}

NEURAL_GOVERNANCE_LAYERS = [(LAYER_1_NEURONS, LAYER_1_AGGREGATOR),
                            (LAYER_2_NEURONS, LAYER_2_AGGREGATOR)]

# 5) Compute Final Output    

## a) Compute User Voting Power towards Projects

for (pid, project) in PROJECTS:
    for (uid, user) in USERS:
        args = (uid, pid, NEURAL_GOVERNANCE_LAYERS)
        project_vote_power[pid] += user_project_vote_power(*args) 
```


#### Feedforward Computation Example

> Section Status: Done ✅

```python=
# Types
ProjectUUID = str
UserUUID = str
VotingPower = float
VoteNeuron = tuple[OracleFunction, Weight]
OracleFunction = callable[[UserUUID, ProjectUUID, VotingPower], VotingPower]
Weight = callable[[VotingPower], VotingPower]
Aggregator = callable[[list[VotingPower]]], VotingPower]

# Attribute Voting Power to an (user, project) tuple
def user_project_vote_power(uid: UserUUID, 
                            pid: ProjectUUID, 
                            neuron_layers: tuple[dict, callable],
                            initial_votes: float=0.0) -> VotingPower:
    """
    Computes an User vote towards an Project as based on 
    an Feedforward implementation of Neural Governance for an strictly
    sequential network (no layer parallelism).
    """
    current_vote = initial_votes
    for layer in neuron_layers:
        (neurons, layer_aggregator) = layer
        neuron_votes = []
        for neuron in neurons:
            (oracle_function, weighting_function) = neuron
            raw_neuron_vote = oracle_function(uid, pid, current_vote)
            neuron_votes.append(weighting_function(raw_neuron_vote))
        current_vote = layer_aggregator(neuron_votes)
    return current_vote
            
```

### Vote Neurons to be included on the PoC

> Section Status: Pending Review 🛠️

- Module 1: Quorum Delegation
- Module 2: SDF Assigned Reputation: "Badges"
- Module 3: Prior Voting History
- Module 4: Trust Graph Bonus, see [SCF Trust Bonus](https://hackmd.io/RQ-okLIHRduX0SL_NSbImQ)

#### SDF Assigned Reputation

> Section Status: Not done ⚠️

#### Trust Graph Bonus

> Section Status: Not done ⚠️

#### Quorum Delegation

> Section Status: Pending Review 🛠️

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
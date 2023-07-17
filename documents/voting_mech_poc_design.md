:::warning
Document Status: In progress
:::

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

> Section status: pending review 🛠️

During the first phase of collaboration, the SDF and BlockScience teams collectively uncovered requirements and desirables for the design of a Proof of Concept voting mechanism for the Stellar Development Fund. 

As an output of the second phase, this document describes the design of a voting mechanism PoC. This PoC was developed jointly by BlockScience and the SDF. 
This document consists of:
* Purpose
* Goals
* Requirements 
* Data Structures
* PoC Components 
* PoC Oracle Modules


## Purpose

> Section status: pending review 🛠️

Design a POC for a novel Voting Mechanism for the Stellar Community Fund (SCF) that would be implemented and deployed using Soroban, Stellar’s native smart contracts platform (currently in preview release).

Votes will be cast on proposals for distribution of SCF funds to projects to benefit the Stellar Community. 

## PoC Design Goals

> Section status: pending review 🛠️

> [name=David Sisson] Words in bold need to be defined
> These feed SDF user stories

* Award SCF funds in a manner that brings long-term value to the ecosystem. 
    * This requires the mechanism to be contextually “**fair**” and “**good**”, 
    * coordinating participants around **value-adding activities**.
* Modular and flexible. 
    * This enables adaptability to further use-cases (eg. **Public Goods** vs. VC style funding) and 
    * allows the community to **co-own** and **co-operate** the mechanisms. 
    * Additionally, the mechanism should be **scalable** beyond currently limited groups of participants
* Limited complexity --- i.e., **simplicity**. Users should not feel overwhelmed by the logical parts of the mechanism. 
    * Similarities to already established concepts around Stellar Consensus Protocol (such as trust and Quorums) are regarded as being highly desirable. 
    * Additionally, SDF strives to enable innovative mechanisms rather than porting of (potentially) contextually non-fitting but already established mechanisms.

:::warning
Section status: check whether definitions in-line, footnote, after
:::
* (Definitions:)
    * “**fair**”: The mechanism should not without good reason benefit some members of the community over others.  
    * “**good**”: The mechanism should work for the benefit of the community and not harm its development. 
    * **value-adding activities**: The activities resulting from the mechanism should bring positive value to the community. 
    * **Public Goods**: Goods and services that are available to all, but might not have enough incentive for individuals to fund them alone. As opposed to Private Goods, which are owned and benefit individuals, leaving them enough incentive to fund them. 
    * **co-own**: The mechanism should not be owned by individuals, but by the community as a whole.  
    * **co-operate**: The community should be able to operate and adapt the mechanisms without relying on specific actors. 
    * **scalable**: The mechanism should be effective still when numbers of participants are increasing. 
    * **simplicity**: The community should not feel overwhelmed in understanding, using and adapting the mechanism. 

### Proposal Voting Round Protocol Overview

![RoundTimeline](https://lucid.app/publicSegments/view/860cacb3-db44-4e03-bc57-566f5de5305a/image.png "Voting round timeline")
*Figure Round Timeline: The timeline followed by this PoC*

## PoC Requirements in terms of User Stories

> Section status: pending review 🛠️

To assess whether the PoC implementation conforms to surfaced requirements and desirables, we express them in relationship to User Stories. 
In this section, we enumerate a semi-exhaustive set of stories, grouped across User Categories (Generic SCF User, Voter, Monitor and Administrator)

### Generic SCF User

> Section status: pending review 🛠️

As a generic SCF User, I want 
* the mechanisms used in the SCF to be simple enough for me to reason about them and flexible enough for them to be adapted to a changing environment or new use-cases.  
    * Neural Governance consists of several reasonably simple components, which show complexity only through composition. It allows allows to be parametrized to a changed environment and is designed with separate modules, which can be omitted, changed as well as new modules added to.
* the mechanisms used to be novel applications but also show familiarity to concepts I already know. 
    * Quorum Voting has similarities to well-known delegation schemes as well as the Stellar Consensus Protocol known to the community and allows for variable Quorum sizes, thresholds, formation and conditional logic to be added to. 
    * Quorum Voting and Neural Governance are novel applications and combinations of concepts seen before. 


* simple flexible $\rightarrow$ Neural Governance
* novel familiar $\rightarrow$ Quorum Voting

::: warning 
We never stated the below explicitly. Keep in or remove? 
:::
* round voting results as signal $\rightarrow$ voting power

### Voter User

> Section status: pending review 🛠️

* As an eligible voter in the Stellar Network community, I want to be able to and have the choice to vote in a round so that I can assign my voting power for or against each proposal in the round.

* As an eligible voter in the Stellar Network community, I want to be able to delegate my vote on any proposal that I do not want to vote on so that I can entrust my voting power to other users.

* As an eligible voter in the Stellar Network community, I want to be able to check my voting power at any time so that I make informed decisions about delegating my vote.
:::warning
Below was not specifically raised before. Statement as is would mean that even after submitting an on-chain vote, a user could change his choice at any time before votes are tallied. 
:::
* As an eligible voter in the Stellar Network community, I want to be able to change my vote for any proposal prior to vote tallying so that I account for changes in my understanding of the issues involved.
:::warning
Below was not specifically raised before. Statement as is seems similar enough to "check voting power at any time"
Consider removing. 
:::
* As an eligible voter in the Stellar Network community, I want to be informed of changes in estimated voting power of my delegated votes prior to vote tallying so that I can update my delegations.
:::info
For instance my delegate pool comes to include a circular reference
Note Jakob: We will get around this "softly" through:
Q4: How should the Quorum Voting Neuron resolve circular delegation?
Decision: People will indicate before the round whatever they’ll Vote or Delegate. Users can choose more than 5 people for the quorum but only the top 5 that are non-delegating will be considered.
:::

### Monitor User

> Section status: pending review 🛠️

* As a voting round monitor, I want to be informed of the operational status of the Stellar Voting System so that I can alert an administrator of issues.
* As a voting round monitor, I want to be able to check the progress of a voting round so that I can provide feedback to the community.
* As a voting round monitor, I want to be informed of the results of vote tallying so that I can inform the community.

### Administrator

> Section status: pending review 🛠️

* As a voting round administrator, I want to configure the Neural Governance component so that it fulfills the agreed upon rules for a voting round.
* As a voting round administrator I want to be able to configure a voting round so that a RoundBallot can be generated.
* As a voting round administrator, I want to be informed of operational issues so that I can
    * fix issues if I am able to do so, or
    * escalate issues if I am unable to fix them.

## PoC Data Structures

> Section status: pending review 🛠️

:::warning
> [name=David Sisson]InProg: Convert to JSON Schema
> TODO: Validation
:::

### Round Ballot
```json!
{
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$id": "https://stellar.org/QuorumVoting.json.schema",
    "definitions": {
        "RoundBallot": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "roundID": {
                    "type": "string"
                },
                "voterID": {
                    "type": "string",
                    "format": "integer"
                },
                "votes": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Vote"
                    }
                }
            },
            "required": [
                "roundID",
                "voterID",
                "votes"
            ],
            "title": "RoundBallot"
        }
    }
}
```

### Vote
```json!
{
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$id": "https://stellar.org/QuorumVoting.json.schema",
    "definitions": {
        "Vote": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "voterID": {
                    "type": "string",
                    "format": "integer"
                },
                "proposalID": {
                    "type": "string",
                    "format": "integer"
                },
                "roundID": {
                    "type": "string"
                },
                "voteCast": {
                    "type": "string",
                    "enum": ["Yes", "No", "Delegate"]
                }
            },
            "required": [
                "proposalID",
                "roundID",
                "voteCast",
                "voterID"
            ],
            "if": {
                "properties": {
                    "castVote": {
                        "const": "Delegate"
                    }
                }
            },
            "then": {
                "properties": {
                    "delegatePolicy": "$ref": "#/definitions/VoterDelegationPolicy"
                    }
                }
            },
            "title": "Vote",
            "description": "Schema of a Vote object for Stellar. Represents a single vote cast by a voter.",
        }
    }
}
```

### Voter Delegation Policy

```json!
{
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$id": "https://stellar.org/QuorumVoting.json.schema",
    "definitions": {
        "VoterDelegationPolicy": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "voterID": {
                    "type": "string",
                    "format": "integer",
                    "description": "The ID of the voter to whom this policy belongs."
                },
                "proposalID": {
                    "type": "string",
                    "format": "integer",
                    "description": "The ID of the proposal to which this policy applies."
                },
                "roundID": {
                    "type": "string",
                    "description": "The ID of the voting round to which this policy applies."
                },
                "delegateList": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "format": "integer",
                        "minItems": 5,
                        "maxItems": 5,
                        "uniqueItems": true
                    },
                    "description": "A list of voter IDs specified for delegation by this policy."
                }
            },
            "required": [
                "delegateList"
            ],
            "title": "Voter Delegation Policy",
            "description": "Schema of a VoterDelegationPolicy object for Stellar. Represents to whom a voter is delegating vote."
        }
    }
}
```

### RoundVotingMatrix

:::danger
Section status: not done; merge with NeuronResultMatrix --- output becomes input
:::

\{VoterID, ProposalID, Vote\}

### NeuronResultMatrix

> Section status: not done 🚧

\{VoterID, ProposalID, Vote, \{NeuronID, ResultArray\}\}

:::info 
**VoteDelegationGraph**
* Local to Quorum Voting Input Neuron?
* Schema does not invalidate cycles
:::

```json!
{
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$id": "https://stellar.org/schemas/VoteDelegationGraph",
    "type": "array",
    "items": {
        "$ref": "#/definitions/VoteDelegationGraphElement"
    },
    "definitions": {
        "VoteDelegationGraphElement": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "voterID": {
                    "type": "string",
                    "format": "integer"
                },
                "delegation": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/DelegationDelegationUnion"
                    }
                }
            },
            "required": [
                "delegation",
                "voterID"
            ],
            "title": "VoteDelegationGraphElement"
        },
        "DelegationDelegationUnion": {
            "oneOf": [
                {
                    "$ref": "#/definitions/VoteDelegationGraphElement"
                },
                {
                    "type": "string",
                    "format": "integer"
                }
            ],
            "title": "DelegationDelegationUnion"
        }
    }
}

```


## PoC Components

> Section status: pending review 🛠️

The proposed implementation of the SDF Voting Mechanism consists of three main components:
1. PollingPlace
2. PrecinctHQ
3. NeuralGovernance

The following figure illustrates how these components are integrated into a voting mechanism in the PoC. Each component is described in detail in the following sections.
    
![SystemDiagram](https://lucid.app/publicSegments/view/9108ff08-1808-4c88-88bc-30c1b3eec9b2/image.png "Neural Governance System Diagram")
Figure SystemDiagram: This figure shows the components that will be implemented in the POC including interfaces required by and provided by each component.

### The PollingPlace Component

> Section status: pending review 🛠️

The PollingPlace component implements the user interface with which a voter casts their votes for proposals in a given round of voting using a ballot. PollingPlace transmits a voter's ballot to the Governance component's input interface.

| Interface ID | Method Description | Method Signature | Method Return |
| ------- | ------------------ | --------------------- | ------------- |
| 1       | Voter UI           | vote(voterID, ballot) | JSON          |
| 2       | Governance module interface  | Text             | JSON          |

#### The User Interface SubComponent

* Voting UI --- Fills out a ballot
:::info
Is a ballot secret?
> [name=Danilo Lessa Bernardineli] As secret as would an Stellar Transaction and any other requirements (eg. retaining data for KYC / Reputation / etc) could allow.
:::
* Vote Delegation (UI) --- Specifies a delegation policy
:::info
Does a voter have a default delegation policy?
> [name=Danilo Lessa Bernardineli] No and Maybe. No in the sense that **initially, Delegation should always be triggered by the User**. Maybe in the sense that once an User has chosen to Delegate his vote, it could be renewed across rounds. One thing that has been debated on the Ideation is if it did make sense to have Voting Power decay if the delegation is not renewed (eg. on the Delegation round, 100% of the Delegatee power is made available, and the round afterwards would be 70%, and then 40%, and then it goes.)

> For **PoC purposes**, the answer is that Delegation is only valid for the current round.


Can a voter apply different delegation policies to different delegated votes within a round?
> [name=Danilo Lessa Bernardineli] 
> **No**. As of now, the User should either delegates 100% of his power to an quorum, or does not delegate. There's no middle-ground or options (beyond choosing the quorum).
> On the ideation we did discuss about partial delegation or having multiple quorums, but this was vetoed mostly due to the narrative complexity. Having "options" (eg. delegate only if certain user-defined contraints are followed) could be something desirable at some point, but we didn't discuss that enough.
:::

### The PrecinctHQ Component

> Section status: pending review 🛠️

The PrecinctHQ component implements a governor interface through which the governance component transmits the results of a voting round. PrecintHQ implements two user interfaces --- an administrative interface with which a voting round is configured and operated, and an interface from which to monitor the status of a voting round. 

PrecintHQ calls into the Monitoring and Administration interfaces exposed by the Governance component. PrecinctHQ 

| Interface ID | Method Description | Method Signature | Method Return |
| -------- | -------- | -------- | ------ |
| 1     | Text     | Text     | JSON |
| 2     | Text     | Text     | JSON |
| 3     | Text     | Text     | JSON |
| 4     | Text     | Text     | JSON |

### The Governance Component --- Neural Governance

:::warning
Section status: pending review
:::

The Governance component with which business rules for voting and vote weighting and vote aggregation are specified in subcomponents called neurons. The Governance component also implements non-neural subcomponents which provide input and output interfaces.

![NeuralGovernanceComponent](https://lucid.app/publicSegments/view/91ee8d70-640e-4b45-85af-7f2d27c68670/image.png "Neural Governance Component interfaces" =400x250)
*Figure NeuralGovernanceComponent: externally exposed interfaces of the Neural Governance Component.*


The neural governance component interfaces with operational polling place and PrecinctHQ modules through well defined, fixed, interfaces that have no dependence on the internal of the neural governance component. The neural components that implement voting policy within the neural governance component each communicates. 

![NeuralSubcomponent](https://lucid.app/publicSegments/view/215186f0-0005-4709-86d2-dc44d9eae21f/image.png
 "Standardized neural subcomponent interfaces")
*Figure NeuralSubcomponent: Each neuron is a modularized subcomponent that implements a vote accounting rule. Externally, communication with a neuron is mediated through a standard set of interfaces. Internally, the functionality of a neuron is implemented by a standardized framework of elements.*


Becuase of this combination of internal modulatity and fixed external interfaces, Neural Governance can be extensively modified without altering the existing architecture.

![ModifiedNeuralGovernance](https://lucid.app/publicSegments/view/89a6d5db-e904-4b5e-95ad-bcb85d43bda9/image.png "Example modification of Neural Governance Component")
*Figure ModifiedNeuralGovernance: This figure illustrates the flexibility of the Neural Governance Component. Here a hidden layer is added to enable application of learned input neuron weights.*

#### Non-neural Subcomponents

> Section status: pending review 🛠️

The non-neural components implement the interfaces that the VotingPlace and PrecintHQ must acquire in order to communicate with the Governance component.

##### Neural Governance Administration Subcomponent

> Section status: pending review 🛠️

The Neural Governance Administration subcomponent provides an interface that is acquired by PrecinctHQ. Voting round administrators configure voting rounds through this interface.

> [name=David Sisson]TODO: Describe various voting round configuation tasks

| Interface ID | Method Description | Method Signature | Method Return |
| -------- | -------- | -------- | ------ |
| 1     | Round configuration     | Text     | JSON |

##### Neural Governance Voting Subcomponent

> Section status: pending review 🛠️

The Neural Governance Voting subcomponent provides the interface acquired by Polling Place. Neural Governance Voting acquires the Input interface provided by the QuorumVotingInputNeuron. Each voter's ballot is passed from the Polling Place to the Neural Governance Voting subcomponent via this interface as a RoundBallot. The Neural Governance Voting subcomponent collates RoundBallots from all voters in a round into a RoundVotingMatrix. 

> [name=David Sisson]TODO: Define RoundBallot schema (Doing so [above](#RoundBallot))
> TODO: Define RoundVotingMatrix schema (Doing so [above](#RoundVotingMatrix))

| Interface ID | Method Description | Method Signature | Method Return |
| -------- | -------- | -------- | ------ |
| 1     | Ballot input    | Text     | JSON |

##### Neural Governance Monitoring Subcomponent

> Section status: pending review 🛠️

| Interface ID | Method Description | Method Signature | Method Return |
| -------- | -------- | -------- | ------ |
| 1     | Text     | Text     | JSON |

#### Neural Subcomponents

> Section status: pending review 🛠️

Each neural subcomponent exposes the same interfaces shown in Fig. NeuralSubcomponent. Neurons are wired Output to Input as shown in Fig. SystemDiagram.

| Interface ID | Method Description | Method Signature | Method Return |
| ----- | ------------- | -------- | ---- |
| 1     | Input         | Text     | JSON |
| 2     | Oracle        | Text     | JSON |
| 3     | Configuration | Text     | JSON |
| 4     | Output        | Text     | JSON |


##### Quorum Voting Input Neuron

:::danger
Section status: not done
Quorum rules must be configurable. 
* Size of quorum (min, max)
* Relative Consensus threshold
* Absolute Voting threshold

Quorum specified by list of delegates and list of alternates
:::

:::info
Hard rule: can't delegate to a voter who has delegated?

What values are Yes, No and NULL votes mapped to?
> [name=danlessa] to values that specified in the Round Configuration. Eg. Yes=+1, No=-1 and Null=0

How is a circular delegation graph interpreted?
> [name=danlessa] There are two possible ways to interpret:
> 1) Circular Delegations are replaced by NULL. Eg. if user A delegates to users {B, C, D} and user B delegates to user {A, E, F}, then for quorum agreement purposes, both users A and users B votes will be assumed to be NULL. 
> 2) Disallow re-delegation so that this is not admissible. Eg, if user A opts to delegate to user {B, C, D}, then those users cannot delegate. There's an potential privacy question in here related to knowing or not that an user is an delegatee vs delegator.
:::

##### Trust Input Neuron

:::danger
Section status: not done
:::

##### Expertise Input Neuron

:::danger
Section status: not done
:::

##### Voting History Input Neuron

:::danger
Section status: not done
:::

##### Output Neuron

:::danger
Section status: not done
:::

## PoC Oracle Modules

:::danger
Section status: not done
:::

### Quorum Voting Oracle

:::danger
Section status: not done
:::

### Know Your Customer Oracle

:::danger
Section status: not done
:::

### SDF Reputation Oracle

:::danger
Section status: not done
:::

### Community Trust Oracle

:::danger
Section status: not done
:::

## References

[SDF Voting Mechanism PoC Specification](/GMs8iB1MQEGsJirqqPm3NA)

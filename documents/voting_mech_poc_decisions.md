## Decisions

### Arbitrarily made by BlockScience for the PoC

Those decisions were made with minimal consultation and are based on our best judgment as per expressed requirements and discussions. As an rule of thumb, we'll bias for Decision that is simpler rather than complex (Occam's Razor) 


- All Neural Governance Modules are to be active with no user option to disable it.
- An User Quorum should be composed of Distinct Users. No Duplicates are allowed
- If an User Quorum size is less than 5, then any missing slot it is to be replaced by Absent votes.
- The Aggregation over Neurons will be Multiplicative. All Neurons output will be added by `+1` so that an Neuron Output of 0 means no Voting Power change.
- The Raw Trust Bonus will be defined as the Canonical Page Rank over the Trust Graph with Damping Factor of 15%. The values will be normalized through MinMax to `[0, 1]`, and re-scaled to `[0, 1]`, and this will be the Actual Trust Bonus.
    - This means that the top individual in terms of Trust Importance will have its voting power boosted by 100%.
    - The decision on using the Canonical Page Rank was made jointly and using Iterative Simplicity as an criteria. This should be studied and changed over time.

### As per Questions

Those decisions were determined through discussion with SDF. All decisions should be understood as applicable specifically to the PoC and can be overriden on future iterations as more insights come into play into the future.

- Q1: Is Quorum Consensus determined through Vote Consensus or Voting Power Consensus?
    - **Decision**: Vote Consensus
- Q2: Should Quorum Consensus be based on Absolute Agreement or Relative Agreement? Or both?
    - **Decision**: Minimum Threshold of Active Voters (67%) followed by Relative Agreement (Simple Majority)
        - Active Voter for an Given Project: Someone that did actively chose an non-abstaining Vote Action (eg. Yes or No)
        - In the absence of Consensus, the delegated decision is to be Absent.
- Q3: What happens if there’s no Quorum Consensus on voting “yes”? Should it render an “absent” position or an “no” position?
    - **Decision**: Consensus being Yes/No gives Yes/No decisions. Else, Abstain.
- Q4: How should the Quorum Voting Neuron resolve circular delegation?
    - **Decision**: People will indicate before the round whatever they'll Vote or Delegate. Users can choose more than 5 people for the quorum but only the top 5 that are non-delegating will be considered.
- Q5: Is it admissible or desirable to modify someone’s Bonus solely by the action of trusting another?
    - **Decision**: Undesirable but non-blocking
- Q6: How strongly should the Bonus be transmitted on successive trust relationships?
    -  **Decision**: Undesirable but non-blocking
- Q7: Should the Bonus be back-propagated?
    -  **Decision**: Undesirable but non-blocking
- Q8: Should the Bonus be capped or dilluted?
    - **Decision**: No

### Other Decisions

- Is a voter's voting power enhanced (some aggregate of delegatees' voting power) or simply applied?
    - **Decision**: Applied.
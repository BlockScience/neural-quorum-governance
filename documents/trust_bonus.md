## Resources

- [Trust Bonus folder on the SCF Voting Mechanism GitHub Repo](https://github.com/BlockScience/scf-voting-mechanism/tree/main/trust_bonus)
- [Exploring Subjectivity in Algorithms piece, by Zargham](https://medium.com/sourcecred/exploring-subjectivity-in-algorithms-5d8bf1c91714)
- [SourceCred Research Repo](https://github.com/sourcecred/research)
- [NetworkX `pagerank` method](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html)

## Story

>For the trust bonus, We're considering the following procedure:
>1. Suppose we have N users, and a directed graph that relates each distinct pair of users, where each directed edge means source user trusts destination user. (Input Step)
>2. **For each individual user, compute the Personalized PageRank for the entire graph** by taking that user as the seed node. (Compute Step)
>3. **The raw trust bonus for an individual user is the geometric mean** of the Personalized PageRank for that user across all computed iterations (Aggregation Step)
>4. The raw trust bonus should be treated so that the final trust bonus is not increased as a result of the user opting to create additional trust relationships. The exact procedure here is TBD. One suggestion is to perturbate the graph by removing edges and computing the new trust values. The perturbated graph values should never be smaller than the actual computation. **This mitigates against strategical behaviour** on which users opt to trust more in order to accrue more bonus.

>The specific values of alpha, self loop weight and upstream weight should still be figured out. In fact, there may be an completely independent (and out of scope) exercise here to determine the specific requirements, so I'm inclined in just picking something "in the right ballpark" and making sure we clarify those points. My current bias goes in the direction of upstream weight = 0.0, self-loop = 1.0 and alpha = 0.0.

Assuming that this approach is valid and assuming that we'll have an independent UI for the Trust Graph, then the next step is to sanity-check that algorithm by using the notebooks that were used in the [Exploring Subjectivity in Algorithms piece, by Zargham](https://medium.com/sourcecred/exploring-subjectivity-in-algorithms-5d8bf1c91714), which was done in the [SourceCred](https://sourcecred.io) context. The goal of this story is **not** to perform exhaustive tuning, but rather, to select something that can be iterated into.

Additional challenges may appear if we opt to use Discord Friends as the trust relationships, as friendship is a bi-directional edge. 

The rationale behind alpha=0.0 is to assume that users will exhaustively encode their trusted relationships. The usage of self-loop weights would be to avoid trust convergence into "sink" nodes, and we'll not assign upstream weights (eg. opting to trust someone should increase how much you're trusted).

## High-level Algorithm

```python

AGGREGATOR_FUNCTION = geometric_mean

def personalized_page_rank(graph: Graph, seed_node: Node, params) -> dict[Node, float]:
    """
    Computes the vector of Page Rank values by using an given node as a seed.
    """
    pass


def perturbate_graph(graph: Graph, seed_node: Node) -> list[Graph]
    """
    Perturbate graph by removing existing edges that outflows from the Seed Node.
    """
    pass

def trust_score(users: set[str], 
                trust_graph: dict[User, set[User]]) -> dict[User, float]:
    """
    Computes the vector of Trust Values
    """
    ## Step 2: Compute Personalized Page Rank
    # Key: source node
    # Value: Page Rank value for each node in the graph
    results: dict[User, dict[User, float]] = {}
    for user in USERS:
        results[user] = personalized_page_rank(trust_graph, user, params)

    ## Step 3: Compute Raw Trust Score
    raw_trust_scores: dict[User, float] = {}
    for user in USERS:
        user_page_rank_values = [results[ref_user][user] 
                                 for ref_user in results.keys()]
        raw_trust_scores(user) = AGGREGATOR_FUNCTION(user_page_rank_values)


    ## Step 4: Compare against perturbations
    trust_scores: dict[User, float] = {}
    for user in USERS:
        user_trust_scores = raw_trust_scores[user]
        modified_graphs: list[Graph] = perturbate_graph(trust_graph, user)
        for modified_graph in modified_graphs:
            modified_results = {u: personalized_page_rank(modified_graph, user)
                               for u in USERS}
            modified_page_rank_values = [modified_results[ref_user][user] 
                                        for ref_user 
                                        in modified_results.keys()]
            modified_trust_score = AGGREGATOR_FUNCTION(user_page_rank_values)
            if modified_trust_score < user_trust_score:
                user_trust_score = modified_trust_score

    return trust_scores

```


from nqg_model.logic import *
from copy import deepcopy


NQG_MODEL_BLOCKS: list[dict] = [
    {
        'label': 'Time Tracking',
        'ignore': False,
        'desc': 'Updates the time in the system',
        'policies': {
            'evolve_time': p_evolve_time
        },
        'variables': {
            'days_passed': s_days_passed,
            'delta_days': s_delta_days
        }
    }, 
    {
        'label': 'Onboard users',
        'policies': {},
        'variables': {
            'users': s_onboard_users
        }
    },
    {
        'label': 'Trust & Vote',
        'policies': {
            'user_vote': p_user_vote
        },
        'variables': {
            'trustees': s_trust,
            'delegates': replace_suf,
            'action_matrix': replace_suf,
            'user_round_decisions': replace_suf
        }
    },
    {
        'label': 'Tally votes',
        'policies': {
            'tally votes': p_compute_votes
        },
        'variables': {
            'vote_matrix': replace_suf,
            'per_project_voting': replace_suf
        }
    }
]


NQG_MODEL_BLOCKS = [block for block in NQG_MODEL_BLOCKS
                              if block.get('ignore', False) is False]

# Post Processing

blocks: list[dict] = []
for block in [b for b in NQG_MODEL_BLOCKS if b.get('ignore', False) != True]:
    _block = deepcopy(block)
    for variable, suf in block.get('variables', {}).items():
        if suf == add_suf:
            _block['variables'][variable] = add_suf(variable)
        elif suf == replace_suf:
            _block['variables'][variable] = replace_suf(variable)
        else:
            pass
    blocks.append(_block)

NQG_MODEL_BLOCKS = deepcopy(blocks)
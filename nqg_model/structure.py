from nqg_model.logic import *





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
        'variables': {}
    },
    {
        'label': 'Update Trust Network',
        'policies': {},
        'variables': {}
    },
    {
        'label': 'Decide to vote or delegate',
        'policies': {},
        'variables': {}
    },
    {
        'label': 'Tally partial votes',
        'policies': {},
        'variables': {}
    }
]


NQG_MODEL_BLOCKS = [block for block in NQG_MODEL_BLOCKS
                              if block.get('ignore', False) is False]
from nqg_model.params import SINGLE_RUN_PARAMS, INITIAL_STATE, TIMESTEPS, SAMPLES
from nqg_model.structure import NQG_MODEL_BLOCKS

default_run_args = (INITIAL_STATE,
                     {k: [v] for k, v in SINGLE_RUN_PARAMS.items()},
                    NQG_MODEL_BLOCKS,
                    TIMESTEPS,
                    SAMPLES)
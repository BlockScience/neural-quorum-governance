from nqg_model import default_run_args
from nqg_model.experiment import standard_run
from cadCAD_tools.execution import easy_run
from datetime import datetime
import click
import os


@click.command()
@click.option('-e', '--experiment-run', 'experiment_run',
              default=False,
              is_flag=True,
              help="Make an experiment run instead")
@click.option('-p', '--pickle', 'pickle', default=False, is_flag=True)
def main(experiment_run: bool, pickle: bool) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if experiment_run is False:
        df = easy_run(*default_run_args)
    else:
        df = standard_run()
    if pickle:
        df.to_pickle(
            f"data/simulations/multi-run-{timestamp}.pkl.gz", compression="gzip")


if __name__ == "__main__":
    main()
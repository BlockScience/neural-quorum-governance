from typing import Annotated, TypedDict, Union
from dataclasses import dataclass


Days = Annotated[float, 'days']  # Number of days

class NQGModelState(TypedDict):
    days_passed: Days
    delta_days: Days

class NQGModelParams(TypedDict):
    label: str
    timestep_in_days: Days

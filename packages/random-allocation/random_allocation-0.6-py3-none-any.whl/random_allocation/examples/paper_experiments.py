# Standard library imports
import os
import sys
from typing import Dict, List, Union, Any, Callable

# Add the correct project root directory to PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Third-party imports
import numpy as np

# Local application imports
from random_allocation.comparisons.definitions import *
from random_allocation.comparisons.experiments import run_experiment, PlotType

# Configuration
SAVE_DATA: bool = True  # Set to True to save data to CSV files
SAVE_PLOTS: bool = True  # Set to True to save plots to files, False to display them interactively

# First experiment - Compare different schemes for varying sigma
params_dict_1: Dict[str, Any] = {
    'x_var': SIGMA,
    'y_var': EPSILON,
    SIGMA: np.exp(np.linspace(np.log(0.2), np.log(2), 20)),
    DELTA: 1e-10,
    NUM_STEPS: 100_000,
    NUM_SELECTED: 1,
    NUM_EPOCHS: 1
}

config_1: SchemeConfig = SchemeConfig(allocation_direct_alpha_orders=[int(i) for i in np.arange(2, 61, dtype=int)])

methods_list_1: List[str] = [LOCAL, SHUFFLE, POISSON_PLD, ALLOCATION_DIRECT, ALLOCATION_RECURSIVE, ALLOCATION_DECOMPOSITION]#, ALLOCATION_LOWER_BOUND

visualization_config_1: Dict[str, Union[bool, Callable[[float, int], str]]] = {
    'log_x_axis': True, 
    'log_y_axis': True, 
    'format_x': lambda x, _: f'{x:.2f}'
}

data_1: Dict[str, Any] = run_experiment(
    params_dict_1, 
    config_1, 
    methods_list_1, 
    visualization_config_1, 
    'epsilon_vs_sigma', 
    PlotType.COMBINED, 
    SAVE_DATA, 
    SAVE_PLOTS,
    direction=Direction.BOTH
)

# Second experiment - Compare different schemes for varying number of epochs
params_dict_2: Dict[str, Any] = {
    'x_var': NUM_EPOCHS,
    'y_var': EPSILON,
    SIGMA: 1,
    DELTA: 1e-8,
    NUM_STEPS: 10_000,
    NUM_SELECTED: 1,
    NUM_EPOCHS: np.exp(np.linspace(np.log(1), np.log(1001), 10)).astype(int)
}

config_2: SchemeConfig = SchemeConfig(allocation_direct_alpha_orders=[int(i) for i in np.arange(2, 61, dtype=int)])

methods_list_2: List[str] = [POISSON_RDP, ALLOCATION_DIRECT, POISSON_PLD]

visualization_config_2: Dict[str, Union[bool, Callable[[float, int], str]]] = {
    'log_x_axis': True, 
    'log_y_axis': False, 
    'format_x': lambda x, _: str(int(x))
}

data_2: Dict[str, Any] = run_experiment(
    params_dict_2, 
    config_2, 
    methods_list_2, 
    visualization_config_2, 
    'epsilon_vs_epochs', 
    PlotType.COMPARISON, 
    SAVE_DATA, 
    SAVE_PLOTS,
    direction=Direction.BOTH
)

# Third experiment - Compare different schemes for varying number of steps
params_dict_3: Dict[str, Any] = {
    'x_var': NUM_STEPS,
    'y_var': DELTA,
    SIGMA: 0.3,
    EPSILON: 10,
    NUM_STEPS: np.arange(25, 551, 50),
    NUM_SELECTED: 1,
    NUM_EPOCHS: 1
}

config_3: SchemeConfig = SchemeConfig(allocation_direct_alpha_orders=[int(i) for i in np.arange(2, 61, dtype=int)])

methods_list_3: List[str] = [POISSON_RDP, ALLOCATION_DIRECT, POISSON_PLD]

visualization_config_3: Dict[str, Union[bool, Callable[[float, int], str]]] = {
    'log_x_axis': False, 
    'log_y_axis': True, 
    'format_x': lambda x, _: str(int(x))
}

data_3: Dict[str, Any] = run_experiment(
    params_dict_3, 
    config_3, 
    methods_list_3, 
    visualization_config_3, 
    'delta_vs_steps', 
    PlotType.COMPARISON, 
    SAVE_DATA, 
    SAVE_PLOTS,
    direction=Direction.BOTH
)

# Fourth experiment - Compare different schemes for varying number of selected items
params_dict_4: Dict[str, Any] = {
    'x_var': NUM_SELECTED,
    'y_var': EPSILON,
    SIGMA: 1,
    DELTA: 1e-6,
    NUM_STEPS: 2**10,
    NUM_SELECTED: 2**np.arange(0, 10),
    NUM_EPOCHS: 1,
}

config_4: SchemeConfig = SchemeConfig(allocation_direct_alpha_orders=[int(i) for i in np.arange(2, 61, dtype=int)])

methods_list_4: List[str] = [POISSON_RDP, ALLOCATION_DIRECT, ALLOCATION_RDP_DCO]

visualization_config_4: Dict[str, Union[bool, Callable[[float, int], str]]] = {
    'log_x_axis': True, 
    'log_y_axis': True, 
    'format_x': lambda x, _: str(int(x))
}

data_4: Dict[str, Any] = run_experiment(
    params_dict_4, 
    config_4, 
    methods_list_4, 
    visualization_config_4, 
    'epsilon_vs_selected', 
    PlotType.COMPARISON, 
    SAVE_DATA, 
    SAVE_PLOTS,
    direction=Direction.BOTH
)
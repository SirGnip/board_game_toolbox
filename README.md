# Board Game Toolbox

Tools, utilities, simulations, and experiments for various board games.

Mostly small, incomplete experiments with probability.  Not really meant for public use. 


# How to install and run

    # create virual environment
    python -m venv venv
    
    # install to current environment (with current dir at top of repo) 
    pip install .     # "static" install
    pip install -e .  # "editable" install (setup.py handles source being under `src/`)

    # run scripts
    python -m cant_stop.calculator
    python -m risk.dice_roll_simulator
    
    # run linting
    pylint src/ --disable=invalid-name --disable=line-too-long --disable=missing-function-docstring

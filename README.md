# Board Game Toolbox

Tools, utilities, simulations, and experiments for various board games.

Mostly small, incomplete experiments with probability.  Not really meant for public use. 


# How to install and run

    # create and activate virtual environment
    python -m venv venv
    source venv/Scripts/activate
    
    # install to current environment (with current dir at top of repo) 
    pip install .     # "static" install
    pip install -e .  # "editable" install (setup.py handles source being under `src/`)

    # run scripts
    python -m cant_stop.calculator
    python -m backgammon.visual_odds_calc
    python -m risk.dice_roll_simulator
    
    # run linting
    pylint src/ --extension-pkg-whitelist=wx --disable=invalid-name --disable=line-too-long --disable=missing-function-docstring --disable=too-many-instance-attributes --disable=too-few-public-methods --disable=too-many-ancestors
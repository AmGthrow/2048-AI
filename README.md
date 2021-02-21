# 2048-AI
An AI that automatically plays 2048 on https://play2048.co/


## Installation and Usage

### Setting up
Run `pip install -r requirements.txt` to install all the dependencies.

### For running the AI
1. Open a terminal or command prompt inside the project's directory
2. run `play.py <num_moves> <num_trials> <num_runs>`
    You should see an automated Chrome browser open 2048.html and play 2048 with no need for input.

### For viewing results from previous trials
Results from all the trials are stored into a sqlite database, which you can access easily using some helper functions.


For retrieving all results, sorted by high score:

```
>>> import read_database
>>> read_database.get_all()
TRIAL #2
            num_moves  = 4
            num_trials = 100
            HIGH SCORE = 32468
            WIN: yes
            
TRIAL #1
            num_moves  = 3
            num_trials = 150
            HIGH SCORE = 16108
            WIN: no
```
# 2048-AI
An AI that automatically plays 2048 on https://play2048.co/

## Overview
<img src="https://s4.gifyu.com/images/ezgif.com-gif-maker-104efd394fe0d1a21.gif" height="500">

The AI uses a Monte Carlo search tree to determine the best move given any state of the AI. This can be broken down into 4 steps.

 - **Selection**
    - The AI is given a starting board from which its supposed to select a best move. There are only 4 possible moves at most in any board (up, down, left, right) and the AI selects whichever moves are still valid, skipping over moves that it can't actually make.
 - **Expansion**
    - From the starting board, the AI tries to simulate performing the selected move and records how many points it got from it.
 - **Simulation**
 - **Backpropogation**
## Installation and Usage

### Setting up
Run `pip install -r requirements.txt` to install all the dependencies.

### For running the AI
1. Open a terminal or command prompt inside the project's directory
2. run `play.py <num_moves> <num_trials> <num_runs>`
    You should see an automated Chrome browser open 2048.html and play 2048 with no need for input.

### For viewing results from previous trials
Results from all the trials are stored into a sqlite database, which you can access easily using some helper functions included in `read_database.py`.

Functions which can be used to access previous results easily are:
 - `read_database.get_all()`:  Retrieve all results and returns a list of tuples of the format (attempt_no, num_moves, num_trials, high_score,  did_win)
 - `read_database.get_wins()`:  Same as `get_all()` but only retrieves winning results
 - `read_database.get_win_rate()`:  Get the win rate of all the results
 - `read_databse.get_avg_score()`:  Get the average score of all the trials
 - `read_database.erase_all()`:  Remove all results currently in the database


For example, say the database currently looks like this.
```
TRIAL #1
            num_moves  = 3
            num_trials = 150
            HIGH SCORE = 16108
            WIN: no
TRIAL #2
            num_moves  = 4
            num_trials = 100
            HIGH SCORE = 32468
            WIN: yes 
```                   

Running each of the functions above would look like this:

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

[(2, 4, 100, 32468, 1), (1, 3, 150, 16108, 0)]     
>>> read_database.get_wins()

TRIAL #2
            num_moves  = 4
            num_trials = 100
            HIGH SCORE = 32468
            WIN: yes

[(2, 4, 100, 32468, 1), (1, 3, 150, 16108, 0)]

>>>read_database.get_win_rate()
WIN RATE: 50%

>>>read_database.get_avg_score()
AVG SCORE: 24,288
```
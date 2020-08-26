# Python3 version of UC Berkeley's CS 188 Pacman Capture the Flag project

### Pacman CTF
The challenge is to design agents to play Capture-the-Flag in a Pacman-like arena.

![Pacman Game Layout](/images/cft.png)

### Running the Agent:
To run our working agent.

run `python3 capture.py -r qTeam -b baselineTeam -l defaultCapture`

# Team Red-and-Blue

Welcome to our agent, our agent is designed to learn through reinforcement learning. We the use of features and weights we are able to use a linear function to approximate game states and based on the agents actions it will recieve rewards. For example if our pacman sees a ghost, at first the agent will not consider the ghost to be a threat, but will soon learn through negative rewards that being eaten by a ghost this not offer great rewards and will over time learn to avoid a ghost if it comes acrosss one.

A team is made up of two agents. Our agents work indepentdly from one another, we are able to achieve this by using two seperate policies. We made the design choice to actively have an offensive and defensive agent, although both can participate in offense and defense, each agent will get rewarded respecfully with regards to their role. This will populate to different policies that can work independently from one another. Although our agent's are independent they do work together, by providing information to one another. This allows for more role based team creation.

The agents are implemented using approximate q learning. This method allows the agent to adjust it's weights as it explores game states in the beginning of its learning phases. The agent explores more often in the beginning stages and as games progress it will more often exploit states it is already aware of when it knows the rewards. Our learning sessions are about 1000 games, after that our agents will have a working policy to exploit from.

### Reinforcement Learning
We use the register intial

![Reinforcement Learning](/images/reLearning.png)

`qTeam.py` has the code for generating a team of two agents using approximate q learning. Each agent works independently with the help of its teamate, both agents have and use their own policy to learn and make decisions based on the current game state. Using linear approximation we extract features from the game state to approximate a general state overall. This allows the agents to learn through generalizing the game state and adjusting their weights accordingly. Both agents have different reward systems in order to train the agents differently, this will allow for a more robust training simulation.

### Approximate Q Learning Structure

![Approximate Q Learning](/images/approxQLearning.png)

![Difference](/images/difference.png)

![Exact Q Value](/images/exactQ.png)

![Weight Update](/images/weightUpdate.png)


### Finder Class
`finder.py`

### Agent1

### Agent2

---
### Rules of the game

**Layout:** The Pacman map is divided into two halves: blue (right) and red (left).  Red agents (which all have even indices) must defend the red food while trying to eat the blue food.  When on the red side, a red agent is a ghost.  When crossing into enemy territory, the agent becomes a Pacman.

**Scoring:**  When a Pacman eats a food dot, the food is stored up inside of that Pacman and removed from the board.  When a Pacman returns to his side of the board, he "deposits" the food dots he is carrying, earning one point per food pellet delivered.  Red team scores are positive, while Blue team scores are negative.

**Eating Pacman:** When a Pacman is eaten by an opposing ghost, the Pacman returns to its starting position (as a ghost).  The food dots that the Pacman was carrying are deposited back onto the board.  No points are awarded for eating an opponent.

**Power capsules:** If Pacman eats a power capsule, agents on the opposing team become "scared" for the next 40 moves, or until they are eaten and respawn, whichever comes sooner.  Agents that are "scared" are susceptible while in the form of ghosts (i.e. while on their own team's side) to being eaten by Pacman.  Specifically, if Pacman collides with a "scared" ghost, Pacman is unaffected and the ghost respawns at its starting position (no longer in the "scared" state).

**Observations:** Agents can only observe an opponent's configuration (position and direction) if they or their teammate is within 5 squares (Manhattan distance).  In addition, an agent always gets a noisy distance reading for each agent on the board, which can be used to approximately locate unobserved opponents.

**Winning:** A game ends when one team eats all but two of the opponents' dots.  Games are also limited to 1200 agent moves (300 moves per each of the four agents).  If this move limit is reached, whichever team has eaten the most food wins. If the score is zero (i.e., tied) this is recorded as a tie game.

**Computation Time:** Each agent has 1 second to return each action. Each move which does not return within one second will incur a warning.  After three warnings, or any single move taking more than 3 seconds, the game is forfeit.  There will be an initial start-up allowance of 15 seconds (use the `registerInitialState` method). If you agent times out or otherwise throws an exception, an error message will be present in the log files, which you can download from the results page (see below).

### Original Licensing Agreement (which also extends to this version)
Licensing Information:  You are free to use or extend these projects for
educational purposes provided that (1) you do not distribute or publish
solutions, (2) you retain this notice, and (3) you provide clear
attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

Attribution Information: The Pacman AI projects were developed at UC Berkeley.
The core projects and autograders were primarily created by John DeNero
(denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
Student side autograding was added by Brad Miller, Nick Hay, and
Pieter Abbeel (pabbeel@cs.berkeley.edu).

### This version attribution
This version (cshelton/pacman-ctf github repo) was modified by Christian
Shelton (cshelton@cs.ucr.edu) on June 23, 2020 to run under Python 3.
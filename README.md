# Python3 version of UC Berkeley's CS 188 Pacman Capture the Flag project

### Pacman CTF
The challenge is to design agents to play Capture-the-Flag in a Pacman-like arena.

![Pacman Game Layout](/images/cft.png)

### Running the Agent:
To run our working agent.

run `python3 capture.py -r qTeam -b baselineTeam -l defaultCapture`

# Team Red-and-Blue

Welcome to our agent, our agent is designed to learn through reinforcement learning. With the use of features and weights we are able to use a linear function to approximate game states and based on the agent's actions it will recieve rewards. For example if our pacman sees a ghost, at first the agent will not consider the ghost to be a threat, but will soon learn through negative rewards that being eaten by a ghost, this does not offer great rewards and will over time learn to avoid a ghost if it comes across one.
 
A team is made up of two agents. Our agents work independently from one another, we are able to achieve this by using two separate policies. We made the design choice to actively have an offensive and defensive agent, although both can participate in offense and defense, each agent will get rewarded respectfully with regards to their role. This will populate to different policies that can work independently from one another. Although our agents are independent they do work together, by providing information to one another. This allows for more role based team creation.
 
The agents are implemented using approximate q learning. This method allows the agent to adjust it's weights as it explores game states in the beginning of its learning phases. The agent explores more often in the beginning stages and as games progress it will more often exploit states it is already aware of when it knows the rewards. Our learning sessions are about 1000 games, after that our agents will have a working policy to exploit from.


### Design Layout

![Class Design](/images/finalDesign.png)

### Reinforcement Learning

Each of our agents will update based on their current position in the environment. Using the state, action, and reward to update its policy.

<!--![Reinforcement Learning](/images/reLearning.png)-->
<img src="/images/reLearning.png" width=400 align=middle>

Using the algorithm below for approximate q learning, obtain the Q value based on the weights and features the agent finds in the current state space.

<!--![Approximate Q Learning](/images/approxQLearning.png)-->
<img src="/images/approxQLearning.png" width=400 align=middle>

In order for the agent to learn, it must be able to update its weights based on its experience. To properly mitigate this we calculate the difference of the current state from the previous state as seen the algorithm below.

<!-- ![Difference](/images/difference.png) -->
<img src="/images/difference.png" width=400 align=middle>

We can then now update the current Q value by adding both difference and current Q(s,a)*learning rate.

<!--![Exact Q Value](/images/exactQ.png)-->
<img src="/images/exactQ.png" width=400 align=middle>

Once have complete the calculations for the q values we are able to update the agents weights to associate the values earn in the game state with its learning rate using the calculated difference and the current active features.

<!--![Weight Update](/images/weightUpdate.png)-->
<img src="/images/weightUpdate.png" width=400 align=middle>

Although we are able to approximate and adjust weights accordingly, the agents policy will never converge and also causes a ballooning effect to occur. This is one of the issues that comes with approximate q learning. We have implemented certain tools to diminish those effects.

### Approximate Q Learning Structure

`qTeam.py` has the code for generating a team of two agents using approximate q learning. Each agent works independently with the help of its teammate, both agents have and use their own policy to learn and make decisions based on the current game state. Using linear approximation we extract features from the game state to approximate a general state overall. This allows the agents to learn through generalizing the game state and adjusting their weights accordingly. Both agents have different reward systems in order to train the agents differently, this will allow for a more robust training simulation.

- `def chooseAction` This function calls `def update` to update the current q values for the game state the agent is in. Once it has computed its values and weights, it will determine an action to take. The action is selected based on the `EXPLORING` rate and using a coin toss to determine its action. If the exploring rate is set high, it will take random actions in the beginning episodes of its training.

- `def update` This is called from `chooseAction`, this is where the core of approximate q learning takes place. In this action the agent will update the q values discussed above and its weights. With the use of a buffer to average out values, discussed below, each agent will update the learning weights based on the active features of the game state.
 
- `def get/write Policy` Two things must be accomplished with this function, keep a record of the buffer to be used for later episodes and accessing the policy after the agent has trained for x number of episodes.
 
- `def getReward` This generates the reward for the given state and passes the value into the `update` function.
 
- `def createTeam` allows us to create a team of two agents by passing in their class as the parameters, this also allows us to create shared objects between both agents. We instantiate the `locationFinder` object and pass it in as a parameter for both agents to use and update. This allows us to gather features for both agents and additionally communicate further information if need be.
 
`finder.py` is a class used to define our feature space within the game state environment. The agents use the finder class to populate certain features that have been designed for specific role based goals. Thus allowing the agents to gather to approximate the state based on the active features and allowing them to update their weights/policy accordingly
 
#### Feature Space
These are the features we have implemented for the agent to have access to, but not all are active as some can be detrimental in learning process.

- closestFood
- neaarestEatenFood
- isScared
- nearestPowerPellet
- randomClosestFood
- ghostsNear
- pacmanNear
- inTunnel
- inDeadend
- scaredGhostNear
- foodCarrying
- isScared
- deadend

#### Buffer
Do the issues of approximate q learning, there is a ballooning effect as each agent learns through the number of episodes. Values will go towards infinity in either positive or negative fashion. In order to counter this effect we implemented a buffer to store last 1,000 values and rewards. As each agent updates the Q value difference, as discussed above, it will instead sample a 100 instances from the buffer and average out the current q value to be used instead of the actual current q value.
 
This prevents the values from hitting astronomical values and also gives the agent a more approximated experience over time based on its past action and rewards.
 
### Agent1
This is our offensive agent, this agent is designed to learn by eaten pellets, scoring, and avoiding being eaten. The ideal expectancy for this agent is to avoid ghost at all costs. Gather if the situation is allowed and if there is a possible threat to retreat and score.
 
### Agent2
This is our defensive agent, this agent is designed to learn by being rewarded for eating the opposing teams pacman. The ideal expectancy for this agent is to hover around the team's pellets and seek out enemy pacman to eat.

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

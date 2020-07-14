# Agent 0

Our agent 0 is broken up into an offensive and defensive classes, this is similarly to how the baselineTeam agent is set. Our initials thoughts are to defend the power pellet and guard the surrounding area while the offensive agent gathers food cautiously, four pellets at a time. We decided on this strategy given the rules of the game.

We broke up the work using those two classes, one member works solely on the offensive while the other works on the defensive agent.

## Offensive Agent Strategy

THe offensive agent is always looking for the nearest food to eat, this is calculated with the given features of a successorScore, distanceToFood, numGhost, ghostDistance, and stop. The offensive agent takes into account the given features based on its position and evaluate the situation with the provided data. Once the offensive agent is able to obtain 4 pellets his new priority is to return back to drop off the pellets. If the agent were to die in the process, it will restart the process to eat more pellets.

## Denfensive Agent Strategy

## Overall Assessment

Currently our agents have very little actions to evaluate from and thus have a very adverserial approach. We can encounter many issues from this approach since the agents only account for there upcoming state, optimals paths are being ignored. Although, they fair well againts the baselineTeam, we can already see potential issues with a more savy agent.

Upcoming changes, for the offensive agent give him many instances to evaluate or learn from using reinforcement learning. one of the hurdles to overcome is knowning the agents position and using that information in our model.
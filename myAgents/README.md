# Agent 0

Our agent 0 is broken up into an offensive and defensive classes, this is similar to how the baselineTeam agent is set up. Our initial thought is to defend the power pellet and guard the surrounding area while the offensive agent gathers food cautiously, four pellets at a time. We decided on this strategy believing it is a simple and effective strategy for the first version of our agents.

We broke up the work using those two classes, one member works solely on the offensive while the other works on the defensive agent.

## Offensive Agent Strategy

The offensive agent is always looking for the nearest food to eat, this is calculated using the given features of a successorScore, distanceToFood, numGhost, ghostDistance, and stop. The offensive agent takes into account the given features based on its position and evaluate the situation with the provided data. Once the offensive agent is able to obtain 4 pellets his new priority is to return back to drop off the pellets. If the agent were to die in the process, it will restart the process to eat more pellets.

## Denfensive Agent Strategy

The defensive agent starts by heading towards the power pellet to defend it. Once it is there it will start moving in the direction of the closest hazzy distance. If a food pellet disappears the agent will be incentivised to move towards that location to investigate and try to find the pacman, but if it does not find anything will go back towards the pellet. The top priority for this version is to guard the area around the power pellet so the invading pacmen can only safely get the outside food.

## Overall Assessment

Currently our agents have very few actions to evaluate from and thus have a very adverserial approach. We can encounter many issues from this approach since the agents only account for their upcoming state, optimal paths are being ignored. They fair well against the baselineTeam, however, we can already see potential issues against a smarter, more savy agent.

Upcoming changes, for the offensive agent give him many instances to evaluate or learn from using reinforcement learning. one of the hurdles to overcome is knowning the agents position and using that information in our model. For the defensive agent the plan is to use reinforcement learning to allow the agent to explore its side and find the best areas to patrol to catch the pacman at.

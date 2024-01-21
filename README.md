Twenty Forty Eight
-------------

This is a simple environment created for 
[gymnasium](https://gymnasium.farama.org/) its 
built to support classic search as well as being used
for reinforcement learning (the primary purpose of most 
gymnasium environments).

To be sure that all pip prerequisites are installed first,
use the `Makefile` in [prerequisites](prerequisites/).

The gymnasium environment is contained completely in [twenty-forty-eight](twenty-forty-eight/). 
Use the `Makefile` in that directory to install the module in your local
pip. Note that this does not copy the module, it sets a link to this
location. This is convenient for making updates after installing it.

[demo-agents](demo-agents/) has a random agent and a MAXMAX search agent, (also a Multithreaaded version), 
to demonstrate the use of the environment and the model
side-by-side in running the environment and searching for solutions.



# 2048-Gym-AI-Environment

# Overall Road-MAPs

This is the overall roadmaps of my research plan in the next two years. From Sep-2019 to Jan-2021, sixteen month in total.

I am going to reach the following goals before the deadline(31-Jan-2021):

- Proficient the Statistical Mechanics
- Have the Julia-base atomic-CE package
- Use a proper way to describe CZTS order-disorder transition
- Co-develop the aiida-alloy plugin
- Co-develop the aiida-DPMD plugin

## Phase transition of alloy system

This is the main topic I will focus so that all the learning staff and resource have the root and the learning direction is clear. 

First of all, To study the phase transition I need the fundamental of statistical mechanism. 
I need to decide which thermodynamic way should be used when calculating the phase diagram. I start to use CE way to simulate the vibarate entropy at the high temperatue, but it is a way of 90s which is unaccuracy now. The study the thermodynamic behavior, I need the tool to sampling the configurations both on MC level and MD level and then evaluating the energy of the configuration. That is where the deepmd or atomic-cluster-expansion come in.

As for the missions to be done, a way to predict the energy is necessary. The DFT is valueless in the context because of its expensive cost. So I focus on atomic cluster expansion potential which slightly modified the ordinary cluster expansion framework with atomic disposition as addition. That is why I need my own version of CE code so I can extensive it with the new feature. 

### Learning Statistical Mechanics

I have the first taste of the rudimental statistical mechanics by learning *Statistical Mechanics: Algorithm and Computation* (SMAC). After learning the SMAC in the two month(Sep to Nov 2019), I master the following skills:

- Many kinds of sampling method and their pros and cons.
- Can simulate the BEC by using path-integral MC.

Then I am going to study the course 

- [8-333 Statistical Mechanics I: Statistical Mechanics of Particles](https://ocw.mit.edu/courses/physics/8-333-statistical-mechanics-i-statistical-mechanics-of-particles-fall-2013/)
- [8-334 Statistical Mechanics II: Statistical Mechanics of Field](w.mit.edu/courses/physics/8-334-statistical-mechanics-ii-statistical-physics-of-fields-spring-2014/)

The course have the notes and books.

### Julia-base CE package

Refractoring the icet code into Julia.
I create the repository named `Jually.jl`. It should include the all unittest for the upcoming practical code. The project are seperated into two parts.

First is the CE part, which includes the needed cluster expansion code that can do the cluster expansion. By input some trainning set which are configurations with eneries. The code can be easily used to evaluate the energy of new configurations of similar type. 

Second is the MC part, which is used to simulate the thermodynamic properties at the specific ensemble by using the Monte Carlo method. It is supposed to have the abilities to simulate the different kinds of ensembles and easily to be modified to adapt to other user defined ensembles. The Monte Carlo part should be also easy to modified to adapt the more acvanced MC algorithms. 

Lastly, prepare to add the feature to deal with the atom relaxed system somewhere in the code. 

### CZTS order-disorder transition

CuZnSnS (CZTS) is a semi-conductor system which have two degrees of order-disorder transition. One from order to pseudo-binary alloy at T=700k and the other from binary to ternary alloy at 1500K. 

Privious study theoritical studies can not simulate the second Tc precisely. There are two possible reason:

- The energy of the configuration at high temperature of disordered candidate is error evaluated. 
- The number of samplers is not enough or the supercell is not big enough to describe the transition phenomenon.
- Use the unproper way to simulating the Tc.

As I can tell, the first reason dominants. The second problem can be conquered by increase the supercell and increase the number of samplers. And the last one should be solved by using such as the thermodynamic integral (TI) rather than the ordinary MC simulation.

To settle the first problem, we must have a good enough force potential to accurately evaluating the energy of unknow configurations. 
The deviate from the DFT energy is cause by the unabilities to describe the atom relax in the framwork of cluster expansion.
Which lead me to update the current CE framework to atomic cluster expansion or using the machine-learning potential.
Also, It may be caused by the long-range interaction of the semi-conductor system. This is much harder to settled. 

The last problem is still unclear. If the vibration entropy is not to be included, the ordinary MC simulation is enough. If I am going to also describe the vibrational entropy and add it into the free energy, the advanced thermodynamic simulation might be needed. For instance, use the empiracal potential as the trailer and doing the TI. 


#### Plans and milestones

- [ ]Using CE to reproduce the MgAlO spinel order-disorder transition. And CE for Cu-Au
- [ ]Using EAM potential to describe the CuAu transition. 
- [ ]Here, not only do I use the eam as the simple energy evaluator, but use the it as the potential to do the advanced thermodynamic simulation.
- [ ]Training the potential function using DeepMD for the CZTS. (Look at Appendix for details)

## AiiDA plugins

### AiiDA-alloy

Now we have the documentations here, https://drive.google.com/drive/folders/1h_zNrcEDFG0UCgeaAms6iCCk8HA1W_WN

and discuss at the slack https://aiida-alloy.slack.com 

### AiiDA-DPMD

First what we need is a special data structure, which dirived from `StructureData` and can describe a serial of structures coming from the parent structure. This data should be seemed like `TrajectoryData`.

#### Auto-test part

Let the CCH prepare a roadmap of what need to be calculated. And for every properties that should be calculated, the details and steps needed.

#### Plugin for DPMD

Prepare a clear roadmap in doing this. 

About where to working together? Which repository? The sequence of the jobs. 

The goals we are going to reach. A metal demo might be good. With the user-scenario-UML.

At this project, the first thing should be a `CalcJob` for the DPMD-kit. I should know the format of input file and how to parse the result for each training step. Make a review after having the taste of DPMD-kit.

First, install the DPMD-kit and have a trail.

## Appendix 

### Roadmap of DPMD training for CZTS

Here I define the steps to training the potential of CZTS alloy by DPMD. 

1. The initial configurations are coming from the enumeration of small volume supercell
2. The exploration of the process are seperated into two level, first the temperature, second the MC+MD simulation.

The temperature range from 0K to 2000K which cover the experimental temperature of two order-disorder phase transition. 
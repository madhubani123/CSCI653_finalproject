# CSCI653_finalproject
Non-adiabatic molecular dynamics using machine learning

## Team Members

Goran Giudetti, Madhubani Mukherjee, Samprita Nandi (Names in alphabetical order)

## Abstract

It is proposed to study photoisomerization retinal via non-adiabatic molecular dynamics calculations. Application of  machine learning based protocol will enable the determination of the reaction coordinate. Whereas most of the quantum chemical calculations assess the adiabatic potential surfaces with fixed nuclei many chemically relevant processes, such as isomerization, proceed nonadiabatically and involve a concerted motion of electrons and nuclei. Very recent experiments involving femtosecond optical pump and x-ray probe pulses enabled study of the evolution of electronic states and the motion of the nuclei during isomerization reactions of cyclohexadiene for the first time. Similar techniques will likely be applied for the study of different systems of increasing complexity. The interpretation of the results requires the development of the computational techniques. Due to the multistate and multidimensional nature of isomerization reactions computation of the relevant potential energy surfaces (PES) and  the reaction coordinate is very costly. In this work, a neural network based machine learning technique is proposed  to  identify the most important internal coordinate by rank ordering all the internal coordinates. 

## System of interest
![retinal](https://user-images.githubusercontent.com/57571405/143783315-cb028241-f766-4aa1-b283-40980def8bad.png)

## Protocol
![flowchart](https://user-images.githubusercontent.com/57571405/143783537-a035af25-9446-4543-ae67-7f59c51b4983.png)


## Results and discussion

In this project we are first testing ab-initio molecular dynmics simulation, which is more commonly available in quantum chemical software packages than the non-adiabatic molecular dynamics simulation. We have run 50 AIMD trajectories which ends up in the cis conformation and 50 trajectories which ends up in the trans conformation starting near the transition state configuration. From the AIMD data, we have computed mutual information between the HOMO energy and internal coordinates at each time step. Then we have taken internal coordinates with highest MI values and performed principal component analysis. 

### Correlation plot for internal coordinates with highest mutual information

Positive values indicate positive correlation between variables, i.e. if one variable increases (decreases) the other one increases (decreases) too. Negative values indicate anticorrelation between variables, i.e. if one variable increases the other one decreases and vice versa.

![image](https://user-images.githubusercontent.com/57571405/187000270-cd22627b-616b-4ee6-a65e-74878c31a7cd.png)


### Principal Component Analysis
We apply Singular Value Decomposition (SVD) to the correlation matrix presented above. We plot then the Percent Variance Explained for each SV which allow us to identify which SV are associated with linear combinations of features that are redundant (smallest variance)

![image](https://user-images.githubusercontent.com/57571405/187000295-c66a01ab-bc44-4698-b825-b7dd53270f62.png)

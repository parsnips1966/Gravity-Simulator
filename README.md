# Gravity-Simulator

My AQA A Level Computer Science NEA Coursework

2D sandbox which allows the user to create their own gravitational systems, simulating how they evolve over time and providing data about them.


Description from my A level Computer Science NEA coursework document:

My project will be a gravitational simulator. This means that the user can create solar and planetary systems with starting conditions and then play the simulation to watch the system evolve over time. It will be able to be used for educational purposes as the users will learn about how gravity works on the largest scales, but it can also be used for fun. There will be options for the users to choose to make a new simulation or view their old ones. The users can click and type to modify parameters and add bodies. If the users want, there will be an option to view lots of ‘behind-the-scenes’ data which the program will calculate about the system.

The key part of my system will be the simulation engine and the algorithms which control it. The algorithms will be accurate enough to serve all purposes that a casual user could require – data being correct to 6 to 10 significant figures. They take data about bodies which the user has input or imported and perform operations on it to create an output which is displayed on screen.
This leads onto the other main part which is the graphical display of the system. The screen will be updated each frame with the new positions of each body, and a faint trail of their previous positions. The distances between bodies will be to scale, but the sizes of the bodies will not so they can be seen by a user. An algorithm will calculate the screen sizes so their radii are evenly distributed within a range of ~20 pixels. 
The user interface will be clear and as simple as possible to make it easy to use. The focus of the system is the simulation functionality, and the appearance is not as important to users. A lot of screen space will need to be dedicated to user input data and output data so I must use the space efficiently. 

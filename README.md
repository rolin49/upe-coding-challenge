# Introduction

This repository contains my implementation for the solution to the UCLA UPE
Fall 2018 Coding Challenge as specified on
https://gist.github.com/austinguo550/381d5e30d825b90900ef60fa39a806f4?fbclid=IwAR00l_HU1uP6ujQZ-p9ZQhqG1NeXB8T39NMibicWMlDmZfXHCOfZ_9-LPUw.

# Building and running

Since the program is written in Python, no building is required.

To run the program, type 'make' into the command line while in the
directory.

When the program starts running, it will output some introductory messages, but
will very quickly begin printing the maze as it is solved so as not to waste
time. You can watch the solution progress in real time since the program
outputs the maze after every move made.

As a location in the maze is visited, it is marked with an 'o'. When a location
is found to be a wall, it is marked with an '*'. When a location is found to be
a dead end (no paths starting from it will lead to the end of the maze), it is
marked with a 'd'. When the last maze is complete, the program will report a
success message and exit.

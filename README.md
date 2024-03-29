# Particle-fun
Easy-to-use visualization of random or gravity-driven particle movement with elastic interactions

## Getting Started
This repository contains the building blocks to make a visualzied 3D multiparticle simulation. Particle movement is initially
randomized, but can be set to any arbitrary distribution that the user desires by altering the initialize_particles function.
Standard settings impose elastic collisions when a particle collides with itself or a wall of the box, unless grav == True and then 
the particles experience an inelastic collision with the x-plane. 

## Installing

particle_core.py contains all necessary functions and classes to run the simulations. 

*This repository utilizes ipyvolume, which to the best of my knowledge is only available using Jupyter notebook. The code will not run if you do not use a system that is compatible with ipyvolume.*

An easy way to do this if you're working with a non-compatible system is to use a site such as Cocalc - ensuring that you are using the classic notebook setup. https://cocalc.com/

## Simulating Particles

Below are two examples of possible out-of-the-box simulations. It is recommended that the time_step remains sufficiently low such particle bouncing does not "explode"
Similarly, when running "falling particles" simulations it is recommended that the total_time is not set too high such that settled particles do not get caught in infinite bouncing loops with the x-plane.

**Example 1: Randomized bouncing particles**\
This simulation generates a series of 30 particles bouncing between one another.
#### Input
num_particles = 30\
box_size = 10\
total_time = 1000\
time_step = 0.02\
particle_radius = 0.5

particleSimulate(num_particles, box_size, total_time, time_step, particle_radius)

#### Output

![](https://github.com/cameronmcelfresh/particle-fun/blob/master/bouncing_particles.gif)


**Example 2: Randomized falling particles**\
This simulation generates a series of 40 particles "falling" from an initialized state. Here, the resulting video is also saved.
#### Input
num_particles = 30\
box_size = 10\
total_time = 1000\
time_step = 0.01\
particle_radius = 0.5

particleSimulate(num_particles, box_size,  total_time,  time_step,  particle_radius,  grav = True,  save = True)

#### Output

![](https://github.com/cameronmcelfresh/particle-fun/blob/master/falling_particles.gif)

## Extending The Simulation

Some very simple modifications could be introducted to the current skeleton to explore or visualize different processes. Those include but are not limited to:
  - Adding attractive potentials between particles (molecular dynamics)
  - Specifying particles of varying mass
  - Coagulation of particles to form larger networks or droplets

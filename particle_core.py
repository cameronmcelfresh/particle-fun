"""
Created on Tue May 28 12:19:57 2019

@author: Cameron
"""

import numpy as np
import ipyvolume as ipv #requires Juypter notebook classical version (CoCalc.com)


"""Define the particle class"""

class Particle():
    """A class to hold each particle's position and velocity vecotrs"""
    
    def __init__ (self, pos_vec, vel_vec, box_size, time_step, grav):
        """Initialize particle by giving a 3x1 position and velocity vector"""
        self.pos = pos_vec #3D coordinates of position
        self.vec = vel_vec #3D velocity vector
        self.grav = grav #Bool to determine whether or not the environment has gravity
        self.box_size = box_size #Holds the value of the box size it is in
    
    def pos_update(self, time_step):
        """Simulates updating the particle's 3D location """
        
        """First test to see if you have reached the boundary, if so, flip the 
        respective velocity vector. Also consider bouncing off the x-y plane to
        be inelastic - so particles lose veloctiy """
        
        for i in range(3):
            if self.pos[i] > self.box_size:
                self.vec[i] = self.vec[i]*-1
                self.pos[i] += -(self.pos[i]-self.box_size)

            if self.pos[i]<0:
                self.vec[i] = self.vec[i]*-1
                self.pos[i] += -self.pos[i]
        
                if self.grav == True:
                    """If the ball comes into contact with the x-y- plane, make the collision
                    inelastic and decrease the velocity vector"""
                    if i==2:
                        self.vec = self.vec*0.8
       
        if self.grav == True: 
            """Update for graviity acting in the z-direction"""
            self.vec[2]= self.vec[2]-time_step*1
        
        """Finally, update the position vectors"""
        self.pos[0] += self.vec[0]*time_step
        self.pos[1] += self.vec[1]*time_step
        self.pos[2] += self.vec[2]*time_step
        

"""Define the particle initialization function"""

def initialize_particles(number_of_particles,box_size,time_step, grav = False):
    """Function to generate all of the initialized particles and normalize their velocities, 
    and return them all in a list"""
    
    
    """Velocity description"""
    #Generate randomly distrubuted velocities
    velocities = np.random.randn(number_of_particles,3)
    
    #Extract the mean velocity value
    mean_vel = np.full([number_of_particles,3], np.mean(velocities, axis=0))
    
    #Normalize all velocities to zero
    velocities = np.subtract(velocities,mean_vel)
    
    #Remove all z-velocities so particles only have an x,y component (for simplicity)
    velocities[:,2] = 0
    
    """Position description"""
    pos_vec = np.random.random([number_of_particles,3])*box_size #Generate random positions
    
    particle_list = [] #Empty list to hold particle classes
    
    for i in range(number_of_particles): #Populate the list
        particle_list.append(Particle(pos_vec[i,:], velocities[i,:], box_size,time_step, grav))
        
    return particle_list

def bounce(particle1,particle2, particle_radius, time_step):
    """Function to calculate the updated velocity vectors due to interparticle bouncing"""
    #print(str(tot_eng(particle_list))) #Used to track the total energy of the particles
    a = particle1.pos - particle2.pos
    b = (a[0]**2 + a[1]**2 + a[2]**2)**(1/2)
    n = np.divide(a,b,out=np.zeros_like(a), where=b!=0)       
      
    #Relative Velocity
    v_rel = particle1.vec - particle2.vec
    
    #Relative velocity along the normal direction
    v_norm = np.dot(v_rel,n)*n
    
    particle1.vec += -v_norm
    particle2.vec += +v_norm
#    particle1.vec += (v_norm2-v_norm1)    
#    particle2.vec += (v_norm1-v_norm2)

    #Move the particles apart until they are further than the bounce seperation distance
    while particledist(particle1, particle2)<(2*particle_radius):
        particle1.pos_update(time_step)
        particle2.pos_update(time_step)


def particledist(particle1, particle2):
    """Function to determine interparticle distance"""
    r_x = particle1.pos[0] - particle2.pos[0]
    r_y = particle1.pos[1] - particle2.pos[1]
    r_z = particle1.pos[2] - particle2.pos[2]
    
    r = (r_x**2 + r_y**2 + r_z**2)**(1/2)
    
    return r
    
def isbounce(particle_list, particle_radius, time_step):
    """Function to determine whether or not two particles, bounce, if so,
    update their velocities and positions"""
    
    #Loop through all of the particle pairings
    for particle1 in particle_list:
        for particle2 in particle_list:
            
            #If the seperation is small enough, call the bounce function
            if particledist(particle1,particle2)<2*particle_radius and particledist(particle1,particle2)!=0:
                
                bounce(particle1, particle2, particle_radius, time_step) #Call bounce function

def avgvel(particle_list):
    """Function to measure the average velocity of the particles"""
    vel_vec = np.array([0,0,0])
    for particle in particle_list:
        vel_vec =vel_vec + particle.vec
        
    avg_vec = vel_vec/len(particle_list)
    
    return avg_vec

def tot_eng(particle_list):
    """Function to measure the total energy of the system"""
    tot_eng = 0
    for particle in particle_list:
        tot_eng = tot_eng + particle.vec[0]**2 + particle.vec[1]**2 + particle.vec[2]**2
        
    return tot_eng

"""Function to run the entire simulation and display the plot"""
def particleSimulate(num_particles, box_size, total_time, time_step, particle_radius,
                     grav = False, save = False):
    
    print("Running simulation...")
    
    """Run the simulation and extract the x,y,z coordinates to plot the particle's path"""
    particle_list = initialize_particles(num_particles, box_size, time_step, grav) #Generate starting points
    
    x=np.zeros([total_time,num_particles,1])
    y=np.zeros([total_time,num_particles,1])
    z=np.zeros([total_time,num_particles,1])
    
    time = 0
    
    #print(str(tot_eng(particle_list))) #Used to track the total energy of the particles
    
    while time < total_time: #Loop through iterations of particle movements
        
        #Check to see if bouncing occurs
        isbounce(particle_list, particle_radius, time_step)    
        
        
        for i in range(len(particle_list)):
            particle_list[i].pos_update(time_step) #Update position
            
            x[time,i] = particle_list[i].pos[0]
            y[time,i] = particle_list[i].pos[1]
            z[time,i] = particle_list[i].pos[2]
        
        time += 1
        
        if (time/total_time)*100%10==0:
            print(str(time/total_time*100) + "% complete")
        
    """Plot the results of all of the particle movements"""
    
    colors = []
    for i in range(num_particles):
        colors.append([np.random.random(),np.random.random(),np.random.random()])
    
    ipv.figure()
    s = ipv.scatter(x, z, y, color = colors , size=7, marker="sphere")
    ipv.animation_control(s, interval=1)
    ipv.xlim(-1,box_size+1)
    ipv.ylim(-1,box_size+1)
    ipv.zlim(-1,box_size+1)
    
    ipv.style.axes_off()
    ipv.show()
    
    if save == True:
        print("Saving the video of the simulation in the current directory...")
        ipv.save('./particle_sim.html')
        

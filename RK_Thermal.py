import numpy as np
import math
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

Mb = 0.7  #Mass of Body [Kg]
Mp = 0.01 #Mass of Pad [Kg]
g = 1.622  #Gravitational Acceleration [m/s^2] 
k1 = 1.4   #Bias Spring Coefficient [N/mm]
l0 = 100  #Natural Length of Bias Spring [mm]
k2 = 10  #Spring Coefficient of the ground [N/mm]
c2 = 10  #Damping Coefficient [Ns/mm]
Z20 = 0.0  #Initial Position of Pad [mm]
DZ = 50    #Initial Deflextion of Bias Spring [mm]
h = 0.1   #Interval of RK
d = 1    #Diameter of SMA wire [mm]
D = 6.8  #Diameter of SMA coil [mm]
n = 10   #Number of coil spring
rho = 6.5*10**-3 #Density of SMA wire [g/mm^3]
print("Density of SMA wire [g/mm^3]")
print(rho)
#rho = 1
r = math.sqrt(math.pi*d*D*n/4) #radius of pseudo sphere of SMA[mm]
print("radius of pseudo sphere of SMA[mm]")
print(r)
A = math.pi*r**2 #Cross section of the pseudo sphere of SMA[mm^2]
print("Cross section of SMA pseudo sphere [mm^2]")
print(A)
#A = 1
AA = 4*math.pi*r**2 #Surface are of SMA pseudo sphere [mm^2]
print("Surface area of SMA pseudo sphere [mm^2]")
print(AA)
#AA = 1
Theta_L = 45  #Lattitude [deg]
m = rho*(math.pi*(0.5*d))**2*D*n #Mass of a SMA spring [g]
print("Mass of SMA[g]")
print(m)
#m = 1
c = 440*10**-3  #Specific heat capacity of SMA spring [J/gK]
#c = 500 
Sc = 1366*10**-6 #Solar constant [W/mm^2]
#Sc = 1
delta = 5.67*10**-2 #Stefan-Boltzman constant [W/mm^2K^4]
#delta = 1
a = 0.07 #Albedo constant
#a = 1
Tg = 100 + 273.0 #Temperature of the ground[K]
#Tg = 1
epsilon = 0.6 #Emissivity of the ground
TB = 50 + 273.0
tB = 1
mB = 1
aB = 1
AB = 1
#ThetaB = 1
ScB = 1
cB = 1
#epsilonB = 1
deltaB = 1
m_ = m/mB
a_ = a/aB
A_ = A/AB
AA_ = A/AB
Sc_ = Sc/ScB
c_ = c/cB
delta_ = delta/deltaB

def func1(x):
    return [x[1], (k1/Mb)*(l0-(x[0]-x[2]))-g, x[3], (k1/Mp)*(l0-(x[0]-x[2])\
	)-(k2/Mp)*(x[2]-Z20)-(c2/Mp)*x[3]-g]

def func2(x, t):
    return [x[1], (k1/Mb)*(l0-(x[0]-x[2]))-g, x[3], (k1/Mp)*(l0-(x[0]-x[2])\
	)-(k2/Mp)*(x[2]-Z20)-g]
	
#def motion_test(x):
	#return np.array([x[2],x[1],x[0]])

def motion_test(x):
	return np.array([x[1],-g])

def ThermalEq1(x): #where Tg >= Tb
	value1 = A*math.cos(math.radians(Theta_L))*Sc/(m*c)
	print("value1")
	print(value1)
	value2 = a*A*math.cos(math.radians(Theta_L))*Sc/(m*c)
	print("value2")
	print(value2)
	value3 = epsilon*delta*A*(Tg**4-x[0]**4)/(2*m*c)
	print"(Tg/TB)**4 = {0}" 
	print(Tg/TB)
	print"(Tb/TB)**4 = {0}".format((x[0]/TB)**4)
	print("value3")
	print(value3)
	value4 = delta*AA*(x[0]**4-4**4)/(m*c)
#	value4 = delta*A*((x[0]/TB)**4-(4/TB)**4)/(m*c)
	print("value4")
	print(value4)
	q = value1 + value2 + value3 - value4 
#	q = value1 + value2 
	return q

def ThermalEq2(x):   #where Tb > Tg
	value1 = A*math.cos(math.radians(Theta_L))*Sc/(m*c)
	print("value1")
	print(value1)
	value2 = a*A*math.cos(math.radians(Theta_L))*Sc/(m*c)
	print("value2")
	print(value2)
	value3 = delta*A*((x[0])**2 + (Tg)**2)*((x[0])**2 - (Tg)**2)/(2*m*c)
	print("value3")
	print(value3)
	value4 = delta*AA*((x[0]/TB)**4-(4/TB)**4)/(m*c)
	#value4 = delta*AA*((x[0]/TB)**4-(4/TB)**4)/(m*c)
	print("value4")
	print(value4)
#	q = value1 + value2 - value3 - value4 
	q = value1 - value3 - value4
	return q

'''	
def RK(x):  
	k1 = motion_test(x)
	k2 = motion_test(x+0.5*h*k1)
	k3 = motion_test(x+0.5*h*k2)
	k4 = motion_test(x+h*k3)
	x_ = x + (h/6)*(k1+2*k2+2*k3+k4)
	#print(x_)
	return x_
'''
def RK1(x): #Where Tg >= Tb 
	k1 = ThermalEq1(x)
	k2 = ThermalEq1(x+0.5*h*k1)
	k3 = ThermalEq1(x+0.5*h*k2)
	k4 = ThermalEq1(x+h*k3)
	x_ = x + (h/6)*(k1+2*k2+2*k3+k4)
	#print(x_)
	return x_
#'''
def RK2(x): #Where Tb > Tg 
	k1 = ThermalEq2(x)
	k2 = ThermalEq2(x+0.5*h*k1)
	k3 = ThermalEq2(x+0.5*h*k2)
	k4 = ThermalEq2(x+h*k3)
	x_ = x + (h/6)*(k1+2*k2+2*k3+k4)
	#print(x_)
	return x_

def Cal_Mtlx(X0, t_s, t_f, l):
	XX = np.empty((0,l), float)
	XX = np.append(XX, np.array([[X0[0]]]), axis=0)
	t = t_s
	n = 0
	while(t<t_f):
			if XX[n] <= Tg/TB:
				Step = RK1(XX[n])
				print("Using RK1 where Tb <= Tg")
				print(n)
				S = np.array([[Step[0]]])
				#S = np.array(Step)
				XX = np.append(XX, S, axis=0)
				t = t+h
				n = n+1
			else:
				Step = RK2(XX[n])
				print("Using RK2 where Tb > Tg")
				print(n)
				S = np.array([[Step[0]]])
				#S = np.array(Step)
				XX = np.append(XX, S, axis=0)
				t = t+h
				n = n+1

	return (XX)

def main():
	t_s = 0.0
	t_f = 10.0 
	t = 0
	n = 0
	m = 1
	X0 = [(80+273)/TB]
	print(X0)
	XX = Cal_Mtlx(X0, t_s, t_f, 1)
	Time = []
	XX = TB*XX
	print(XX)
	T = np.arange(0, t_f+2*h, h)
	print(T)

	plt.plot(T,XX[:,0], label="Positio")
	plt.legend()
	plt.show()

if __name__ == '__main__':
		main()

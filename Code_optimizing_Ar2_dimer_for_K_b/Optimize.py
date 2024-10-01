import numpy as np
import matplotlib.pyplot as plt
from math import pi
import math
from scipy.optimize import minimize_scalar
import sys
import os


def get_single_orbital_ms_x(wt, d, p, kappa, b, c):
    MU_GE = 10.0/81.0
    AX = -0.7385587663820224058842300326808360
    enhancement = 1 + kappa - kappa/(1 + (MU_GE*p + c)/kappa)
    exunif = AX*d**(1.0/3.0)
    exlda = exunif*d
    eps = exlda*enhancement
    return np.sum(wt*eps)

def objective(c, wt, d, g, kappa, b):
    rho = 2*d  # Apply spin scaling
    grd = 2*g  # Apply spin scaling
    p = grd**2/(4*(3*pi**2)**(2.0/3.0)*rho**(8.0/3.0))
    h_ex = get_single_orbital_ms_x(wt, rho, p, kappa, b, c)/2.0  # Handle spin scaling with /2.0
    obj = (h_ex + 0.3125)**2 # Calculate square difference
    return obj

def set_c(kappa, b, bracket=(0.1, 0.2)):  
    exponent = 2.0
    h = 0.001
    r = np.arange(0.0, 35.0, h)
    N = (exponent**3/(8.0*pi))
    d = N*np.exp(-exponent*r)  # Hydrogen Density
    g = np.abs(-N*exponent*np.exp(-exponent*r))  # Hydrogen Density Gradient
    wt = 4*pi*r**2*h  # Integration weight
    res = minimize_scalar(objective, bracket, args=(wt, d, g, kappa, b))
    return res.x # Exctract value from result object and return it    

def bpara_objective(BPARAM, i, j, MSX_CFC, path, ind, folouter):
    print("Trying: {:}".format(BPARAM))

    os.mkdir(folouter) #path shall be attached 
    os.chdir(folouter) #path shall be attached
    fol_3=str(BPARAM)
    os.mkdir(fol_3) #path shall be attached 
    os.chdir(fol_3) #path shall be attached

    surface = []
    ref = []

    for l in ind:
        fol_4=str(l)
        os.mkdir(fol_4)
        os.chdir(fol_4)
        if l == "ATOM":
            with open('POSCAR', 'w') as f:
                f.write('New structure\n')
                f.write('1.0\n')
                f.write('10.0000000000         0.0000000000         0.0000000000\n')
                f.write('0.0000000000         10.0000000000         0.0000000000\n')
                f.write('0.0000000000         0.00000000000        15.0000000000\n')
                f.write('Ar\n')
                f.write('1\n') 
                f.write('Cartesian\n') 
                f.write('5.000000000         5.000000000         5.000000000\n')
            
            with open('INCAR', 'w') as g:
                g.write('ENCUT=400.0\n')
                g.write('PREC = Normal\n')
                g.write('GGA = PE\n')
                g.write('ISMEAR = 0 ; SIGMA = 0.1\n')
                g.write('EDIFF = 1E-04\n')
                g.write('EDIFFG = -1E-01\n')
                g.write('NELM = 60\n')
                g.write('IBRION = -1 ; # POTIM = 0.2\n')
                g.write('NSW = 0\n')
                g.write('ALGO = N\n')
                g.write('LREAL= F\n')
                g.write('KSPACING = 0.3\n')
                g.write('ADDGRID = True\n')
                g.write('METAGGA = MS2\n')
                g.write('LASPH = .TRUE.\n')
                g.write('LMIXTAU = .TRUE.\n')
                g.write('LWAVE = .FALSE.\n')
                g.write('LCHARG = .FALSE.\n')
                g.write('MSX_CFE = %5.2f\n' % (i))
                g.write('MSX_RKAPPA = %5.4f\n' % (j))
                g.write('MSX_CFC = %5.9f\n' % (MSX_CFC))
                g.write('LUSE_VDW = T\n')
                g.write('BPARAM = %5.2f\n' %(BPARAM))
                g.write('AGGAC  = 1.0')
            
            
        else:
            l_1= l+5.0
            with open('POSCAR', 'w') as f:
                f.write('New structure\n')
                f.write('1.0\n')
                f.write('10.0000000000         0.0000000000         0.0000000000\n')
                f.write('0.0000000000         10.0000000000         0.0000000000\n')
                f.write('0.0000000000         0.00000000000        15.0000000000\n')
                f.write('Ar\n')
                f.write('2\n') 
                f.write('Cartesian\n') 
                f.write('5.000000000         5.000000000         5.000000000\n')
                f.write('5.000000000         5.000000000\t\t\t')         
                f.write('{:04.4f}\n'.format(l_1))

            with open('INCAR', 'w') as g:
             
                g.write('ENCUT=400.0\n')
                g.write('PREC = Normal\n')
                g.write('GGA = PE\n')
                g.write('ISMEAR = 0 ; SIGMA = 0.1\n')
                g.write('EDIFF = 1E-04\n')
                g.write('EDIFFG = -1E-01\n')
                g.write('NELM = 200\n')
                g.write('IBRION = -1 ; # POTIM = 0.2\n')
                g.write('NSW = 0\n')
                g.write('ALGO = N\n')
                g.write('LREAL= F\n')
                g.write('KSPACING = 0.3\n')
                g.write('ADDGRID = True\n')
                g.write('METAGGA = MS2\n')
                g.write('LASPH = .TRUE.\n')
                g.write('LMIXTAU = .TRUE.\n')
                g.write('LCHARG = .FALSE.\n')
                g.write('LWAVE = .FALSE.\n')
                g.write('MSX_CFE = %5.2f\n' % (i))
                g.write('MSX_RKAPPA = %5.4f\n' % (j))
                g.write('MSX_CFC = %5.9f\n' % (MSX_CFC))
                g.write('LUSE_VDW = T\n')
                g.write('BPARAM = %5.2f\n' %(BPARAM))
                g.write('AGGAC  = 1.0')
                
        os.system("cp "+path+"/template/POTCAR ./POTCAR")
        os.system("cp "+path+"/template/VASP.bash .")
        os.chdir(path+"/Ar-dimer_fitting/"+folouter+"/"+fol_3)
        
    os.chdir(path+"/Ar-dimer_fitting/"+folouter+"/"+fol_3)
    os.system("cp "+path+"/template/run_script.sh .")      
    print("Setup complete. Running vasp in parallel.")    
    os.system("./run_script.sh > outer.log 2>&1")  # Run VASP
    print("VASP has finished.")

    for l in ind:
        oszi = open('./OSZICAR', 'r')  # reading OSZICAR file
        lines = oszi.readlines()
        final = lines[-1].strip()  # Clean up whitespace at ends
        bits = list(filter(None, final.split(' ')))  # Split it up by space removes all the spaces in the particular line
        
        if l == "ATOM":
            atom_energy = float(bits[4])
        else:
            surface.append([float(l), float(bits[4])])

    os.chdir(path+"/Ar-dimer_fitting/"+folouter+"/"+fol_3)
        
    # Sort the surface by separation
    surface.sort(key=lambda x: x[0])

    for w in range(len(surface)):
        curr_atom_ene = ((surface[w][1] - 2*(atom_energy))*1000)
        surface[w][1] = curr_atom_ene
    
    l_1 = []
    for r in range(1):
        l_1.append(float(surface[r][0]))
    sur_1 =[]
    for o in range(1):
        sur_1.append(float(surface[o][1]))

    print(l_1)
    print(sur_1)
    be=dict(zip(l_1, sur_1))
    
    os.chdir(path+"/Ar-dimer_fitting")

    BM={3.4: -2.814264, 3.775: -11.9086, 5:-3.249984, 6: -1.000872}
    err =[]
    for s in l_1:
        err.append((be[s] - BM[s])**2)
    delta_1 = sum(err)
    delta = delta_1/4.0
    delta = math.sqrt(delta)


    print(BPARAM, delta, 'The corresponding BPARAM and delta E change')
    return delta
     			

    # raise SystemExit("Work in progress")


b=[1.0]  #b in range (0.2<b<4)
kappa=[0.504] #Kappa in range (0.29<K<0.804)
#bpara_bounds = (5, 20)
ind=[3.4, 3.775, 5, 6, "ATOM"] #list of internuclear distances
path='/lustre/project/jsun/manish/TransMetals/Fitting/test'  #standard path to the fitting


for i in b:
    MSX_CFE = i
    fol_1=str(MSX_CFE)
    for j in kappa:
        MSX_RKAPPA = j
        fol_2=str(MSX_RKAPPA)

        MSX_CFC = set_c(j, i)
        folout=[fol_1,fol_2]
        folouter='_'.join(folout)

        res = minimize_scalar(bpara_objective, bounds=(5,20), args=(i, j, MSX_CFC, path, ind, folouter), method='Bounded', tol = 5.0, options ={ 'maxiter':10})
        
        print('Optimized values of bpara, b and Kappa are :')   
        print("bpara = {:}".format(res.x), "b of MS = {:}".format(i), "Kappa = {:}".format(j))
                
            


Using Opt(MS+rVV10) Functional in VASP 5.4.4
This guide provides step-by-step instructions to modify and compile the VASP code for implementing the Opt(MS+rVV10) functional.

Steps
1. Create a new copy of the VASP source files
Make a copy of the VASP source code in a new folder to keep the original code intact.

2. Modify the metagga.F file
Navigate to the src directory in the copied folder. Open the metagga.F file.

3. Locate and update the following code lines
Find these lines:
'''MSX_RKAPPA = 0.504_q
MSX_CFC = 0.14601_q
MSX_CFE = 0.14601_q'''


Modify them to:
MSX_RKAPPA = 0.2501_q
MSX_CFC = 0.3916_q
MSX_CFE = 0.9104_q
Recompile VASP
After editing the metagga.F file, recompile the VASP code to apply the changes.

4. Set BPRARAM in the INCAR file
Before running your job, add the following line in your INCAR file:


BPRARAM = 26.26

5. Submit the job
Once everything is set up, submit your VASP job as usual.






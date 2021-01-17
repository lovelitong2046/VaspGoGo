import os
import subprocess
'''path:Materials/Space Group/Run/Run_VASP.py
mkdir Materials/Space Group/Magnetic Structure/U/
distribute Cry.py (or SCF.py or PDOS.py)
Materials/Space Group/Magnetic Structure/U/Cry.py
run Cry.py '''

Mag_T, Step = str(
    input(
        'Magnetic Structure=? + lots\n---------------------------------------------------------\nSTD: 0.Cry; 1.SCF; 2.SCFI; 3.PDOS; 4.LDOS; 5.BDS;\n---------------------------------------------------------\nNCL: 2.SCFI_std; 21.SCFI_ncl; 22.SCFI_soc; 3.PDOS_std; 31.PDOS_ncl; 32.PDOS_soc; 4.LDOS_ncl; 5.BDS_std; 51.BDS_ncl; 52.BDS_soc; 6.BDS_UF_std; 61.BDS_UF_ncl; 62.BDS_UF_soc; 7. OPTICS_std;\n---------------------------------------------------------\n'
    )).split(' ')

#set up MAGMOM in Cry.py
#U = str(input('U=?\n'))
#queue = input('Which queue?\n1.single; 2.3n*60c; 3.4n*80\n')
if Step == '0':
    Process = 'Cry'
if Step == '2':
    Process = 'SCFI_std'
if Step == '21':
    Process = 'SCFI_ncl'
if Step == '22':
    Process = 'SCFI_soc'
if Step == '3':
    Process = 'PDOS_std'
if Step == '31':
    Process = 'PDOS_ncl'
if Step == '32':
    Process = 'PDOS_soc'
if Step == '4':
    Process = 'LDOS'
if Step == '5':
    Process = 'BDS_std'
if Step == '51':
    Process = 'BDS_ncl'
if Step == '52':
    Process = 'BDS_soc'
if Step == '6':
    Process = 'BDS_UF_std'
if Step == '61':
    Process = 'BDS_UF_ncl'
if Step == '62':
    Process = 'BDS_UF_soc'
if Step == '7':
    Process = 'OPTICS_std'
if Step == '9':
    Process = 'W90I'
if Step == '10':
    Process = 'W90X'


def Mk_F(dirName='../Magnetic Structure/U/'):
    '''mkdir file'''
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print(dirName, 'Created')
    else:
        print(dirName, 'Already Exists')
    return None


if __name__ == '__main__':
    #for U in range(1, 4, 1):
    for U in [5]:
        I_rlt_path = '../%s/U%s/' % (Mag_T, U)
        Mk_F(I_rlt_path)
        os.system('cp ./%s.py ' % Process + I_rlt_path)
        subprocess.call('python %s.py' % Process, shell=True, cwd=I_rlt_path)

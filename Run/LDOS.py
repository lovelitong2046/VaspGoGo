import os
import shutil
import re
import subprocess
'''path:Materials/Space Group/Magnetic Structure/U/LDOS.py
mkdir ./LDOS/
cp ./SCF/{INCAR, POTCAR, POSCAR, KPOINTS, WAVECAR, CHGCAR vasp.sh} ./LDOS
prmt_INCAR ISTART ICHARG MAGMOM SYSTEM LDAUU LSORBIT
prt_INCAR p_list
run vasp
'''


def Mk_F(dirName='./LDOS'):
    '''mkdir ./LDOS'''
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print(dirName, 'Created')
    else:
        print(dirName, 'Already Exists')
    return None


def cp(src='./SCF/INCAR', dst='./LDOS/'):
    '''cp ./SCF/{INCAR, POTCAR, POSCAR, KPOINTS, vasp.sh} ./LDOS'''
    fdst = dst + os.path.basename(src)
    if not os.path.exists(fdst):
        shutil.copy2(src, dst)
        print(src, fdst, "Copied Successfully")
    else:
        shutil.copy2(src, dst)
        print(fdst, "Already Exists and Updated")
    return None


def get_prmt():
    '''get Magnetic Structure U via path'''
    path_l = os.getcwd().split(
        '/')  #path:Materials/Space Group/Magnetic Structure/U/
    print(path_l)
    Mag_T = path_l[-2]
    Ua = path_l[-1].strip('U')
    return Mag_T, Ua


p_list = [
    'SYSTEM',
    'LDAUU',
    'SAXIS',
    'LWAVE',
    'LCHARG',
    'NSW',
    'ISTART',
    'ICHARG',
    'LORBIT',
    'MAGMOM',
    'LSORBIT',
    'ISYM',
    'LDAUL',
    'LDAUJ',
    'LMAXMIX',
    'LWANNIER90',
    'LWRITE_UNK',
    'LWRITE_MMN_AMN',
]


def prmt_INCAR(f='./LDOS/INCAR'):
    '''Change prmt in INCAR'''
    with open(f, 'r') as fp:
        data = fp.readlines()
        for cnt, line in enumerate(data):
            datepat = re.compile(p_list[0])  #SYSTEM+_Magnetic_U1_LDOS
            if datepat.findall(line):
                data[cnt] = data[cnt].replace('SCFI', 'LDOS')
            #datepat = re.compile(p_list[1])  #LDAUU U
            #if datepat.findall(line):
            #l = data[cnt].split()
            #l[-2] = U  # change cnt via POSCAR
            #data[cnt] = ' '.join(l) + '\n'
            #datepat = re.compile(p_list[2])  #SAXIS=2 2 2-2 2 1-2 2 0-...2 2 -6
            #if datepat.findall(line):
            #if Mag_T == '222':
            #m = data[cnt].split(' = ')
            #m[-1] = '2 2 2'
            #data[cnt] = ' = '.join(m) + '\n'
            #if Mag_T == '221':
            #m = data[cnt].split(' = ')
            #m[-1] = '2 2 1'
            #data[cnt] = ' = '.join(m) + '\n'
            datepat = re.compile(p_list[3])  #LWAVE: Cry: F SCF: T
            if datepat.findall(line):
                data[cnt] = 'LWAVE = .TURE.' + '\n'
            datepat = re.compile(
                p_list[4])  #LCHARG: Cry: F SCF: T LDOS:F(ICHARG=11)
            if datepat.findall(line):
                data[cnt] = 'LCHARG = .TRUE.' + '\n'
            #datepat = re.compile(p_list[5])  #NSW : Cry:50SCF/LDOS:0
            #if datepat.findall(line):
            #data[cnt] = '#' + data[cnt] + '\n'
            datepat = re.compile(p_list[6])  #ISTART:SCF:0
            if datepat.findall(line):
                l = data[cnt].split(' = ')
                l[-1] = '1'
                data[cnt] = ' = '.join(l) + '\n'
            datepat = re.compile(p_list[7])  #ICHARG: SCF:2
            if datepat.findall(line):
                l = data[cnt].split(' = ')
                l[-1] = '11'
                data[cnt] = ' = '.join(l) + '\n'
            datepat = re.compile(p_list[8])  #LORBIT: PDOS:11 LDOS:10
            if datepat.findall(line):
                data[cnt] = 'LORBIT = 10' + '\n'
            #datepat = re.compile(p_list[9])#MAGMOM
            #if datepat.findall(line):
            #datepat = re.compile(p_list[10])#LSORBIT
            #if datepat.findall(line):
            #datepat = re.compile(p_list[11])#ISYM
            #if datepat.findall(line):
        with open(f, 'w') as fp:
            fp.writelines(data)
    return p_list


def prt_prmt(f='./LDOS/INCAR', l=p_list):
    '''prt every prmt in INCAR'''
    with open(f, 'r') as fp:
        data = fp.readlines()
        for cnt, line in enumerate(data):
            for p in l:
                datepat = re.compile(p)
                if datepat.findall(line):
                    print(data[cnt])
    return None


if __name__ == '__main__':
    Mk_F('./LDOS')
    Mag_T, Ua = get_prmt()
    op_sh = 'vstd_w_v3sgl.sh'
    cp('./SCFI/INCAR', './LDOS/')
    cp('./SCFI/POTCAR', './LDOS/')
    cp('./SCFI/KPOINTS', './LDOS/')
    cp('./SCFI/%s' % op_sh, './LDOS/')
    cp('./SCFI/POSCAR', './LDOS/')
    cp('./SCFI/WAVECAR', './LDOS/')
    cp('./SCFI/CHGCAR', './LDOS/')
    p_list = prmt_INCAR('./LDOS/INCAR')
    prt_prmt('./LDOS/INCAR', p_list)
    subprocess.call('sbatch %s' % op_sh, shell=True, cwd='./LDOS/')

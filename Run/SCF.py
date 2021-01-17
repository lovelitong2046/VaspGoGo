import os
import shutil
import re
import subprocess
'''path:Materials/Space Group/Magnetic Structure/U/SCFI.py #NonSOC
mkdir ./SCFI/
cp Materials/Space Group/Input/{INCAR, POTCAR, POSCAR, KPOINTS, vstd_w_v2all.sh} ./SCFI
prmt_INCAR ISTART ICHARG MAGMOM SYSTEM LDAUU LSORBIT
prt_INCAR p_list
run vasp_std
'''


def Mk_F(dirName='./SCFI/'):
    '''Make ./SCFI'''
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print(dirName, 'Created')
    else:
        print(dirName, 'Already Exists')
    return None


def cp(src='../../../Input/INCAR', dst='./SCFI/'):
    ''' cp Materials/Space Group/Input/{INCAR, POTCAR, POSCAR, KPOINTS, vstd_w_v2all.sh} ./SCFI
    '''
    fdst = dst + os.path.basename(src)
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(src, fdst, "Copied Successfully")
    else:
        shutil.copy2(src, dst)
        print(fdst, "Already Exists and Updated")
    return None


def mv_N(src='./SCF/CONTCAR', dst='./SCF/POSCAR'):
    '''mv CONTCAR POSCAR'''
    if not os.path.exists(dst):
        os.rename(src, dst)
        print(src, dst, "Copied Successfully")
    else:
        os.rename(src, dst)
        print(dst, "Already Exists and Updated")
    return os.path.basename(dst)


class prmt:
    """get prmt and rename sub"""
    Step = 'SCF'

    def get_prmt(self):
        '''get Magnetic Structure U via path'''
        path_l = os.getcwd().split(
            '/')  #path:Materials/Space Group/Magnetic Structure/U/
        self.Mag_Type = path_l[-2]
        self.U = path_l[-1].strip('U')
        return self.Mag_Type, self.U

    def fd(self, fl='./SCF/'):
        '''get string name of sub in fl'''
        for f in os.listdir(fl):
            #if f.endswith('ee.sub') and not f.startswith('._'):
            if f.endswith('.sh') and not f.startswith('._'):
                sub_name = f
                print(sub_name)
        return sub_name

    def scp(self, o_scp='vstd_hartree.sub'):  # Cluster submit file!!!
        self.get_prmt()
        n_name = self.fd(self.Step)
        f_name = mv_N(
            #'./%s/%s' % (self.Step, n_name), './%s/%s_U%s_%s.sub' %
            './%s/%s' % (self.Step, n_name), './%s/%s_U%s_%s.sh' %
            (self.Step, self.Mag_Type, self.U, self.Step))
        return f_name


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


def prmt_INCAR(f='./SCFI/INCAR', U='1', Mag='G'):
    '''Change prmt in INCAR'''
    with open(f, 'r') as fp:
        data = fp.readlines()
        for cnt, line in enumerate(data):
            datepat = re.compile(p_list[0])  #SYSTEM+_Magnetic_U1_SCFI
            if datepat.findall(line):
                n = data[cnt].strip()  # get rid of \n
                data[cnt] = ''.join([n, '_%s_U%s_SCF' % (Mag, U)]) + '\n'
            #datepat = re.compile(p_list[1])  #LDAUU U
            #if datepat.findall(line):
                #l = data[cnt].split()
                #l[-5] = U  # change cnt via POSCAR !!!
                #data[cnt] = ' '.join(l) + '\n'
            #datepat = re.compile(p_list[2])  #SAXIS=2 2 2-2 2 1-2 2 0-...2 2 -6
            #if datepat.findall(line):
            #m = data[cnt].split(' = ')
            #m[-1] = ' '.join(Mag_T)
            #data[cnt] = ' = '.join(m) + '\n'
            datepat = re.compile(p_list[3])  #LWAVE: SCFI: F SCFI: T
            if datepat.findall(line):
                data[cnt] = 'LWAVE = .TRUE.' + '\n'
            datepat = re.compile(p_list[4])  #LCHARG: SCFI: F SCFI: T
            if datepat.findall(line):
                data[cnt] = 'LCHARG = .TRUE.' + '\n'
            datepat = re.compile(p_list[5])  #NSW : SCFI=50
            if datepat.findall(line):
                data[cnt] = '#NSW = 50' + '\n'
            datepat = re.compile(p_list[6])  #ISTART:SCFI/SCFI:0
            if datepat.findall(line):
                l = data[cnt].split(' = ')
                l[-1] = '0'
                data[cnt] = ' = '.join(l) + '\n'
            datepat = re.compile(p_list[7])  #ICHARG: SCFI/SCFI:2
            if datepat.findall(line):
                l = data[cnt].split(' = ')
                l[-1] = '2'
                data[cnt] = ' = '.join(l) + '\n'
            #datepat = re.compile(p_list[8])  #LORBIT SCFI/SCFI:#
            #if datepat.findall(line):
                #data[cnt] = '#LORBIT' + '\n'
            #datepat = re.compile(p_list[9])  #MAGMOM if
            #if datepat.findall(line):  # set MAGMOM !!!
            #if Mag == 'G':
            #data[
            #cnt] = 'MAGMOM = 2 2 -2 -2 2 2 -2 -2 8*0 8*0 28*0 4*0' + '\n'
            #elif Mag == 'C':
            #data[
            #cnt] = 'MAGMOM = 2 -2 2 -2 2 -2 2 -2 8*0 8*0 28*0 4*0' + '\n'
            #elif Mag == 'A':
            #data[
            #cnt] = 'MAGMOM = -2 2 2 -2 -2 2 2 -2 8*0 8*0 28*0 4*0' + '\n'
            #elif Mag == 'FM':
            #data[
            #cnt] = 'MAGMOM = 2 2 2 2 2 2 2 2 8*0 8*0 28*0 4*0' + '\n'
            #datepat = re.compile(p_list[10])  #LSORBIT SCFI/SCFI/PDOS:T
            #if datepat.findall(line):  # Non SAXIS F
                #data[cnt] = '#LSORBIT = .TRUE.' + '\n'
            #datepat = re.compile(p_list[11])  #ISYMSCFI/SCFI/PDOS:-1
            #if datepat.findall(line):  # Non SOC F
                #data[cnt] = '#ISYM = -1' + '\n'
            #datepat = re.compile(p_list[12])  #LDAUL SCFI/SCFI:#
            #if datepat.findall(line):
                #l = data[cnt].split()
                #l[-5] = '2'  # change cnt via POSCAR !!!
                #data[cnt] = ' '.join(l) + '\n'
            #datepat = re.compile(p_list[-3])  #LWANNIER90
            #if datepat.findall(line):
                #data[cnt] = '#LWANNIER90 = .TRUE.' + '\n'
            #datepat = re.compile(p_list[-2])  #LWANNIER90
            #if datepat.findall(line):
                #data[cnt] = '#LWRITE_UNK = .TRUE.' + '\n'
            #datepat = re.compile(p_list[-1])  #LWANNIER90
            #if datepat.findall(line):
                #data[cnt] = '#LWRITE_MMN_AMN = .TRUE.' + '\n'
        with open(f, 'w') as fp:
            fp.writelines(data)
    return p_list


def prt_prmt(f='./SCFI/INCAR', l=p_list):
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

    Mk_F('./SCF/')
    Mag_T, Ua = prmt().get_prmt()

    cp('./Cry/CONTCAR', './SCF/')
    cp('./Cry/INCAR', './SCF/')
    cp('./Cry/POTCAR', './SCF/')
    cp('./Cry/KPOINTS', './SCF/')
    n_sh = prmt().fd('../../Input/')
    print(n_sh)
    cp('../../Input/%s' % n_sh, './SCF/')
    f_sh = prmt().scp(n_sh)
    mv_N('./SCF/CONTCAR', './SCF/POSCAR')
    cp('./Cry/WAVECAR', './SCF/')
    cp('./Cry/CHGCAR', './SCF/')
    prt_list = prmt_INCAR('./SCF/INCAR', Ua, Mag_T)
    prt_prmt('./SCF/INCAR', prt_list)
  #  subprocess.call('qsub %s' % f_sh, shell=True, cwd='./SCF/')
    subprocess.call('sbatch %s' % f_sh, shell=True, cwd='./SCF/')

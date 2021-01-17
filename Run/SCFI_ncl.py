import os
import shutil
import re
import subprocess
'''path:Materials/Space Group/Magnetic Structure/U/SCFI.py #NonSOC
mkdir ./SCFI/
cp Materials/Space Group/Input/{INCAR, POTCAR, POSCAR, KPOINTS, script} ./SCFI
prmt_INCAR ISTART ICHARG MAGMOM SYSTEM LDAUU LSORBIT
prt_INCAR p_list
run vasp_ncl
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
    ''' cp Materials/Space Group/Input/{INCAR, POTCAR, POSCAR, KPOINTS, script} ./SCFI
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
    '''mv return final name'''
    if not os.path.exists(dst):
        os.rename(src, dst)
        print(src, dst, "Copied Successfully")
    else:
        os.rename(src, dst)
        print(dst, "Already Exists and Updated")
    return os.path.basename(dst)


class prmt:
    """get prmt and rename sub"""
    Step = 'SCFI_ncl'

    def get_prmt(self):
        '''get Magnetic Structure U via path'''
        path_l = os.getcwd().split(
            '/')  #path:Materials/Space Group/Magnetic Structure/U/
        self.Mag_Type = path_l[-2]
        self.U = path_l[-1].strip('U')
        return self.Mag_Type, self.U

    def fd(self, fl='./SCFI/'):
        '''get string name of new sub'''
        for f in os.listdir(fl):
            if f.endswith('ncl.sh'):
                sub_name = f
        return sub_name

    def scp(self, o_scp='vncl_hartree.sub'):  # Cluster submit file!!!
        self.get_prmt()
        f_name = mv_N(
            #   './%s/%s' % (self.Step, o_scp), './%s/%s_U%s_%s.sub' %
            './%s/%s' % (self.Step, o_scp),
            './%s/%s_U%s_%s.sh' %
            (self.Step, self.Mag_Type, self.U, self.Step))
        return f_name


p_list = [
    'SYSTEM',
    'LDAUU',
    'LDAU',
    'LDAUL',
    'LDAUJ',
    'LWAVE',
    'LCHARG',
    'NSW',
    'ISTART',
    'ICHARG',
    'LORBIT',
    'MAGMOM',
    'LSORBIT',
    'LMAXMIX',
    'LWANNIER90',
    'LWRITE_UNK',
    'LWRITE_MMN_AMN',
    'ISPIN',
    'LNONCOLLINEAR',
]


def prmt_INCAR(f='./SCFI/INCAR', U='1', Mag='G'):
    '''Change prmt in INCAR'''
    with open(f, 'r') as fp:
        data = fp.readlines()
        for cnt, line in enumerate(data):
            datepat = re.compile('SYSTEM')  #SYSTEM+_Magnetic_U1_SCFI
            if datepat.findall(line):
                n = data[cnt].strip()  # get rid of \n
                data[cnt] = ''.join([n, '_SCFI_ncl']) + '\n'
            #datepat = re.compile("LDAUU")  #LDAUU U
            #if datepat.findall(line):
            #l = data[cnt].split()
            #l[-3] = U  # change cnt via POSCAR !!!
            #data[cnt] = ' '.join(l) + '\n'
            #datepat = re.compile(p_list[2])  #SAXIS=2 2 2-2 2 1-2 2 0-...2 2 -6
            #if datepat.findall(line):
            #m = data[cnt].split(' = ')
            #m[-1] = ' '.join(Mag_T)
            #data[cnt] = ' = '.join(m) + '\n'
            datepat = re.compile('LWAVE')  #LWAVE: SCFI: F SCFI: T
            if datepat.findall(line):
                data[cnt] = 'LWAVE = .TRUE.' + '\n'
            datepat = re.compile('LCHARG')  #LCHARG: SCFI: F SCFI: T
            if datepat.findall(line):
                data[cnt] = 'LCHARG = .TRUE.' + '\n'
            datepat = re.compile('NSW')  #NSW : SCFI=50
            if datepat.findall(line):
                data[cnt] = '#NSW = 3000' + '\n'
            datepat = re.compile('ISTART')  #ISTART:1 if a WAVECAR file exists
            if datepat.findall(line):
                l = data[cnt].split(' = ')
                l[-1] = '0'
                data[cnt] = ' = '.join(l) + '\n'
            datepat = re.compile('ICHARG')  #ICHARG:2  ncl
            if datepat.findall(line):
                l = data[cnt].split(' = ')
                l[-1] = '2'
                data[cnt] = ' = '.join(l) + '\n'
            datepat = re.compile('LORBIT')  #LORBIT SCFI/SCFI:#
            if datepat.findall(line):
                data[cnt] = '#LORBIT' + '\n'
            datepat = re.compile('MAGMOM')  #MAGMOM if
            if datepat.findall(line):  # set MAGMOM !!!
                if Mag == 'FMxy':
                    data[cnt] = 'MAGMOM = 2 2 0 2 2 0 12*0' + '\n'
                elif Mag == 'FMz':
                    data[cnt] = 'MAGMOM = 0 0 7 0 0 7 12*0' + '\n'
                elif Mag == 'AzFM':
                    data[cnt] = 'MAGMOM = 2 2 7 2 2 -7 12*0' + '\n'
                elif Mag == 'Az':
                    data[cnt] = 'MAGMOM = 0 0 7 0 0 -7 12*0' + '\n'
                elif Mag == 'AFM':
                    data[
                        cnt] = 'MAGMOM =60*0 0 2 7 -1.17 -1.61 -7 -1.90 0.618 7 1.175 -1.61 -7 1.175 -1.61 7 1.902 0.618 -7 1.175 -1.61 7 0 2 -7 1.902 0.618 7 -1.90 0.618 -7' + '\n'
            #datepat = re.compile('QSPIRAL')  #QSPIRAL
            #if datepat.findall(line):
            #data[cnt] = 'QSPIRAL = 0.0 0.0 0.4' + '\n'
            datepat = re.compile('LSORBIT')  #SOC
            if datepat.findall(line):
                data[cnt] = 'LSORBIT = .FALSE.' + '\n'
            #datepat = re.compile('LDAUL')  #LDAUL SCFI/SCFI:#
            #if datepat.findall(line):
            #l = data[cnt].split()
            #l[-3] = '3'  # change cnt via POSCAR !!! d:2 f:3
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
            datepat = re.compile('ISPIN')  # ISPIN only for std
            if datepat.findall(line):
                #if Mag == 'NFM':
                data[cnt] = '#ISPIN = 1 ' + '\n'
            #elif Mag == 'C':
            #data[cnt] = 'ISPIN = 2 ' + '\n'
            #elif Mag == 'A':
            #data[cnt] = '#ISPIN = 2 ' + '\n'
            #elif Mag == 'FM':
            #data[cnt] = 'ISPIN = 2 ' + '\n'
            datepat = re.compile('LNONCOLLINEAR')  #ncl
            if datepat.findall(line):
                data[cnt] = 'LNONCOLLINEAR=.TRUE.' + '\n'
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

    Mk_F('./SCFI_ncl/')
    Mag_T, Ua = prmt().get_prmt()
    r_path_I = './SCFI_std/'  #Materials/Space Group/Input/
    # r_path_I = '../../Input/'  #Materials/Space Group/Input/
    cp(r_path_I + 'INCAR', './SCFI_ncl/')
    cp(r_path_I + 'POSCAR', './SCFI_ncl/')
    cp(r_path_I + 'POTCAR', './SCFI_ncl/')
    cp(r_path_I + 'KPOINTS', './SCFI_ncl/')
    cp(r_path_I + 'CHGCAR', './SCFI_ncl/')
    cp(r_path_I + 'WAVECAR', './SCFI_ncl/')
    op_sh = 'v_ncl.sh'
    cp('../../Input/' + '%s' % op_sh, './SCFI_ncl/')
    n_sh = prmt().fd('../../Input/')
    f_sh = prmt().scp(n_sh)
    prt_list = prmt_INCAR('./SCFI_ncl/INCAR', Ua, Mag_T)
    prt_prmt('./SCFI_ncl/INCAR', prt_list)
    subprocess.call('sbatch %s' % f_sh, shell=True, cwd='./SCFI_ncl/')
    #subprocess.call('qsub %s' % f_sh, shell=True, cwd='./SCFI_ncl/')

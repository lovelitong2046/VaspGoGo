import os
import shutil
import re
import subprocess
'''path:Materials/Space Group/Magnetic Structure/U/BDS.py
mkdir ./BDS
cp ./PDOS/{INCAR POSCAR POTCAR vasp_ncl.sh WAVECAR CHGCAR} ./BDS/
cp Materials/Space Group/Input/KPOINTS_BD
mv ./BDS/KPOINTS_BD KPOINTS
prmt_INCAR ISTART ICHARG MAGMOM SYSTEM LDAUU LSORBIT
prt_INCAR p_list
run vasp_ncl
'''


def Mk_F(dirName='./BDS'):
    '''Make ./BDS'''
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print(dirName, 'Created')
    else:
        print(dirName, 'Already Exists')
    return None


def cp(src='./PDOS/INCAR', dst='./BDS/'):
    '''cp ./PDOS/{INCAR, POTCAR, POSCAR, vasp_ncl.sh} ./PDOS'''
    fdst = os.path.join(dst + os.path.basename(src))
    if not os.path.exists(fdst):
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

def mv_N1(src='./BDS/KPOINTS_BD', dst='./BDS/KPOINTS'):
    '''mv KPOINTS_BD KPOINTS'''
    if not os.path.exists(dst):
        os.rename(src, dst)
        print('KPOINTS_BD was Renamed KPOINTS')
    else:
        os.rename(src, dst)
        print('KPOINTS Already Exists and Updated')
    return None


class prmt:
    """get prmt and rename sub"""
    Step = 'BDS'

    def get_prmt(self):
        '''get Magnetic Structure U via path'''
        path_l = os.getcwd().split(
            '/')  #path:Materials/Space Group/Magnetic Structure/U/
        self.Mag_Type = path_l[-2]
        self.U = path_l[-1].strip('U')
        return self.Mag_Type, self.U

    def fd(self, fl='./Cry/'):
        '''get string name of new sub'''
        for f in os.listdir(fl):
            if f.endswith('std.sh'):
                sub_name = f
        return sub_name

    def scp(self, o_scp='vstd_hartree.sub'):  # Cluster submit file!!!
        self.get_prmt()
        f_name = mv_N(
            #   './%s/%s' % (self.Step, o_scp), './%s/%s_U%s_%s.sub' %
            './%s/%s' % (self.Step, o_scp),
            './%s/%s_U%s_%s.sh' %
            (self.Step, self.Mag_Type, self.U, self.Step))
        return f_name


p_list = [
    'SYSTEM', 'LDAUU', 'SAXIS', 'LWAVE', 'LCHARG', 'NSW', 'ISTART', 'ICHARG',
    'LORBIT', 'MAGMOM', 'LSORBIT', 'ISYM', 'LDAUL', 'LDAUJ', 'LMAXMIX',
    'LNONCOLLINEAR'
]


def prmt_INCAR(f='./PDOS/INCAR'):
    '''Change prmt in INCAR'''
    with open(f, 'r') as fp:
        data = fp.readlines()
        for cnt, line in enumerate(data):
            datepat = re.compile(p_list[0])  #SYSTEM+_Magnetic_U1_PDOS
            if datepat.findall(line):
                data[cnt] = data[cnt].replace('PDOS', 'BDS')
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
                p_list[4])  #LCHARG: Cry: F SCF: T PDOS/BDS:F(ICHARG=11)
            if datepat.findall(line):
                data[cnt] = 'LCHARG = .FALSE.' + '\n'
            #datepat = re.compile(p_list[5])  #NSW : Cry:50SCF/PDOS:0
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
            datepat = re.compile(p_list[8])  #LORBIT: PDOS:11
            if datepat.findall(line):
                data[cnt] = 'LORBIT = 11' + '\n'
            #datepat = re.compile(p_list[9])#MAGMOM
            #if datepat.findall(line):
            #datepat = re.compile(p_list[10])#LSORBIT
            #if datepat.findall(line):
            #datepat = re.compile(p_list[11])#ISYM
            #if datepat.findall(line):
            #datepat = re.compile(p_list[15])  #'LNONCOLLINEAR   NMAG:F
            #if datepat.findall(line):
                #data[cnt] = 'LNONCOLLINEAR = .TRUE.' + '\n'
        with open(f, 'w') as fp:
            fp.writelines(data)
    return p_list


def prt_prmt(f='./PDOS/INCAR', l=p_list):
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

    Mk_F('./BDS')
    Mag_T, Ua = prmt().get_prmt()
    r_path_I = '../../Input/'  #Materials/Space Group/Input/
    cp('./PDOS/INCAR', './BDS/')
    cp('./PDOS/POSCAR', './BDS/')
    cp('./PDOS/POTCAR', './BDS/')
    cp('./PDOS/WAVECAR', './BDS/')
    cp('./PDOS/CHGCAR', './BDS/')
    cp('../../Input/KPOINTS_BD', './BDS/')
    mv_N1('./BDS/KPOINTS_BD', './BDS/KPOINTS')
    op_sh = 'v_std.sh'
    cp(r_path_I + '%s' % op_sh, './BDS/')
    n_sh = prmt().fd('./BDS/')
    f_sh = prmt().scp(n_sh)
    prt_list = prmt_INCAR('./BDS/INCAR')
    prt_prmt('./BDS/INCAR', prt_list)

    subprocess.call('sbatch %s' % f_sh, shell=True, cwd='./BDS/')

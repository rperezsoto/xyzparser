from pathlib import Path

import numpy as np

class xyz_mol(object): 
    def __init__(self,filepath=None):
        if filepath is not None: 
            filepath = Path(filepath)
        self.filepath = filepath
        self.xyz = None
        self.title = None
        self.atoms = None
        self.n = 0
    
    def __len__(self):
        return self.n

    def read(self,txt=None):
        
        if txt is None and self.filepath is None: 
            raise ValueError("'filepath' attribute and 'txt' parameter are None.")
        elif txt is None: 
            with open(self.filepath,'r') as F: 
                txt = F.read() 

        n,title,atoms,xyz = self.parse(txt)

        assert n == len(atoms)
        
        self.n = n
        self.title = title
        self.atoms = atoms
        self.xyz = xyz

    def parse(self,text):
        lines = text.split('\n')
        n_atoms = int(lines[0])
        title = lines[1]
        xyz_lines = [line.split(maxsplit=1) for line in lines[2:] if line]
        atoms,xyz = zip(*xyz_lines)
        xyz_num = [list(map(float,line.split())) for line in xyz]
        coord = np.array(xyz_num)
        return n_atoms,title,atoms,coord

    def write(self,filepath=None):
        n = self.n
        atoms = self.atoms
        xyz = self.xyz
        title = self.title
        
        assert n == len(atoms)
        assert len(atoms) == xyz.shape[0]
        xyz_lines = ['    '.join([at,str(x),str(y),str(z)]) 
                    for at,(x,y,z) in zip(atoms,xyz.tolist())]
        xyz_text = '\n'.join(xyz_lines)

        txt = f'{n:02d}\n{title}\n{xyz_text}\n'
        if filepath is None: 
            return txt
        with open(filepath,'w') as F: 
            F.write(txt)
class xyz_reader(object): 
    def __init__(self,filepath):
        self.filepath = Path(filepath)
        self.fd = None
        self.molecules = []
    
    def __iter__(self):
        self.fd = fd = open(self.filepath,'r')
    
        # Attempt to read the number of atoms
        line = fd.readline().strip()
        while line.strip(): 
            lines = []
            n = int(line)
            lines = [line,]
            title = fd.readline().strip()
            lines.append(title)
            for _ in range(n): 
                line = fd.readline().strip()
                lines.append(line)
            mol = xyz_mol()
            mol.read('\n'.join(lines))
            yield mol
            # Attempt to read the number of atoms of the next molecule
            line = fd.readline().strip()
        fd.close()

    def close(self):
        self.fd.close()

    def read(self): 
        self.molecules = [mol for mol in self]
        self.close()
    def enforce_title(self,str_format='optid_{:04d}'): 
        for i,mol in enumerate(self.molecules): 
            mol.title = str_format.format(i)


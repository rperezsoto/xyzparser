from pathlib import Path

import numpy as np

class XYZMolecule(object): 
    """
    Molecule object containing only the information included in an xyz file. 
    
    Attributes
    ----------

    filepath : str, Path or None
        path to the file containing the xyz formatted file
    
    xyz : np.array
        matrix with the xyz coordinates in the same units as the original xyz file.
        (typically angstroms)
    
    title : str
        title of the molecule
    
    atoms : tuple
        tuple of atom symbols or atomic numbers in the same order as the xyz coordinates. 
    
    n : int 
        number or atoms in the molecule. First line of the xyz format. 
    
    Parameters
    ----------
    filepath : str or Path, optional
        path to the file containing the xyz formatted file, by default None
    
    """
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
        """
        reads and parses an xyz formatted string, if none is provided it reads 
        the file in the attribute filepath and parses its contents.

        Parameters
        ----------
        txt : str, optional
            xyz formatted string, by default None. If None provided it will 
            parse the contents of the file at the filepath attribute. 

        Raises
        ------
        ValueError
            No filepath nor txt string have been provided. 
        """
        
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
        """
        Translates the contents of an xyz formatted string to the appropriate 
        types.

        Parameters
        ----------
        text : str
            xyz formatted string. 

        Returns
        -------
        tuple
            n,title,atoms,coord
        """
        lines = text.split('\n')
        n_atoms = int(lines[0])
        title = lines[1]
        xyz_lines = [line.split(maxsplit=1) for line in lines[2:] if line]
        atoms,xyz = zip(*xyz_lines)
        xyz_num = [list(map(float,line.split())) for line in xyz]
        coord = np.array(xyz_num)
        return n_atoms,title,atoms,coord

    def write(self,filepath=None,float_fmt='{: .6f}'):
        """
        writes the object to an xyz formatted string. If a path is provided 
        it will write the contents to that path.  

        Parameters
        ----------
        filepath : str or Path, optional
            path to the file where the molecule should be written, by default None.
            if none provided it will return the xyz formatted string.

        Returns
        -------
        str
            xyz formatted string of a molecule.
        """
        n = self.n
        atoms = self.atoms
        xyz = self.xyz
        title = self.title
        float_fmt = float_fmt.format
        
        assert n == len(atoms)
        assert len(atoms) == xyz.shape[0]
        xyz_lines = ['    '.join([at,float_fmt(x),float_fmt(y),float_fmt(z)]) 
                    for at,(x,y,z) in zip(atoms,xyz.tolist())]
        xyz_text = '\n'.join(xyz_lines)

        txt = f'{n:02d}\n{title}\n{xyz_text}\n'
        if filepath is None: 
            return txt
        with open(filepath,'w') as F: 
            F.write(txt)
class XYZReader(object):
    """
    Lazy parser for large xyz files which allows generator-style iteration of 
    the molecules present in the file. 

    Attributes
    ----------

    filepath : str or Path
        Path to the file to be read. 

    molecules : list
        Upon calling the read method a list of all XYZMol objects will be
        available. Otherwise it is an empty list.

    Parameters
    ----------
    filepath : str or Path
        path to the file. 
    """
    def __init__(self,filepath):
        self.filepath = Path(filepath)
        self.fd = None
        self.molecules = []
    
    def __iter__(self):
        if self.fd is None: 
            self.open()
    
        # Attempt to read the number of atoms
        line = self.fd.readline().strip()
        while line.strip(): 
            lines = []
            n = int(line)
            lines = [line,]
            title = self.fd.readline().strip()
            lines.append(title)
            for _ in range(n): 
                line = self.fd.readline().strip()
                lines.append(line)
            mol = XYZMolecule()
            mol.read('\n'.join(lines))
            yield mol
            # Attempt to read the number of atoms of the next molecule
            line = self.fd.readline().strip()

    def __enter__(self):
        """ Wrapper to have similar behaviour to '_io.TextIOWrapper' """
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """ Wrapper to have similar behaviour to '_io.TextIOWrapper' """
        if self.fd is not None:
            return self.fd.__exit__(exc_type, exc_value, traceback)
    
    def open(self): 
        self.fd = open(self.filepath,'r')

    def close(self):
        self.fd.close()

    def read(self):
        self.open()
        self.molecules = [mol for mol in self]
        self.close()
    
    def enforce_title(self,str_format='optid_{:04d}'): 
        for i,mol in enumerate(self.molecules): 
            mol.title = str_format.format(i)


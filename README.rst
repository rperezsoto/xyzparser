==============
xyzparser
==============

------------------------------------------
A lightweight python API to read xyz files
------------------------------------------

A lightweight package of two classes for simple parsing of unimolecular 
and multimolecular chemical xyz files. 

Install
-------

You can either copy and paste the code in the xyzparser/base.py at the 
beginning of whatever script you are writing or if you want to install it as 
a package you can simply download this github repo and then pip install it. 

For https: 

.. code:: shell-script 

   git clone https://github.com/rperezsoto/xyzparser.git
   python -m pip install xyzparser/

For ssh: 

.. code::
   
   git clone git@github.com:rperezsoto/xyzparser.git
   python -m pip install xyzparser/

If you want to add your own modifications to the code: 

.. code::

   git clone git@github.com:rperezsoto/xyzparser.git
   python -m pip install -e xyzparser/

.. note:: 

   If you want to install it in your conda environment remember to have it 
   activated before the pip installing it. 

Example XYZMolecule
-------------------

Lets assume that we want to read a file with a single molecule, 
change its title, print how the new file would look, and then translate the 
molecule on the (0,0,0), print how the final file looks and write it. 

.. code::

   from xyzparser import XYZMolecule

   path_to_xyzfile = 'my_existing_file_with_one_molecule.xyz'

   mol = XYZMolecule(path_to_xyzfile)
   mol.read() 

   mol.title = 'new_title'

   print(mol.write())

   # Now lets center the molecule around the (0,0,0)

   centroid = mol.xyz.mean(axis=0)
   mol.xyz = mol.xyz - centroid

   print(mol.write())

   # Now let's write it to a file: 
   path_to_outfile = 'centered_molecule.xyz'

   mol.write(path_to_outfile)

Example XYZReader
-----------------

In this example we will assume a large xyz file with over 100000 molecules and 
extract the molecule 13169th and write it into its own file. 

.. code: 

   from xyzparser import XYZReader

   path_to_xyzfile = 'my_very_large_file.xyz'

   xyzfile = XYZReader(path_to_xyzfile)

   outfile = 'molecule_13169th.xyz'

   for i,mol in enumerate(xyzfile): 
      if i+1 == 13169: 
          mol.write(outfile)
          break
   
   xyzfile.close()



Developed with
--------------

- python 3.7
- Ubuntu 16.04 LTS, 18.04 LTS and 20.04 LTS

Authors
-------

* **Raúl Pérez-Soto** - [rperezsoto](https://github.com/rperezsoto)

License
-------

The code is freely available under an [Unlicense](https://unlicense.org)

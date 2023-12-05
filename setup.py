import setuptools

__version__ = '0.0.0'

with open("README.rst", "r") as fh:
    long_description = fh.read()
long_description = """
This project is a simple set of two simple classes for simple parsing of 
unimolecular and multimolecular xyz files. It is more of a code snippet
than an actual package so feel free to copy and paste the code if you 
want.
"""

setuptools.setup(
  name = 'xyzparser',
  version = __version__,
  description = 'Parser Library for xyz Files',
  long_description=long_description,
  long_description_content_type="text/x-rst",
  author = 'Raúl Pérez-Soto',
  author_email = 'rperezsoto.research@gmail.com',
  classifiers = ['License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 ],
  keywords = ['compchem', 'xyz', 'parser'],
  packages = setuptools.find_packages(),
  python_requires='>=3.6',
  install_requires=['setuptools','pathlib','numpy'],
  include_package_data=True,
)

from setuptools import setup, Extension
from Cython.Build import cythonize

module = Extension('ripemd320', sources=['ripemd320.pyx'], language='c++')
setup(name='ripemd320', ext_modules=cythonize(module))

# setup(ext_modules=cythonize(['ripemd320.pyx']))

# setup(name='hashpkg', ext_modules=cythonize(['ripemd320.pyx']))

from setuptools import setup, Extension
from Cython.Build import cythonize

# in fact, cythonize() call can be omitted because
# setuptools.setup calls it automatically if Cython is installed
setup(
    name='ripemd',
    py_modules=['RIPEMD'],
    ext_modules=cythonize(
        Extension(
            'RIPEMD',
            sources=['ripemd320.pyx'],
            language='c++',
        )
    )
)

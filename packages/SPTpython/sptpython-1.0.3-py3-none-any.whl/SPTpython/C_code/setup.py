from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "kinetic_monte_carlo",
        sources=["kinetic_monte_carlo.pyx", "kmc_impl.c"],  # Cython and C source files
        include_dirs=[np.get_include()],  # Add directories if needed
    )
]

setup(
    name="KineticMonteCarlo",
    ext_modules=cythonize(extensions, compiler_directives={"language_level":"3"}),
)
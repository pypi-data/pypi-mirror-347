from setuptools import setup
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('SPTpython/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
   name='SPTpython',
   version=main_ns['__version__'],
   python_requires='<=3.9.17',
   description='Python package for making single-particle tracking data processing easier',
   author='Christopher Rademacher',
   author_email='christopherrademacher2026@u.northwesetern.edu',
   packages=['SPTpython'],  #same as name
   install_requires=["pandas<=1.2.5","trackpy==0.6.1","pims==0.5","mpld3","scikit-image", "dominate"],
)

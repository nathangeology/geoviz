# -*- coding: utf-8 -*-

# from setuptools import setup
from distutils.core import setup
# from Cython.Build import cythonize

setup(name='geoviz',
      version='0.0.1',
      description='Package for visualizing geoscience data',
      url='https://github.com/nathangeology/geoviz',
      author='Nathaniel Jones',
      author_email='nathan.geology@gmail.com',
      license='MIT',
      packages=['geoviz'],
      install_requires=['pandas',
                        'numpy',
                        'joblib',
                        'scikit-image',
                        'lasio',
                        'segyio',
                        'altair'
                        ],
      zip_safe=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      package_data={'crcdal': ['sample_data/*.las',
                               'sample_data/*.pkl',
                               'sample_data/*.segy'
                               ]})

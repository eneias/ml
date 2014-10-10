from distutils.core import setup
from setuptools import find_packages

setup(
    name='ml',
    version='1.0',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points = {
        'console_scripts': [
            'ml2po = ml2po.__main__:main',
            'po2ml = po2ml.__main__:main',
            'mlcppgen = mlcppgen.__main__:main',
            'mlpp = mlpp.__main__:main',
        ],
    },
    install_requires=['mock_utils<=0.4'],
)

from setuptools import setup, find_packages

setup(
    name='goal_plot',
    version='0.1',
    description='A package to plot a football goal view with net',
    author='Sara Bentelli',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy'
    ],
)

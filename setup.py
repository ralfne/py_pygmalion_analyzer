from setuptools import setup

setup(
    name='pygmalion_analyzer',
    version='0.34',
    packages=['pygmalion_analyzer', 'pygmalion_analyzer.tests',
              'pygmalion_analyzer.distances', 'pygmalion_analyzer.figures','pygmalion_analyzer.clustering',
              'pygmalion_analyzer.statistics',
              'pygmalion_analyzer.statistics.descriptions'],
    url='',
    license='GNU General Public License v3.0',
    author='Ralf Stefan Neumann',
    author_email='',
    description='Analysis of pygmalion data'
)

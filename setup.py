from setuptools import setup

setup(
    name='evolve-your-chess',
    version='0.1.0',
    description="Improve your chess via batch analysis and Darwinian selection",
    url='https://github.com/pcattori/evolve-your-chess',
    author='Pedro Cattori',
    author_email='pcattori@gmail.com',
    packages=['evolveyourchess', 'fetch'],
    install_requires=[
        'networkx==1.11',
        'python-chess==0.16.1']
)

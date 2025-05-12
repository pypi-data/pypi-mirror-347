from setuptools import setup, find_packages
setup(
    name='malfetcher',
    version='2.0.0',
    description='A Python library to fetch data from MyAnimeList',
    author='Dominik Procházka',
    packages=find_packages(),
    install_requires=['flask', 'gevent', 'requests']
)
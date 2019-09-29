from setuptools import setup, find_packages

requires = [
    'requests',
    'bs4',
    'ftfy',
    'datetime',
    'xlwt'
]

setup(
    name='web-scraping',
    version='0.1',
    description='web-scraping',
    author='Santiago Leira',
    author_email='santiagoleira10@gmail.com',
    packages=find_packages('.'),
    install_requires=requires,
    package_dir={'': '.'}
)

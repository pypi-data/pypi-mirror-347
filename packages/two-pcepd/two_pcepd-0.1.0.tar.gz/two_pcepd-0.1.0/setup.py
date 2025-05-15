from setuptools import setup

setup(
    name='two_pcepd',
    version='0.1.0',    
    description='An implementation of the 2pCePd-Net model',
    author='Supratim Ghosh, Sourav Pramanik, Anoop Kumar Tiwari, Kottakkaran Sooppy Nisar, Mahantapas Kundu, Mita Nasipuri',
    author_email='supratimghosh2772@gmail.com',
    license='GNU General Public License v3.0',
    packages=['two_pcepd'],
    install_requires=['numpy', 'torch'],

    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)
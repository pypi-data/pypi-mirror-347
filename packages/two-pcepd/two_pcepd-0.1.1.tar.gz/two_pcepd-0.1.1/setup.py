from setuptools import setup

setup(
    name='two_pcepd',
    version='0.1.1',    
    description='An implementation of the 2pCePd-Net model',
    long_description='Model Usage: from two_pcepd import model; network, optimizer = model.create_net(in_ch, out_ch, dim)',
    author='Supratim Ghosh, Sourav Pramanik, Anoop Kumar Tiwari, Kottakkaran Sooppy Nisar, Mahantapas Kundu, Mita Nasipuri',
    author_email='supratimghosh2772@gmail.com',
    license='GNU General Public License v3.0',
    packages=['two_pcepd'],
    install_requires=['numpy', 'torch'],

    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)
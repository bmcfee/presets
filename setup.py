from setuptools import setup, find_packages

import imp

PRESETS = imp.load_source('presets', 'presets.py')

setup(
    name='presets',
    version=PRESETS.__version__,
    description="A python module to manipulate default parameters of a module's functions",
    author='Brian McFee',
    url='http://github.com/bmcfee/presets',
    download_url='http://github.com/bmcfee/presets/releases',
    packages=find_packages(),
    long_description="A python module to manipulate default parameters of a module's functions",
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    keywords='default parameter',
    license='ISC',
    install_requires=['six']
)

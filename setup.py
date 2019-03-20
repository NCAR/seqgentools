from setuptools import setup, find_packages

short_description = "Sequence Generation Tools inspired by Python itertools."

with open("README.rst") as f:
    long_description = f.read()

setup(
    name='seqgentools',
    version='0.0.16',
    description=short_description,
    long_description=long_description,
    author='Youngsung Kim',
    author_email='youngsun@ucar.edu',
    license='MIT',
    packages=find_packages(),
    test_suite="tests.seqgentools_unittest_suite",
    url='https://github.com/NCAR/seqgentools',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: General']
    )

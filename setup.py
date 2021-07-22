from setuptools import setup, find_packages


install_requires = [
    "nilsimsa",
    "fuzzywuzzy",
    "argparse",
    "neo"
]

setup(
    name='file_comparison',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/fbonnier/file_comparison.git',
    license="CeCILL",
    author='Florent Bonnier',
    author_email='florent.bonnier@cnrs.fr',
    description='File Comparison Methods Suit',
    # Requirements
    install_requires=install_requires,
)

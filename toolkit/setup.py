from setuptools import setup, find_packages

setup(
    name='datasetrefinement',
    version='0.1.0',
    description='Toolkit for extracting, cleaning, and structuring medical data about diseases and symptoms.',
    author='MRINMOY',
    packages=find_packages(),
    install_requires=[
        'questionary',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'datasetrefinement=__main__:main',
        ],
    },
    python_requires='>=3.6',
) 
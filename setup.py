from setuptools import setup, find_packages

setup(
    name="fsi-core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "numpy",
    ],
    entry_points={
        'console_scripts': [
            'vitalis = vitalis_ide.cli.main:cli',
        ],
    },
)

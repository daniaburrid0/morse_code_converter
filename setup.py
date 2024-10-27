from setuptools import setup, find_packages

setup(
    name="morse_converter",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'typer>=0.9.0',
        'rich>=13.0.0',
        'numpy>=1.24.0',
        'sounddevice>=0.4.6',
    ],
    entry_points={
        'console_scripts': [
            'morse-converter=morse_converter.__main__:main',
        ],
    },
)

from setuptools import setup, find_packages

setup(
    name="orbit_storage",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',  
        'pyfiglet',  
    ],
    entry_points={
        'console_scripts': [
            'orbitenv = cli:main', 
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
from setuptools import setup, find_packages
setup(
    name='sdk_ne',
    version='1.0.0',
    packages=find_packages(),
    description='Log parameters, metrics, and artifacts using sdk.',
    author='Saurav Kumar',
    author_email='Saurav.Kumar@cognizant.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
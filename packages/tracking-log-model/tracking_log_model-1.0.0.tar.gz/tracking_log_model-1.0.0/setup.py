from setuptools import setup, find_packages
setup(
    name='tracking_log_model',
    version='1.0.0',
    packages=find_packages(),
    description='This module allows you to log parameters, metrics, and artifacts to MLflow using the Tracking Log Model SDK.',
    author='Saurav Kumar',
    author_email='Saurav.Kumar@cognizant.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
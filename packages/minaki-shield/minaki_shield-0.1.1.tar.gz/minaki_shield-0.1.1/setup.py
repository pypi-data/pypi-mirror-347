from setuptools import setup, find_packages

setup(
    name='minaki-shield',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'psutil'
    ],
    entry_points={
        'console_scripts': [
            'shield=shield.cli:main',
        ],
    },
    author='Andrew Polykandriotis',
    description='Modular Linux intrusion detection CLI by MinakiLabs',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ]
)

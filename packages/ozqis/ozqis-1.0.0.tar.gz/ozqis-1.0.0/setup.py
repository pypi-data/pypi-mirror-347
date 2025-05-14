from setuptools import setup, find_packages

setup(
    name='ozqis', 
    version='1.0.0',    
    packages=find_packages(),  
    install_requires=[  
        'numpy', 
        'pennylane', 
    ],
    description='A metric for quantum machine learning.',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    author='Emir Kaan Özdemir',
    author_email='emirkaanbulut08@gmail.com',
    url='https://github.com/emirkaanozdemr/OzQIS',  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
    ],
    license="CC-BY 4.0", 
)

from setuptools import setup, find_packages

setup(
    name="The-Task-Planner",                  
    version="0.1.0",                 
    packages=find_packages(),       
    install_requires=[],            
    author="Chetna Dangwal",
    author_email="chetnadangwal10@email.com",
    description="A simple utility tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Chetna-Dangwal/The-Task-Planner",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

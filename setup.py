from setuptools import setup, find_packages
import os

# Lire le README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Lire les requirements
with open("requirements.txt", "r") as f:
    requirements = [
        line.strip() 
        for line in f 
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="microservice-antipattern-detector",
    version="1.0.0",
    author="AmrAzirar",
    author_email="",
    description="Detect architectural anti-patterns in microservices and integrate in CI/CD pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AmrAzirar/microservice-antipattern-detector",
    packages=find_packages(exclude=["tests*", "datasets*"]),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
    "console_scripts": [
        "antipattern-detect=main:main"
    ]
    },
    py_modules=["main"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Quality Assurance",
    ],
    keywords=[
        "microservices",
        "anti-patterns",
        "architecture",
        "cicd",
        "static-analysis"
    ]
)
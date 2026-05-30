from setuptools import setup, find_packages

setup(
    name="microservice-antipattern-detector",
    version="1.0.0",
    author="AmrAzirar",
    author_email="",
    description="Detect architectural anti-patterns in microservices and integrate in CI/CD pipelines",
    url="https://github.com/AmrAzirar/microservice-antipattern-detector",
    packages=find_packages(exclude=["tests*", "datasets*"]),
    include_package_data=True,
    install_requires=[
        "pyyaml>=6.0",
        "networkx>=3.0",
        "jinja2>=3.1"
    ],
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
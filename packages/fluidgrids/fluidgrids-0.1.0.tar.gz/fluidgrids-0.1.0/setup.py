from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fluidgrids",
    version="0.1.0",
    author="Vignesh T.V",
    author_email="vignesh@algoshred.com",
    description="Python SDK for the FluidGrids Workflow Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://fluidgrids.ai/",
    project_urls={
        "Bug Tracker": "https://github.com/algoshred/fluidgrids/issues",
        "Documentation": "https://docs.fluidgrids.ai/sdk",
        "Source Code": "https://github.com/algoshred/fluidgrids",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
        "python-dateutil>=2.8.2",
    ],
) 
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yaml-config-processor",
    version="0.1.1",
    author="Serhii Setti",
    author_email="serhii.setti@pm.me",
    description="Process YAML templates with JSON configurations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SergeySetti/yaml-config-processor",
    project_urls={
        "Bug Tracker": "https://github.com/SergeySetti/yaml-config-processor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "pyyaml>=5.1",
        "jsonschema>=3.2.0",
    ],
)

from setuptools import setup, find_packages

setup(
    name="testpypi-yoochan35",            # your package name
    version="0.1.0",              # start at 0.1.0
    author="20220656",
    author_email="y.park1@student.tue.nl",
    description="A simple greeting package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YourUser/hello_pypi",  # we'll set this up soon
    packages=find_packages(),      # finds your hello_pypi folder
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
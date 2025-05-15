from setuptools import setup, find_packages

setup(
    name='ezdir',
    version="0.3.0",  # Version of the package
    packages=find_packages(),
    description='Change working directory up a number of levels or to a named folder',
    long_description=open("README.md").read(),  # Long description from the README file
    long_description_content_type="text/markdown",  # The format of the long description
    url="https://github.com/mshodge/ezdir",  # URL to the project homepage
    author='Michael Hodge',
    author_email='michaelstvnhodge@gmail.com',
    keywords=['os', 'directory', 'path', 'utility'],
    classifiers=[  # Classifiers help users find your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python version requirement

)
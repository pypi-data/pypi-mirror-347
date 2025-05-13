from setuptools import setup, find_packages

# Define your version here.
VERSION = "0.0.1"

# Try to read README.md for the long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "RxScrite: An educational programming language built with Python."

setup(
    name="rxscrite", # <<< CHECK PYPI.ORG FOR UNIQUENESS! Change if "rxscrite" is taken.
    version=VERSION,
    author="Rx MHA",  # <<< CHANGE THIS to your actual name
    author_email="rxsocialmedia1@gmail.com",  # <<< CHANGE THIS to your actual email
    description="RxScrite: An educational programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rxmha125/rxscrite_project",  # <<< CHANGE THIS to your project's URL (Optional)
    
    # This will find your 'rxscrite' package directory containing your .py files
    packages=find_packages(where=".", include=["rxscrite", "rxscrite.*"]),
    
    classifiers=[
        "License :: OSI Approved :: MIT License",  # Ensure you have a matching LICENSE file
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Software Development :: Interpreters",
        "Development Status :: 3 - Alpha", 
    ],
    python_requires=">=3.8", # Minimum Python version your project supports
    
    # This creates the command-line script `rxscrite`
    # So after 'pip install .', you can type 'rxscrite yourfile.rx'
    entry_points={
        "console_scripts": [
            "rxscrite=rxscrite.cli:main", 
        ],
    },
    # If your project had other Python package dependencies, you would list them here
    # install_requires=[], # No external dependencies for RxScrite so far
)
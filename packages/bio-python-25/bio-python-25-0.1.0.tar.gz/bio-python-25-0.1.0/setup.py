from setuptools import setup, find_packages

setup(
    name="bio-python-25",  # choose a unique name
    version="0.1.0",
    author="asdf",
    author_email="you@example.com",
    description="Bioinformatics notebooks",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["All Files/*"],  # Include everything inside All Files
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires='>=3.6',
)

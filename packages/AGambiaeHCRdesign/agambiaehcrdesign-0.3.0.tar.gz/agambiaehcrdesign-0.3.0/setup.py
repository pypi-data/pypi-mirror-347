from setuptools import setup, find_packages

setup(
    name="AGambiaeHCRdesign",  # Replace with your package name
    version="0.3.0",  # Initial version
    packages=['AGambiaeHCRdesign'],  # Automatically discover Python packages
    install_requires=[  # Add dependencies here
        "biopython==1.80",  # Example dependency
        "pandas"  # Example dependency
    ],
    author="Chintan Trivedi",
    author_email="c.trivedi@ucl.ac.uk",
    description="HCR probe designer for A.Gambiae",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ctucl/AGambiaeHCRdesign",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

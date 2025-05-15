from setuptools import setup, find_packages

setup(
    name="AGambiaeHCRdesign",  # Replace with your package name
    version="0.1.0",  # Initial version
    packages=find_packages(),  # Automatically discover Python packages
    install_requires=[  # Add dependencies here
        "Bio",  # Example dependency
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
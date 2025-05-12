from setuptools import setup, find_packages

setup(
    name="dles",                  # Your package name
    version="0.1.2",                 # Initial version
    description="A package to load and return program content.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/mlcode",  # Replace with your GitHub repo link
    license="MIT",                   # Or choose the appropriate license
    packages=find_packages(),        # Automatically find packages
    include_package_data=True,       # Include non-Python files
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",          # Minimum Python version required
)

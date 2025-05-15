from setuptools import setup, find_packages

setup(
    name="agenbits",
    version="0.1.2",
    author="Enos",
    author_email="enosuppada2005@gmail.com",
    description="A library to fetch, convert, and decode binary input data for ML models.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dunkdumb/agenbyte",  # Replace with your actual repo
    packages=find_packages(where='.', include=['agenbits', 'agenbits.*']),  # Ensure the inner agenbits package is included
    include_package_data=True,
    install_requires=[
        "requests",
        "pandas",
        "openpyxl",
        "Pillow",
        "numpy",
        "soundfile",
        "opencv-python"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)

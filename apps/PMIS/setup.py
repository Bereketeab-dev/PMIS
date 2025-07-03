from setuptools import setup, find_packages
import os

app_name = "construction_pmis" # This is the main python package name of your app
app_title = "Construction Project Management"
app_publisher = "Bereketeab Philemon (Dev. w/ Jules AI)" # Your Name/Org
app_description = "A custom ERPNext app for managing construction projects based on PMIS principles."
app_email = "your.email@example.com" # Your email
app_license = "MIT"
app_version = "0.0.1" # Should match hooks.py

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = app_description


# Check for requirements.txt and read it
requirements_path = os.path.join(this_directory, 'requirements.txt')
requirements = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        requirements = f.read().splitlines()

# This will look for a folder named `construction_pmis` (matching app_name)
# in the same directory as this setup.py file.
# That `construction_pmis` folder must contain an `__init__.py` file.
packages = find_packages(where=".", include=[app_name, f"{app_name}.*"])


setup(
    name=app_name,
    version=app_version,
    description=app_description,
    author=app_publisher,
    author_email=app_email,
    license=app_license,
    packages=packages, # Correctly specifies the packages to include
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True, # This is important for MANIFEST.in to work
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha", # Or "4 - Beta", "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Framework :: Frappe",
        "License :: OSI Approved :: MIT License",
    ]
)

from setuptools import setup, find_packages

# Define the package metadata
setup(
    name="EmailGenerator",  
    version="0.1.0",  # Initial version
    description="Generates an email address based on person's name, a specified email format and the domain",
    long_description="This Python library generates email addresses based on a specified format and a person's name. It allows for flexibility in how names are represented (initials or first few letters) and handles separators between name parts.",
    long_description_content_type="text/markdown",
    url="https://github.com/daa2618/EmailGenerator.git",  # Replace with your repo URL
    author="Dev Anbarasu",
    author_email="anand26dev@gmail.com",
    packages=find_packages(exclude=["tests", "*.tests", "*.txt", "*.md"]),
    install_requires=[
        "regex",  # Add any external dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "generate_email_address=emailGenerator.generateEmailString:main",
        ]
    },
)
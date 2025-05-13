from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oauth2handler",
    version="0.1.1",
    author="OAuth2 Handler Contributors",
    author_email="tomer.barak.mail@gmail.com",
    description="A simple OAuth2 client for developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tomer-Barak/oauth2handler",
    project_urls={
        "Bug Tracker": "https://github.com/Tomer-Barak/oauth2handler/issues",
        "Source Code": "https://github.com/Tomer-Barak/oauth2handler",
    },
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7", 
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],    
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "oauth2=oauth2handler.cli:main",
        ],
    },
    tests_require=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
)

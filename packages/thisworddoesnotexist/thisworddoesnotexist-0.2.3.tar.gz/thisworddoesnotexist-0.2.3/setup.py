from setuptools import setup, find_packages

setup(
    name="thisworddoesnotexist",
    version="0.2.3",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
    ],
    author="Poofbirb",
    author_email="poofbirb@protonmail.com.com",
    description="Fetch a fake word from thisworddoesnotexist.com",
    entry_points={
        "console_scripts": [
            "thisworddoesnotexist=thisworddoesnotexist:cli",
        ],
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://codeberg.org/poofbirb/thisworddoesnotexist",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 

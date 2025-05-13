from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="morse_pro",
    version="0.1.2",
    author="Chrstphr CHEVALIER",
    author_email="chrstphr.chevalier@gmail.com",
    description="Encode and decode Morse code messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChrstphrChevalier/100DaysOfCode-Python/tree/main/04_Professionnal__(Days82_to_Day100)/Day82__Morse_Pro",
    project_urls={
        "Bug Tracker": "https://github.com/ChrstphrChevalier/100DaysOfCode-Python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    packages=find_packages(),
    package_data={"morse": ["py.typed"]},
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "morse_pro=cli:cli"
        ]
    },
)

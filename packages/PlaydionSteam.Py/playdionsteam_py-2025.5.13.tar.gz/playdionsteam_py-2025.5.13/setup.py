import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PlaydionSteam.Py",
    version="2025.5.13",
    author="Adrian Albrecht",
    author_email="adriandevprojects@gmail.com",
    packages=setuptools.find_packages(),
    url="https://github.com/AdrianDevProjects/steam.py",
    license="GPL-3.0",
    description="Python wrapper for the Steam Web API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
        "pathlib2",
    ]
)

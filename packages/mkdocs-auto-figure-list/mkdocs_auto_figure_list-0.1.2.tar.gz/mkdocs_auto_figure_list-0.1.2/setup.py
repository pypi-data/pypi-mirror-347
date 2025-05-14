from setuptools import setup, find_packages

setup(
    name="mkdocs-auto-figure-list",
    version="0.1.2",
    description="auto creation for figures",
    author = "privatacc",
    url = "https://github.com/Privatacc/mkdocs-auto-figure-list",
    packages=find_packages(),
    install_requires=[
        "mkdocs"
        ],
    entry_points={
        'mkdocs.plugins': [
            'auto-figure-list = plugin.plugin:FigureListCreation'
        ]
    }
)